from datetime import date
from rpg_tracker.database.db_setup import SessionLocal, init_db
from rpg_tracker.database.models import Campaign, Session, Hero

init_db()


def seed_campaigns():
    session = SessionLocal()

    if not session.query(Campaign).first():
        campaigns = [
            Campaign(
                name="Campaign 1",
                system="D&D 5e",
                start_date=date(2024, 1, 1),
                notes="Nothing special",
            ),
            Campaign(
                icon="sword",
                name="Campaign 2",
                system="Warhammer 4e",
                start_date=date(2024, 2, 15),
            ),
            Campaign(
                name="Campaign 3",
                system="Cyberpunk Red",
                start_date=date(2024, 3, 10),
                notes="Bugged system",
            ),
            Campaign(
                icon="wizard-hat",
                name="Campaign 4",
                system="Pathfinder 2e",
                start_date=date(2024, 4, 20),
                notes="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
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

    if not session.query(Session).first():
        sessions = [
            Session(
                title="Example session title 1",
                session_date=date(2024, 1, 1),
                campaign_id=1,
                notes="aaaaaa",
            ),
            Session(
                title="Example session title 2",
                session_date=date(2024, 2, 1),
                campaign_id=1,
                notes="bbbbbbb",
            ),
            Session(
                title="Example session title 3",
                session_date=date(2024, 2, 12),
                campaign_id=2,
                notes="PoKeMoN fOnT",
            ),
            Session(
                title="Example session title 4",
                session_date=date(2024, 3, 14),
                campaign_id=1,
                notes="ccccccccccccccccccc",
            ),
            Session(
                title="Example session title 5",
                session_date=date(2024, 5, 16),
                campaign_id=3,
                notes="veni, vidi, vici",
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
                notes="example note",
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
                notes="something",
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


def seed_heroes():
    session = SessionLocal()

    if not session.query(Hero).first():
        heroes = [
            Hero(
                campaign_id=1,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=2,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=3,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
                status="retired",
            ),
            Hero(
                campaign_id=4,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=5,
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=2,
                icon="star",
                name="name and surname",
                notes="nothing left to say now",
                status="dead",
            ),
            Hero(
                campaign_id=3,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=4,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=5,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=3,
                icon="sword-cross",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=4,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
            Hero(
                campaign_id=4,
                icon="sword",
                name="name and surname",
                notes="nothing left to say now",
            ),
        ]
        session.add_all(heroes)
        session.commit()
        print("The 'heroes' table has been populated with examples.")
    else:
        print("The 'heroes' table already contains data.")

    session.close()


# Wywołanie funkcji
if __name__ == "__main__":
    seed_campaigns()
    seed_sessions()
    seed_heroes()
