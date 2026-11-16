# tournament_toolbox.py
# Author: Sebastian Cooper


class TournamentToolbox:
    """Check and run tournament tools requested by the model."""

    def __init__(self, tournament_tool, registration_queue):
        """Store the tournament tool and registration queue."""
        self.tournament_tool = tournament_tool
        self.registration_queue = registration_queue

    def tool_list(self):
        """Return the tools the model may request."""
        return [
            self.tournament_tool.get_tournament_info,
            self.registration_queue.request_registration,
        ]

    def run(self, name, arguments, history):
        """Check a tool request before allowing it to run."""

        if name == "get_tournament_info":
            topic = str(arguments.get("topic", "")).strip().lower()

            if topic == "":
                return "The tournament topic is missing. Ask the customer."

            allowed_phrases = {
                "time": ["time", "when", "schedule"],
                "location": ["location", "where", "venue"],
                "players": ["players", "participants"],
                "courts": ["courts", "court"],
            }

            if topic not in allowed_phrases:
                return "That tournament topic is not available."

            if not any(
                self.customer_said(history, phrase) for phrase in allowed_phrases[topic]
            ):
                return "The customer has not asked about that tournament topic."

            return self.tournament_tool.get_tournament_info(topic)

        if name == "request_registration":
            player_name = str(arguments.get("player_name", "")).strip()

            if player_name == "":
                return "The player's name is missing. Ask the customer."

            if not self.customer_said(history, player_name):
                return "The customer has not provided that player's name. Ask them."

            return self.registration_queue.request_registration(player_name)

        return f"There is no tool named {name}."

    def customer_said(self, history, text):
        """Check whether the customer actually supplied the information."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True

        return False
