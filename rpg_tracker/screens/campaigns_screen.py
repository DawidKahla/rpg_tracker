from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
)
from kivymd.uix.scrollview import MDScrollView
from database.db_setup import SessionLocal
from database.models import Campaign


class CampaignListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
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
                MDListItemHeadlineText(text=campaign.name),
                MDListItemSupportingText(text=f"System: {campaign.system}"),
                MDListItemSupportingText(text=f"Start: {campaign.start_date}"),
                on_release=lambda x, c=campaign: self.open_campaign(c),
            )
            self.list_view.add_widget(item)

    def open_campaign(self, campaign):
        print(f"Otwieranie kampanii: {campaign.name}")
