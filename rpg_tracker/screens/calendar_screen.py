from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItemHeadlineText,
    MDListItemSupportingText,
)
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from rpg_tracker.database.db_setup import SessionLocal


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

        nav_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            md_bg_color=self.theme_cls.primaryColor,
        )
        back_button = MDIconButton(
            icon="arrow-left", on_release=self.go_back, icon_color="green"
        )
        title = MDLabel(
            text="Calendar",
            halign="left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )
        nav_bar.add_widget(back_button)
        nav_bar.add_widget(title)

        layout.add_widget(nav_bar)
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

    def open_session(self, session_id):
        print(f"Fetching session: {session_id}")

    def go_back(self, *args):
        self.navigation.switch_to_screen("campaign_screen")
