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
from kivymd.uix.anchorlayout import MDAnchorLayout


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

        self.nav_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
        )

        back_button = MDIconButton(icon="arrow-left", on_release=self.go_back)
        left_anchor = MDAnchorLayout(anchor_x="left", anchor_y="center")
        left_anchor.add_widget(back_button)

        self.title = MDLabel(text="default", halign="center", valign="center")
        center_anchor = MDAnchorLayout(anchor_x="center", anchor_y="center")
        center_anchor.add_widget(self.title)

        add_button = MDIconButton(icon="plus", on_release=self.add_session)
        right_anchor = MDAnchorLayout(anchor_x="right", anchor_y="center")
        right_anchor.add_widget(add_button)

        self.nav_bar.add_widget(left_anchor)
        self.nav_bar.add_widget(center_anchor)
        self.nav_bar.add_widget(right_anchor)

        layout = MDBoxLayout(orientation="vertical")
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

        campaign = self.session.query(Campaign).filter(Campaign.id == campaign_id)

        if campaign:
            self.title.text = campaign.first().name

    def open_session(self, session_id):
        print(f"Fetching session: {session_id}")

    def go_back(self, *args):
        self.navigation.switch_to_screen("campaign_screen")

    def add_session(self, *args):
        self.navigation.switch_to_screen("add_session_screen")
