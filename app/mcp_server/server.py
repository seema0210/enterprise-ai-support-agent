
from mcp.server import MCPServer

mcp = MCPServer("EnterpriseSupportServer")


TICKETS = {
    "T101": {
        "status": "Open",
        "priority": "High",
        "assigned_team": "Payments Support",
        "customer": "ABC Retail",
        "issue": "Customer payment failed during checkout.",
        "resolution": "Investigation is in progress."
    },
    "T102": {
        "status": "In Progress",
        "priority": "Critical",
        "assigned_team": "Engineering",
        "customer": "XYZ Technologies",
        "issue": "Users cannot log in after password reset.",
        "resolution": "Engineering is investigating the authentication service."
    },
    "T103": {
        "status": "Resolved",
        "priority": "Medium",
        "assigned_team": "Account Support",
        "customer": "Global Services",
        "issue": "Account verification email was not received.",
        "resolution": "Email delivery configuration was corrected."
    }
}


@mcp.tool()
def get_ticket_status(ticket_id: str) -> dict:
    """Get the status, priority, and assigned team of a support ticket."""

    ticket = TICKETS.get(ticket_id.upper())

    if ticket is None:
        return {"error": "Ticket not found"}

    return {
        "ticket_id": ticket_id.upper(),
        "status": ticket["status"],
        "priority": ticket["priority"],
        "assigned_team": ticket["assigned_team"]
    }


@mcp.tool()
def get_ticket_details(ticket_id: str) -> dict:
    """Get the customer issue, description, and resolution of a support ticket."""

    ticket = TICKETS.get(ticket_id.upper())

    if ticket is None:
        return {"error": "Ticket not found"}

    return {
        "ticket_id": ticket_id.upper(),
        "customer": ticket["customer"],
        "issue": ticket["issue"],
        "resolution": ticket["resolution"]
    }


if __name__ == "__main__":
    mcp.run()
