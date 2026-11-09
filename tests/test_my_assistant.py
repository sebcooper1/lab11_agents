from mock_model import MockModel
from my_assistant import TournamentAssistant
from my_tool import TournamentLookup


def make_bot():
    """Create a new tournament assistant for each test."""
    info = {
        "time": "The tournament starts at 9:00 AM.",
        "players": "The tournament allows up to 80 players.",
    }

    tool = TournamentLookup(info)

    return TournamentAssistant("PickleBot", "Be helpful.", tool, MockModel())


def test_tournament_time():
    bot = make_bot()
    reply = bot.respond("What time does it start?")
    assert reply == "The tournament starts at 9:00 AM."


def test_unknown_topic():
    bot = make_bot()
    reply = bot.respond("What is the parking situation?")
    assert "not sure" in reply


def test_human_handoff():
    bot = make_bot()
    reply = bot.respond("Can I get a refund?")
    assert "organizer" in reply


def test_unknown_request():
    bot = make_bot()
    reply = bot.respond("Tell me a joke")
    assert "not sure" in reply


def test_history():
    bot = make_bot()
    bot.respond("hello")
    bot.respond("What time does it start?")

    assert len(bot.history) == 4


class SilentModel:
    """A model that returns no response."""

    def reply(self, instructions, history):
        return None


def test_model_unavailable():
    info = {"time": "The tournament starts at 9:00 AM."}
    tool = TournamentLookup(info)

    bot = TournamentAssistant("PickleBot", "Be helpful.", tool, SilentModel())

    reply = bot.respond("hello")

    assert "try again" in reply
