from app.tools import (
    get_payment,
    get_user_balance,
    search_knowledge
)

TOOLS = {
    "get_user_balance": get_user_balance.execute,
    "get_payment": get_payment.execute,
    "search_knowledge": search_knowledge.execute,
}