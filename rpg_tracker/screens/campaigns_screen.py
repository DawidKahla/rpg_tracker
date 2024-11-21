from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemLeadingIcon,
)
from kivymd.uix.scrollview import MDScrollView
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Campaign  # do not use there direct


class CampaignScreen(MDScreen):
    def __init__(self, navigation=None, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.navigation = navigation
        self.build_ui()

    def build_ui(self):
        scroll_view = MDScrollView()
        self.list_view = MDList()
        scroll_view.add_widget(self.list_view)
        self.add_widget(scroll_view)

    def on_enter(self):
        self.populate_campaign_list()

    def populate_campaign_list(self):
        self.list_view.clear_widgets()

        campaigns = self.session.query(Campaign).all()

        for campaign in campaigns:
            item = MDListItem(
                MDListItemLeadingIcon(icon=campaign.icon),
                MDListItemHeadlineText(text=campaign.name),
                MDListItemSupportingText(text=f"System: {campaign.system}"),
                MDListItemSupportingText(text=f"Start: {campaign.start_date}"),
                on_release=lambda x, c=campaign: self.open_calendar(c.id),
            )
            self.list_view.add_widget(item)

    def open_calendar(self, campaign_id):
        if self.navigation:
            self.navigation.set_campaign(campaign_id)
            self.navigation.switch_to_screen("calendar_screen")
        else:
            raise ValueError("Navigation manager is not set!")
