from datetime import date
from database.db_setup import SessionLocal, init_db
from database.models import Campaign, Session

# Inicjalizacja bazy danych
init_db()


# Funkcja do dodawania danych
def seed_campaigns():
    session = SessionLocal()

    # Sprawdzenie, czy tabela nie jest już wypełniona
    if not session.query(Campaign).first():
        # Dodanie przykładowych danych (zmiana dat na obiekty typu `date`)
        campaigns = [
            Campaign(
                name="Campaign 1",
                system="D&D 5e",
                start_date=date(2024, 1, 1),
            ),
            Campaign(
                icon="sword",
                name="Campaign 2",
                system="Warhammer 4e",
                start_date=date(2024, 2, 15),
            ),
            Campaign(
                name="Campaign 3", system="Cyberpunk Red", start_date=date(2024, 3, 10)
            ),
            Campaign(
                icon="wizard-hat",
                name="Campaign 4",
                system="Pathfinder 2e",
                start_date=date(2024, 4, 20),
            ),
            Campaign(
                icon="skull",
                name="Campaign 5",
                system="Call of Cthulhu",
                start_date=date(2024, 5, 25),
            ),
        ]
        session.add_all(campaigns)
        session.commit()
        print("The 'campaigns' table has been populated with examples.")
    else:
        print("The 'campaigns' table already contains data.")

    session.close()


def seed_sessions():
    session = SessionLocal()

    # Sprawdzenie, czy tabela nie jest już wypełniona
    if not session.query(Session).first():
        # Dodanie przykładowych danych (zmiana dat na obiekty typu `date`)
        sessions = [
            Session(
                title="Example session title 1",
                session_date=date(2024, 1, 1),
                campaign_id=1,
            ),
            Session(
                title="Example session title 2",
                session_date=date(2024, 2, 1),
                campaign_id=1,
            ),
            Session(
                title="Example session title 3",
                session_date=date(2024, 2, 12),
                campaign_id=2,
            ),
            Session(
                title="Example session title 4",
                session_date=date(2024, 3, 14),
                campaign_id=1,
            ),
            Session(
                title="Example session title 5",
                session_date=date(2024, 5, 16),
                campaign_id=3,
            ),
            Session(
                title="Example session title 6",
                session_date=date(2024, 5, 21),
                campaign_id=1,
            ),
            Session(
                title="Example session title 7",
                session_date=date(2024, 5, 30),
                campaign_id=4,
            ),
            Session(
                title="Example session title 8",
                session_date=date(2024, 6, 1),
                campaign_id=1,
            ),
            Session(
                title="Example session title 9",
                session_date=date(2024, 6, 10),
                campaign_id=5,
            ),
            Session(
                title="Example session title 10",
                session_date=date(2024, 6, 21),
                campaign_id=2,
            ),
            Session(
                title="Example session title 11",
                session_date=date(2024, 7, 20),
                campaign_id=3,
            ),
        ]
        session.add_all(sessions)
        session.commit()
        print("The 'sessions' table has been populated with examples.")
    else:
        print("The 'sessions' table already contains data.")

    session.close()


# Wywołanie funkcji
if __name__ == "__main__":
    seed_campaigns()
    seed_sessions()
