# my_main.py
# Author: Sebastian Cooper

from my_assistant import TournamentAssistant
from my_tool import TournamentLookup
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are PickleBot, a helpful assistant for a pickleball tournament.
Answer questions in one short sentence.
The tournament starts at 9:00 AM.
The tournament takes place in Tampa, Florida.
There are 80 available player spots and 8 pickleball courts.
Only state facts that appear in these instructions.
If you do not know the answer, say you do not know and suggest contacting a tournament organizer."""

TOURNAMENT_INFO = {
    "time": "The tournament starts at 9:00 AM.",
    "location": "The tournament takes place in Tampa, Florida.",
    "players": "The tournament allows up to 80 players.",
    "courts": "There will be 8 pickleball courts available.",
}

tournament_tool = TournamentLookup(TOURNAMENT_INFO)
model = OllamaModel(MODEL_NAME)


bot = TournamentAssistant(
    "PickleBot",
    "You help customers find information about a pickleball tournament.",
    tournament_tool,
    model,
)

print("Welcome to PickleBot!")
print("Type quit to stop.")

user_message = input("You: ")

while user_message.lower() != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
