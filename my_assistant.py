# my_assistant.py
# Author: Sebastian Cooper

HANDOFF_WORDS = ["refund", "cancel", "payment"]
MAX_TOOL_ROUNDS = 3


class TournamentAssistant:
    """A mock assistant that answers pickleball tournament questions."""

    def __init__(self, name, instructions, tools, model):
        """Set up the assistant with its toolbox, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user message and the assistant's response."""
        self.history.append({"role": "user", "content": user_message})

        reply = self.choose_reply(user_message)

        self.history.append({"role": "assistant", "content": reply})

        return reply

    def choose_reply(self, user_message):
        """Handle organizer requests before asking the model."""
        if self.needs_human(user_message.lower()):
            return "Please contact a tournament organizer for help with that request."

        return self.model_reply()

    def model_reply(self):
        """Ask the model and safely handle its tool requests."""
        rounds = 0

        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()

            decision = self.model.decide(self.instructions, self.history, tool_list)

            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."

            if "text" in decision:
                return decision["text"]

            name = decision["tool"]
            arguments = decision["arguments"]

            result = self.tools.run(name, arguments, self.history)

            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )

            rounds += 1

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
