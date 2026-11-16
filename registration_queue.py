# registration_queue.py
# Author: Sebastian Cooper


class RegistrationQueue:
    """Hold tournament registrations until an organizer approves them."""

    def __init__(self):
        self.requests = []
        self.next_number = 1
        self.registrations = []

    def request_registration(self, player_name):
        """Request a tournament registration for organizer approval.

        Args:
            player_name: The full name of the player registering.
        """
        request = {
            "number": self.next_number,
            "player_name": player_name,
            "status": "waiting",
        }

        self.requests.append(request)
        self.next_number += 1

        return f"Request {request['number']} was sent to an organizer. Registration is waiting for approval."

    def waiting(self):
        """Return all registration requests still waiting for approval."""
        return [request for request in self.requests if request["status"] == "waiting"]

    def approve(self, number):
        """Approve a registration request only once."""
        for request in self.requests:
            if request["number"] == number:
                if request["status"] != "waiting":
                    return f"Request {number} is already {request['status']}."

                request["status"] = "approved"
                self.registrations.append(request["player_name"])
                return f"Request {number} approved."

        return f"No request {number} was found."

    def reject(self, number):
        """Reject a registration without adding the player."""
        for request in self.requests:
            if request["number"] == number:
                if request["status"] != "waiting":
                    return f"Request {number} is already {request['status']}."

                request["status"] = "rejected"
                return f"Request {number} rejected."

        return f"No request {number} was found."
