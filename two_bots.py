from chatbot import SupportChatbot
from change_queue import ChangeQueue
from keyword_model import KeywordModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox


def make_bot(name, instructions):
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
    }

    order_tool = OrderLookup(orders)
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    change_queue = ChangeQueue(order_tool)
    tools = Toolbox(order_tool, stock_tool, change_queue)

    model = KeywordModel()

    return SupportChatbot(name, instructions, tools, model)


def main():
    sunny = make_bot("Sunny", "Be friendly and helpful.")
    river = make_bot("River", "Be brief and professional.")

    print(sunny.respond("hello"))
    print(river.respond("hello"))

    print("Sunny's messages:", sunny.count_user_messages())
    print("River's messages:", river.count_user_messages())


if __name__ == "__main__":
    main()
