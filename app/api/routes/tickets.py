
from fastapi import APIRouter, HTTPException, Request

from app.schemas.ticket import TicketCreate, TicketUpdate


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.post("/")
def create_ticket(ticket_data: TicketCreate, request: Request):
    ticket_service = request.app.state.ticket_service

    ticket = ticket_service.create_ticket(ticket_data)

    return {
        "message": "Support ticket created successfully.",
        "ticket": ticket
    }


@router.get("/")
def get_all_tickets(request: Request):
    ticket_service = request.app.state.ticket_service
    tickets = ticket_service.get_all_tickets()

    return {
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/customer/{customer_id}")
def get_customer_tickets(customer_id: str, request: Request):
    ticket_service = request.app.state.ticket_service
    tickets = ticket_service.get_customer_tickets(customer_id)

    return {
        "customer_id": customer_id,
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/status/{status}")
def get_tickets_by_status(status: str, request: Request):
    ticket_service = request.app.state.ticket_service
    tickets = ticket_service.get_tickets_by_status(status)

    return {
        "status": status,
        "total_tickets": len(tickets),
        "tickets": tickets
    }


@router.get("/{ticket_id}")
def get_ticket(ticket_id: str, request: Request):
    ticket_service = request.app.state.ticket_service

    try:
        return ticket_service.get_ticket(ticket_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.patch("/{ticket_id}")
def update_ticket(
    ticket_id: str,
    updates: TicketUpdate,
    request: Request
):
    ticket_service = request.app.state.ticket_service

    try:
        return ticket_service.update_ticket(ticket_id, updates)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: str, request: Request):
    ticket_service = request.app.state.ticket_service

    deleted = ticket_service.delete_ticket(ticket_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found.")

    return {
        "message": "Support ticket deleted successfully."
    }
# Support ticket endpoints will be implemented in a later phase.
