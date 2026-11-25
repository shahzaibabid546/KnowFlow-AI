# Ticket business logic will be implemented here.

from app.schemas.ticket import SupportTicket, TicketCreate, TicketUpdate
from app.storage.ticket_store import TicketStore


class TicketService:

    def __init__(self, ticket_store: TicketStore):

        self.ticket_store = ticket_store

    # Create a New Support Ticket
    def create_ticket(
        self,
        ticket_data: TicketCreate
    ) -> SupportTicket:

        ticket = SupportTicket(
            **ticket_data.model_dump()
        )

        return self.ticket_store.create_ticket(ticket)

    # Get Ticket by ID
    def get_ticket(
        self,
        ticket_id: str
    ) -> SupportTicket:

        ticket = self.ticket_store.get_ticket(ticket_id)

        if ticket is None:
            raise ValueError("Ticket not found.")

        return ticket

    # Get All Support Tickets
    def get_all_tickets(self) -> list[SupportTicket]:

        return self.ticket_store.get_all_tickets()

    # Update Existing Ticket
    def update_ticket(
        self,
        ticket_id: str,
        updates: TicketUpdate
    ) -> SupportTicket:

        return self.ticket_store.update_ticket(
            ticket_id=ticket_id,
            updates=updates
        )

    # Delete Support Ticket
    def delete_ticket(self, ticket_id: str) -> bool:

        return self.ticket_store.delete_ticket(ticket_id)

    # Get Customer Tickets
    def get_customer_tickets(
        self,
        customer_id: str
    ) -> list[SupportTicket]:

        return self.ticket_store.get_customer_tickets(
            customer_id
        )

    # Get Tickets by Status
    def get_tickets_by_status(
        self,
        status: str
    ) -> list[SupportTicket]:

        return self.ticket_store.get_tickets_by_status(
            status
        )
