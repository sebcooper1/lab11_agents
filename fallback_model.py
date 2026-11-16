# fallback_model.py
# Author: Sebastian Cooper


class FallbackModel:
    """Ask the first model. If it has no answer, ask the second."""

    def __init__(self, first, second):
        """Store the two models in the order they are asked."""
        self.first = first
        self.second = second

    def decide(self, instructions, history, tools):
        """Use the backup if the first model returns None."""
        decision = self.first.decide(instructions, history, tools)

        if decision is None:
            return self.second.decide(instructions, history, tools)

        return decision
