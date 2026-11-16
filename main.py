# main.py
# Author: Sebastian Cooper
from fallback_model import FallbackModel
from keyword_model import KeywordModel
from chatbot import SupportChatbot
from change_queue import ChangeQueue
from ollama_model import OllamaModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox

INSTRUCTIONS = """
You are Sunny, a friendly customer support assistant.
You can help customers look up orders, check product stock,
and request shipping address changes.

Use the available tools when needed.
Do not invent order information or stock quantities.
For address changes, use the change_address tool.
An address change must be approved by a staff member before
the actual address is updated.
"""


def main():
    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
    }

    stock = {
        "rain jacket": 12,
        "day pack": 0,
    }

    order_tool = OrderLookup(orders)
    stock_tool = StockLookup(stock)
    change_queue = ChangeQueue(order_tool)
    tools = Toolbox(order_tool, stock_tool, change_queue)

    model = FallbackModel(
    OllamaModel("granite4.1:3b"),
    KeywordModel()
)
    bot = SupportChatbot("Sunny", INSTRUCTIONS, tools, model)

    print("Sunny Support Chatbot")
    print("Type 'quit' to stop.")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "quit":
            break

        reply = bot.respond(user_message)
        print(f"Sunny: {reply}")

    print("\nPending address changes:")
    for request in change_queue.waiting():
        print(request)

    for request in change_queue.waiting():
        answer = input(
            f"Approve request {request['number']}? (yes/no): "
        ).strip().lower()

        if answer == "yes":
            print(change_queue.approve(request["number"]))
        else:
            print(change_queue.reject(request["number"]))


if __name__ == "__main__":
    main()
