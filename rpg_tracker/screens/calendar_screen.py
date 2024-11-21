from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
)
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Session, Campaign


class CalendarScreen(MDScreen):
    def __init__(self, navigation=None, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.navigation = navigation
        self.build_ui()

    def build_ui(self):
        scroll_view = MDScrollView()
        self.list_view = MDList()
        scroll_view.add_widget(self.list_view)
        layout = MDBoxLayout(orientation="vertical")
        self.nav_bar = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=50
        )
        back_button = MDIconButton(icon="arrow-left", on_release=self.go_back)
        self.nav_bar.add_widget(back_button)
        self.title = MDLabel(text="default", halign="left")
        self.nav_bar.add_widget(self.title)
        layout.add_widget(self.nav_bar)
        layout.add_widget(scroll_view)
        self.add_widget(layout)

    def on_enter(self):
        if self.navigation:
            campaign_id = self.navigation.get_campaign()
            self.get_sessions(campaign_id)
        else:
            print("No campaign selected")

    def get_sessions(self, campaign_id):
        self.list_view.clear_widgets()
        self.nav_bar.remove_widget(self.title)

        sessions = self.session.query(Session).filter(
            Session.campaign_id == campaign_id
        )

        for session in sessions:

            item = MDListItem(
                MDListItemHeadlineText(text=session.title),
                MDListItemSupportingText(text=str(session.session_date)),
                on_release=lambda x, s=session: self.open_session(s),
            )
            self.list_view.add_widget(item)
        title = self.session.query(Campaign).filter(Campaign.id == campaign_id)[0].name
        self.title = MDLabel(text=title, halign="center")
        self.nav_bar.add_widget(self.title)

    def open_session(self, session_id):
        print(f"Fetching session: {session_id}")

    def go_back(self, *args):
        self.navigation.switch_to_screen("campaign_screen")
