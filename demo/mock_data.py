"""Mock customer database for Acme Galactic Financial Services.

All data is fictional and Star Wars themed.
"""

CUSTOMERS = {
    "luke.skywalker@rebelalliance.org": {
        "name": "Luke Skywalker",
        "email": "luke.skywalker@rebelalliance.org",
        "account_id": "ACT-77421",
        "ssn": "000-42-1234",
        "phone": "555-290-7753",
        "address": "42 Moisture Farm Lane, Anchorhead, Tatooine 00042",
        "balance": "$12,450.77",
        "recent_transactions": [
            {"date": "2026-02-20", "description": "Docking Bay 94 - Ship Repair", "amount": "-$450.00"},
            {"date": "2026-02-18", "description": "Tosche Station - Power Converters", "amount": "-$89.99"},
            {"date": "2026-02-15", "description": "Rebel Alliance Payroll", "amount": "+$3,200.00"},
        ],
    },
    "leia.organa@rebelalliance.org": {
        "name": "Leia Organa",
        "email": "leia.organa@rebelalliance.org",
        "account_id": "ACT-10019",
        "ssn": "000-66-5678",
        "phone": "555-843-1138",
        "address": "1 Royal Palace Drive, Aldera, Alderaan 00001",
        "balance": "$84,102.33",
        "recent_transactions": [
            {"date": "2026-02-21", "description": "Diplomatic Transport Fuel", "amount": "-$1,200.00"},
            {"date": "2026-02-19", "description": "Secure Comms Array Subscription", "amount": "-$299.00"},
            {"date": "2026-02-14", "description": "Senate Stipend Deposit", "amount": "+$7,500.00"},
        ],
    },
    "han.solo@millenniumfalcon.net": {
        "name": "Han Solo",
        "email": "han.solo@millenniumfalcon.net",
        "account_id": "ACT-55320",
        "ssn": "000-37-9012",
        "phone": "555-432-1977",
        "address": "Bay 7, Smuggler's Row, Mos Eisley, Tatooine 00099",
        "balance": "$2,187.00",
        "recent_transactions": [
            {"date": "2026-02-22", "description": "Coaxium Fuel Purchase", "amount": "-$800.00"},
            {"date": "2026-02-17", "description": "Kessel Run Delivery Payment", "amount": "+$5,000.00"},
            {"date": "2026-02-12", "description": "Payment to Jabba the Hutt", "amount": "-$3,500.00"},
        ],
    },
    "padme.amidala@naboo.gov": {
        "name": "Padme Amidala",
        "email": "padme.amidala@naboo.gov",
        "account_id": "ACT-40088",
        "ssn": "000-15-3456",
        "phone": "555-114-0032",
        "address": "Theed Royal Palace, Lake Country, Naboo 00010",
        "balance": "$156,820.91",
        "recent_transactions": [
            {"date": "2026-02-21", "description": "Senate Campaign Fund", "amount": "+$25,000.00"},
            {"date": "2026-02-16", "description": "Handmaiden Security Detail", "amount": "-$4,500.00"},
            {"date": "2026-02-10", "description": "Naboo Charitable Foundation", "amount": "-$10,000.00"},
        ],
    },
    "din.djarin@mandalore.net": {
        "name": "Din Djarin",
        "email": "din.djarin@mandalore.net",
        "account_id": "ACT-66713",
        "ssn": "000-28-7890",
        "phone": "555-667-1300",
        "address": "Covert Bunker 7, Underground, Nevarro 00077",
        "balance": "$31,500.00",
        "recent_transactions": [
            {"date": "2026-02-22", "description": "Beskar Armor Upgrade", "amount": "-$7,000.00"},
            {"date": "2026-02-19", "description": "Bounty Payout - Guild", "amount": "+$15,000.00"},
            {"date": "2026-02-13", "description": "Razor Crest Fuel & Repairs", "amount": "-$2,300.00"},
        ],
    },
}


def find_customer(identifier: str) -> dict | None:
    """Search for a customer by name, email, or account ID."""
    identifier_lower = identifier.lower().strip()

    for email, customer in CUSTOMERS.items():
        if identifier_lower == email.lower():
            return customer

    for customer in CUSTOMERS.values():
        if identifier_lower in customer["name"].lower():
            return customer

    for customer in CUSTOMERS.values():
        if identifier_lower == customer["account_id"].lower():
            return customer

    return None
