
from fastapi import APIRouter, HTTPException, Request

from app.schemas.ticket import TicketCreate, TicketUpdate


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# Create Support Ticket
@router.post("/")
def create_ticket(ticket_data: TicketCreate, request: Request):

    ticket_service = request.app.state.ticket_service

    ticket = ticket_service.create_ticket(ticket_data)

    return {
        "message": "Support ticket created successfully.",
        "ticket": ticket
    }


# Get All Tickets
@router.get("/")
def get_all_tickets(request: Request):

    ticket_service = request.app.state.ticket_service

    return {
        "total_tickets": len(ticket_service.get_all_tickets()),
        "tickets": ticket_service.get_all_tickets()
    }


# Get Tickets By Customer
@router.get("/customer/{customer_id}")
def get_customer_tickets(customer_id: str, request: Request):

    ticket_service = request.app.state.ticket_service

    tickets = ticket_service.get_customer_tickets(customer_id)

    return {
        "customer_id": customer_id,
        "total_tickets": len(tickets),
        "tickets": tickets
    }


# Get Tickets By Status
@router.get("/status/{status}")
def get_tickets_by_status(status: str, request: Request):

    ticket_service = request.app.state.ticket_service

    tickets = ticket_service.get_tickets_by_status(status)

    return {
        "status": status,
        "total_tickets": len(tickets),
        "tickets": tickets
    }


# Get Ticket By ID
@router.get("/{ticket_id}")
def get_ticket(ticket_id: str, request: Request):

    ticket_service = request.app.state.ticket_service

    try:
        return ticket_service.get_ticket(ticket_id)

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


# Update Support Ticket
@router.patch("/{ticket_id}")
def update_ticket(
    ticket_id: str,
    updates: TicketUpdate,
    request: Request
):

    ticket_service = request.app.state.ticket_service

    try:
        return ticket_service.update_ticket(
            ticket_id=ticket_id,
            updates=updates
        )

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


# Delete Support Ticket
@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: str, request: Request):

    ticket_service = request.app.state.ticket_service

    deleted = ticket_service.delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    return {
        "message": "Support ticket deleted successfully."
    }
