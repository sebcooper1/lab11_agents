from fake_model import FakeModel
from my_assistant import TournamentAssistant
from my_tool import TournamentLookup
from registration_queue import RegistrationQueue
from tournament_toolbox import TournamentToolbox


def make_assistant(model):
    """Create a tournament assistant with fresh tools."""
    lookup = TournamentLookup(
        {
            "time": "Friday at 9 AM",
            "location": "Tampa Pickleball Crew",
            "players": "80 players",
            "courts": "8 courts",
        }
    )

    queue = RegistrationQueue()
    tools = TournamentToolbox(lookup, queue)

    bot = TournamentAssistant("Robin", "Be friendly.", tools, model)
    return bot, queue


def ask_for_tool(name, arguments):
    """Create a fake tool request."""
    return {"tool": name, "arguments": arguments}


def test_model_can_look_up_tournament_location():
    model = FakeModel(
        [
            ask_for_tool("get_tournament_info", {"topic": "location"}),
            {"text": "The tournament is at Tampa Pickleball Crew."},
        ]
    )

    bot, _ = make_assistant(model)
    reply = bot.respond("Where is the tournament?")

    assert "Tampa Pickleball Crew" in reply
    assert bot.history[1]["role"] == "tool"
    assert bot.history[1]["content"] == "Tampa Pickleball Crew"


def test_made_up_player_name_is_refused():
    model = FakeModel(
        [
            ask_for_tool("request_registration", {"player_name": "Alex Smith"}),
            {"text": "Please provide your full name."},
        ]
    )

    bot, queue = make_assistant(model)
    bot.respond("I want to sign up.")

    assert "has not provided" in bot.history[1]["content"]
    assert queue.waiting() == []
    assert queue.registrations == []


def test_registration_waits_for_approval():
    model = FakeModel(
        [
            ask_for_tool("request_registration", {"player_name": "Alex Smith"}),
            {"text": "Your registration is waiting for approval."},
        ]
    )

    bot, queue = make_assistant(model)
    bot.respond("Please sign up Alex Smith.")

    assert len(queue.waiting()) == 1
    assert queue.registrations == []
    assert queue.waiting()[0]["player_name"] == "Alex Smith"


def test_registration_can_only_be_approved_once():
    queue = RegistrationQueue()

    queue.request_registration("Alex Smith")

    assert queue.approve(1) == "Request 1 approved."
    assert "already approved" in queue.approve(1)
    assert queue.registrations == ["Alex Smith"]


def test_refund_goes_to_an_organizer():
    model = FakeModel([{"text": "This should not be used."}])
    bot, _ = make_assistant(model)

    reply = bot.respond("I need a refund.")

    assert "organizer" in reply
    assert model.calls == 0


def test_unknown_tool_is_refused():
    model = FakeModel(
        [
            ask_for_tool("delete_tournament", {}),
            {"text": "I cannot do that."},
        ]
    )

    bot, _ = make_assistant(model)
    bot.respond("Please delete the tournament.")

    assert "There is no tool named" in bot.history[1]["content"]
