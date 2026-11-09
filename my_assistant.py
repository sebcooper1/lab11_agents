# my_assistant.py
# Author: Sebastian Cooper

HANDOFF_WORDS = ["register", "refund", "cancel", "payment"]


class TournamentAssistant:
    """A mock assistant that answers pickleball tournament questions."""

    def __init__(self, name, instructions, tournament_tool, model):
        """Set up the assistant with a tool and conversation history."""
        self.name = name
        self.instructions = instructions
        self.tournament_tool = tournament_tool
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user message and the assistant's response."""
        self.history.append({"role": "user", "content": user_message})

        reply = self.choose_reply(user_message)

        self.history.append({"role": "assistant", "content": reply})

        return reply

    def choose_reply(self, user_message):
        """Use tournament rules first, then ask the model."""
        text = user_message.lower()

        if self.needs_human(text):
            return "Please contact a tournament organizer for help with that request."

        topic = self.tournament_tool.find_topic(user_message)

        if topic is not None:
            return self.tournament_reply(user_message)

        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply and provide a safe fallback."""
        reply = self.model.reply(self.instructions, self.history)

        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."

        return reply

    def needs_human(self, text):
        """Check whether the request requires a tournament organizer."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def tournament_reply(self, user_message):
        """Use the tournament tool to look up information."""
        topic = self.tournament_tool.find_topic(user_message)

        if topic is None:
            return "I couldn't find that information. Please ask about time, location, players, or courts."

        answer = self.tournament_tool.info_for(topic)

        if answer is None:
            return "I couldn't find that tournament information."

        return answer
