# my_tool.py
# Author: Sebastian Cooper


class TournamentLookup:
    """A tool that stores information about a pickleball tournament."""

    def __init__(self, tournament_info):
        """Store tournament information."""
        self.tournament_info = tournament_info

    def find_topic(self, text):
        """Find a known tournament topic in the user's message."""
        text = text.lower()

        if "where" in text:
            return "location"

        for topic in self.tournament_info:
            if topic in text:
                return topic

        return None

    def info_for(self, topic):
        """Return information for a topic or None if unknown."""
        if topic in self.tournament_info:
            return self.tournament_info[topic]
        return None

    def get_tournament_info(self, topic):
        """Look up information about a pickleball tournament.

        Args:
            topic: The tournament topic, such as time, location, players, or courts.
        """
        topic = topic.lower().strip()

        answer = self.info_for(topic)

        if answer is None:
            return "I couldn't find that tournament information."

        return answer
