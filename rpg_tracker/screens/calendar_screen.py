from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
)
from kivymd.uix.scrollview import MDScrollView
from database.db_setup import SessionLocal
from database.models import Session


class CalendarScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.selected_campaign_id = None
        self.build_ui()

    def build_ui(self):
        scroll_view = MDScrollView()
        self.list_view = MDList()
        scroll_view.add_widget(self.list_view)
        self.add_widget(scroll_view)

    def on_enter(self):
        if self.selected_campaign_id is not None:
            self.get_sessions(self.selected_campaign_id)

    def get_sessions(self, campaign_id):
        self.list_view.clear_widgets()

        sessions = self.session.query(Session).filter(
            Session.campaign_id == campaign_id
        )

        for session in sessions:

            item = MDListItem(
                MDListItemHeadlineText(text=session.title),
                MDListItemSupportingText(text=str(session.session_date)),
                on_release=lambda x, s=session: self.open_campaign(s),
            )
            self.list_view.add_widget(item)

    def open_campaign(self, session):
        print(f"Opening session: {session.title}")
