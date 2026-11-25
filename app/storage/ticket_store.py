
from datetime import datetime, timezone

from app.schemas.ticket import SupportTicket, TicketUpdate


class TicketStore:

    def __init__(self):

        # Store all tickets in memory
        self.tickets: dict[str, SupportTicket] = {}

    # Create a New Ticket
    def create_ticket(
        self,
        ticket: SupportTicket
    ) -> SupportTicket:

        self.tickets[ticket.ticket_id] = ticket

        return ticket

    # Get Ticket by ID
    def get_ticket(
        self,
        ticket_id: str
    ) -> SupportTicket | None:

        return self.tickets.get(ticket_id)

    # Get All Tickets
    def get_all_tickets(self) -> list[SupportTicket]:

        return list(self.tickets.values())

    # Update Existing Ticket
    def update_ticket(
        self,
        ticket_id: str,
        updates: TicketUpdate
    ) -> SupportTicket:

        ticket = self.get_ticket(ticket_id)

        if ticket is None:
            raise ValueError("Ticket not found.")

        update_data = updates.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():

            setattr(ticket, field, value)

        ticket.updated_at = datetime.now(timezone.utc)

        return ticket

    # Delete Ticket
    def delete_ticket(
        self,
        ticket_id: str
    ) -> bool:

        if ticket_id not in self.tickets:
            return False

        del self.tickets[ticket_id]

        return True

    # Get Tickets by Customer
    def get_customer_tickets(
        self,
        customer_id: str
    ) -> list[SupportTicket]:

        return [
            ticket
            for ticket in self.tickets.values()
            if ticket.customer_id == customer_id
        ]

    # Get Tickets by Status
    def get_tickets_by_status(
        self,
        status: str
    ) -> list[SupportTicket]:

        return [
            ticket
            for ticket in self.tickets.values()
            if ticket.status == status
        ]
