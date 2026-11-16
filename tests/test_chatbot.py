from change_queue import ChangeQueue
from chatbot import SupportChatbot
from fake_model import FakeModel
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox


class SilentModel:
    """A model that never has an answer."""

    def decide(self, instructions, history, tools):
        return None


def make_bot(model):
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
    }

    order_tool = OrderLookup(orders)
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    change_queue = ChangeQueue(order_tool)

    tools = Toolbox(order_tool, stock_tool, change_queue)

    return SupportChatbot("Sunny", "Be friendly.", tools, model)


def ask_for_tool(name, arguments):
    """Create a tool request that FakeModel can return."""
    return {"tool": name, "arguments": arguments}


def test_respond_records_both_messages():
    bot = make_bot(KeywordModel())
    bot.respond("hello")
    assert len(bot.history) == 2
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def test_order_question_uses_the_tool():
    bot = make_bot(KeywordModel())
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_two_chatbots_keep_separate_histories():
    first = make_bot(KeywordModel())
    second = make_bot(KeywordModel())

    first.respond("hello")

    assert len(first.history) == 2
    assert len(second.history) == 0


def test_count_user_messages():
    bot = make_bot(KeywordModel())

    bot.respond("hello")
    bot.respond("What is the weather?")

    assert bot.count_user_messages() == 2


def test_payment_question_goes_to_a_human():
    bot = make_bot(KeywordModel())

    assert "human" in bot.respond("I have a payment question.")


def test_card_question_goes_to_a_human():
    bot = make_bot(KeywordModel())

    assert "human" in bot.respond("Can I change my card?")


def test_safe_reply_when_model_has_no_answer():
    bot = make_bot(SilentModel())

    assert "try again" in bot.respond("hello")


def test_fake_model_returns_text():
    model = FakeModel([{"text": "Welcome!"}])
    bot = make_bot(model)

    assert bot.respond("hello") == "Welcome!"


def test_fake_model_can_request_order_lookup():
    model = FakeModel(
        [
            ask_for_tool("look_up_order", {"order_id": "A100"}),
            {"text": "Your order has shipped."},
        ]
    )
    bot = make_bot(model)

    assert bot.respond("Please check A100") == "Your order has shipped."


def test_fake_model_can_request_stock_lookup():
    model = FakeModel(
        [
            ask_for_tool("check_stock", {"item": "rain jacket"}),
            {"text": "We have 12 rain jackets."},
        ]
    )
    bot = make_bot(model)

    assert bot.respond("Is the rain jacket in stock?") == "We have 12 rain jackets."


def test_fake_model_tool_result_is_saved_in_history():
    model = FakeModel(
        [
            ask_for_tool("look_up_order", {"order_id": "A100"}),
            {"text": "Your order has shipped."},
        ]
    )
    bot = make_bot(model)

    bot.respond("Check order A100")

    assert bot.history[1]["role"] == "tool"
    assert "shipped" in bot.history[1]["content"]


def test_address_change_request_does_not_apply_immediately():
    model = FakeModel(
        [
            ask_for_tool(
                "change_address",
                {"order_id": "A100", "new_address": "25 Oak Street"},
            ),
            {"text": "Your address change request is waiting for approval."},
        ]
    )
    bot = make_bot(model)

    reply = bot.respond("Change order A100 to 25 Oak Street")

    assert "waiting for approval" in reply
    assert bot.tools.order_tool.orders["A100"]["address"] == "14 Bay Road"


def test_three_tool_round_limit():
    model = FakeModel(
        [
            ask_for_tool("check_stock", {"item": "rain jacket"}),
            ask_for_tool("check_stock", {"item": "rain jacket"}),
            ask_for_tool("check_stock", {"item": "rain jacket"}),
        ]
    )
    bot = make_bot(model)

    reply = bot.respond("Check stock for rain jacket")

    assert "human" in reply
    assert model.calls == 3


def test_handoff_does_not_call_model():
    model = FakeModel([{"text": "This should not be used."}])
    bot = make_bot(model)

    reply = bot.respond("I have a payment question.")

    assert "human" in reply
    assert model.calls == 0


def test_model_can_ask_about_a_return():
    model = FakeModel(
        [
            ask_for_tool("check_return", {"order_id": "A100"}),
            {"text": "Not yet."},
        ]
    )

    bot = make_bot(model)
    bot.respond("Can I return order A100?")

    assert "cannot be returned yet" in bot.history[1]["content"]


def test_lookups_keep_working_when_the_model_is_down():
    bot = make_bot(FallbackModel(SilentModel(), KeywordModel()))
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."
