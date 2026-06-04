"""
Popula o banco com 30 usuários e 150 pagamentos fictícios do Banco Nexus.
Idempotente: verifica se já existem registros antes de inserir.

Uso:
    python -m app.seed_db
"""

import random
import uuid
from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.models.payment import Payment
from app.models.user import User

# ── Dados fictícios ────────────────────────────────────────────────────────────

NOMES = [
    "Ana Souza", "Bruno Lima", "Carla Ferreira", "Diego Oliveira", "Eduarda Costa",
    "Fábio Santos", "Gabriela Rocha", "Henrique Alves", "Isabela Martins", "João Pereira",
    "Karina Mendes", "Leonardo Barbosa", "Mariana Carvalho", "Nicolas Ribeiro", "Olivia Gomes",
    "Paulo Nascimento", "Quésia Fernandes", "Rafael Azevedo", "Sabrina Moreira", "Thiago Castro",
    "Ursula Correia", "Vitor Monteiro", "Wanessa Cunha", "Xerxes Duarte", "Yasmin Nunes",
    "Zara Freitas", "Andrey Lopes", "Beatriz Cardoso", "Caio Pinto", "Daniela Vieira",
]

PROVIDERS = ["pix", "cartao_credito", "cartao_debito", "boleto", "ted"]

PROVIDER_WEIGHTS = [0.45, 0.25, 0.15, 0.10, 0.05]

STATUSES = ["pago", "pendente", "falhou", "reembolsado", "chargeback"]

STATUS_WEIGHTS = [0.60, 0.15, 0.12, 0.08, 0.05]

AMOUNTS = [
    (10, 100, 0.20),
    (100, 500, 0.35),
    (500, 2000, 0.25),
    (2000, 6000, 0.12),
    (6000, 15000, 0.08),
]


def _random_amount() -> float:
    rand = random.random()
    cumulative = 0.0
    for low, high, weight in AMOUNTS:
        cumulative += weight
        if rand <= cumulative:
            return round(random.uniform(low, high), 2)
    return round(random.uniform(100, 1000), 2)


def _random_date(days_back: int = 90) -> datetime:
    delta = random.randint(0, days_back * 24 * 60)
    return datetime.utcnow() - timedelta(minutes=delta)


def seed(db) -> None:
    existing_users = db.query(User).count()
    if existing_users >= 30:
        print(f"Usuários já existem ({existing_users} registros) — pulando seed de usuários.")
        users = db.query(User).all()
    else:
        print("Inserindo 30 usuários...")
        users = []
        for nome in NOMES:
            username = nome.lower().replace(" ", ".") + str(random.randint(10, 99))
            balance = round(random.uniform(0, 50000), 2)
            user = User(
                id=uuid.uuid4(),
                username=username,
                balance=balance,
                created_at=_random_date(365),
            )
            db.add(user)
            users.append(user)
        db.commit()
        print(f"  {len(users)} usuários inseridos.")

    existing_payments = db.query(Payment).count()
    if existing_payments >= 150:
        print(f"Pagamentos já existem ({existing_payments} registros) — pulando seed de pagamentos.")
        return

    print("Inserindo 150 pagamentos...")
    payments_to_add = 150 - existing_payments
    for _ in range(payments_to_add):
        user = random.choice(users)
        provider = random.choices(PROVIDERS, weights=PROVIDER_WEIGHTS, k=1)[0]
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]

        # boleto e ted não têm chargeback
        if status == "chargeback" and provider in ("boleto", "ted", "pix"):
            status = "reembolsado"

        payment = Payment(
            id=uuid.uuid4(),
            user_id=user.id,
            amount=_random_amount(),
            status=status,
            provider=provider,
            created_at=_random_date(90),
        )
        db.add(payment)

    db.commit()
    print("  150 pagamentos inseridos.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    print("\nSeed do banco concluído.")
