# my_main.py
# Author: Sebastian Cooper

from my_assistant import TournamentAssistant
from my_tool import TournamentLookup
from ollama_model import OllamaModel
from registration_queue import RegistrationQueue
from tournament_toolbox import TournamentToolbox

INSTRUCTIONS = """
You are a friendly assistant for a pickleball tournament.

You can answer questions about tournament times,
location, players, and courts.

Use get_tournament_info when the user asks about
tournament information.

Use request_registration when someone wants to register.
Ask for the player's full name before requesting registration.

Registration requests must be approved by an organizer
before the player is officially registered.

If the user only says hello, greet them and ask how you can help.

Do not invent tournament details or player names.
"""


def main():
    tournament_info = {
        "time": "Friday at 9 AM",
        "location": "Tampa Pickleball Crew",
        "players": "80 players",
        "courts": "8 courts",
    }

    tournament_tool = TournamentLookup(tournament_info)
    registration_queue = RegistrationQueue()

    tools = TournamentToolbox(tournament_tool, registration_queue)
    model = OllamaModel("granite4.1:3b")

    bot = TournamentAssistant("Robin", INSTRUCTIONS, tools, model)

    print("Robin Tournament Assistant")
    print("Type 'quit' to stop.")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "quit":
            break

        reply = bot.respond(user_message)
        print(f"Robin: {reply}")

    print("\nOrganizer review:")

    for request in registration_queue.waiting():
        print(request)

        answer = (
            input(f"Approve request {request['number']}? (yes/no): ").strip().lower()
        )

        if answer == "yes":
            print(registration_queue.approve(request["number"]))
        else:
            print(registration_queue.reject(request["number"]))

    print("\nApproved registrations:")
    print(registration_queue.registrations)


if __name__ == "__main__":
    main()
