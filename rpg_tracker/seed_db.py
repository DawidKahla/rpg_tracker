from datetime import date
from database.db_setup import SessionLocal, init_db
from database.models import Campaign

# Inicjalizacja bazy danych
init_db()


# Funkcja do dodawania danych
def seed_campaigns():
    session = SessionLocal()

    # Sprawdzenie, czy tabela nie jest już wypełniona
    if not session.query(Campaign).first():
        # Dodanie przykładowych danych (zmiana dat na obiekty typu `date`)
        campaigns = [
            Campaign(name="Kampania 1", system="D&D 5e", start_date=date(2024, 1, 1)),
            Campaign(
                name="Kampania 2", system="Warhammer 4e", start_date=date(2024, 2, 15)
            ),
            Campaign(
                name="Kampania 3", system="Cyberpunk Red", start_date=date(2024, 3, 10)
            ),
            Campaign(
                name="Kampania 4", system="Pathfinder 2e", start_date=date(2024, 4, 20)
            ),
            Campaign(
                name="Kampania 5",
                system="Call of Cthulhu",
                start_date=date(2024, 5, 25),
            ),
        ]
        session.add_all(campaigns)
        session.commit()
        print("Tabela 'Campaigns' została wypełniona przykładami!")
    else:
        print("Tabela 'Campaigns' już zawiera dane.")

    session.close()


# Wywołanie funkcji
if __name__ == "__main__":
    seed_campaigns()
