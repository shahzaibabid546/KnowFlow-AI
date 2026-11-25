
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.storage.ticket_store import TicketStore
from app.services.ticket_service import TicketService


print("\n========== TICKET MANAGEMENT TEST ==========")


# Step 1: Initialize Ticket Store
print("\nStep 1: Initializing Ticket Store...")

ticket_store = TicketStore()

print("Ticket Store Ready!")


# Step 2: Initialize Ticket Service
print("\nStep 2: Initializing Ticket Service...")

ticket_service = TicketService(
    ticket_store=ticket_store
)

print("Ticket Service Ready!")


# Step 3: Create First Ticket
print("\nStep 3: Creating First Support Ticket...")

ticket_data = TicketCreate(
    customer_id="customer_101",
    session_id="session_101",
    subject="Refund Not Received",
    description="Customer has not received the refund after purchase.",
    priority="high"
)

ticket = ticket_service.create_ticket(ticket_data)

print("Ticket Created Successfully!")
print("Ticket ID:", ticket.ticket_id)
print("Customer ID:", ticket.customer_id)
print("Subject:", ticket.subject)
print("Status:", ticket.status)
print("Priority:", ticket.priority)


# Step 4: Create Second Ticket
print("\nStep 4: Creating Second Support Ticket...")

second_ticket_data = TicketCreate(
    customer_id="customer_102",
    session_id="session_102",
    subject="Login Problem",
    description="Customer cannot log into their account.",
    priority="normal"
)

second_ticket = ticket_service.create_ticket(
    second_ticket_data
)

print("Second Ticket Created Successfully!")
print("Second Ticket ID:", second_ticket.ticket_id)


# Step 5: Get Ticket by ID
print("\nStep 5: Retrieving Ticket by ID...")

retrieved_ticket = ticket_service.get_ticket(
    ticket.ticket_id
)

print("Ticket Retrieved Successfully!")
print("Subject:", retrieved_ticket.subject)


# Step 6: Get All Tickets
print("\nStep 6: Retrieving All Tickets...")

all_tickets = ticket_service.get_all_tickets()

print("Total Tickets:", len(all_tickets))

for item in all_tickets:

    print("\nTicket ID:", item.ticket_id)
    print("Subject:", item.subject)
    print("Status:", item.status)


# Step 7: Update Ticket
print("\nStep 7: Updating First Ticket...")

ticket_updates = TicketUpdate(
    status="in_progress",
    priority="urgent",
    assigned_to="support_agent_01"
)

updated_ticket = ticket_service.update_ticket(
    ticket_id=ticket.ticket_id,
    updates=ticket_updates
)

print("Ticket Updated Successfully!")
print("New Status:", updated_ticket.status)
print("New Priority:", updated_ticket.priority)
print("Assigned To:", updated_ticket.assigned_to)


# Step 8: Get Customer Tickets
print("\nStep 8: Retrieving Customer Tickets...")

customer_tickets = ticket_service.get_customer_tickets(
    "customer_101"
)

print("Customer Tickets:", len(customer_tickets))

for item in customer_tickets:

    print("Subject:", item.subject)


# Step 9: Get Tickets by Status
print("\nStep 9: Filtering Tickets by Status...")

open_tickets = ticket_service.get_tickets_by_status(
    "open"
)

print("Open Tickets:", len(open_tickets))

in_progress_tickets = ticket_service.get_tickets_by_status(
    "in_progress"
)

print("In Progress Tickets:", len(in_progress_tickets))


# Step 10: Delete Ticket
print("\nStep 10: Deleting Second Ticket...")

deleted = ticket_service.delete_ticket(
    second_ticket.ticket_id
)

print("Ticket Deleted:", deleted)


# Step 11: Verify Deletion
print("\nStep 11: Verifying Ticket Deletion...")

remaining_tickets = ticket_service.get_all_tickets()

print("Remaining Tickets:", len(remaining_tickets))

deleted_ticket = ticket_store.get_ticket(
    second_ticket.ticket_id
)

print("Deleted Ticket:", deleted_ticket)


# Step 12: Test Invalid Ticket ID
print("\nStep 12: Testing Invalid Ticket ID...")

try:

    ticket_service.get_ticket("invalid_ticket_id")

except ValueError as error:

    print("Expected Error:", error)


print("\n========== TEST COMPLETED ==========")
