from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemTertiaryText,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp


class CampaignListPrototype(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        layout = MDBoxLayout(orientation="vertical")
        scroll = MDScrollView()
        self.container = MDList()
        scroll.add_widget(self.container)
        layout.add_widget(scroll)
        return layout

    def on_start(self):
        self.add_campaign(
            icon="sword",
            headline_text="Kampania 1",
            supporting_text="System 1",
            tertiary_text="Data rozpoczęcia",
        )
        self.add_campaign(
            icon="sword-cross",
            headline_text="Kampania 2",
            supporting_text="System 2",
            tertiary_text="Data rozpoczęcia",
        )
        self.add_campaign(
            icon="shield-crown",
            headline_text="Kampania 3",
            supporting_text="System 3",
            tertiary_text="Data rozpoczęcia",
        )

    def add_campaign(self, icon, headline_text, supporting_text, tertiary_text):
        item = MDListItem(
            MDListItemLeadingIcon(icon=icon),
            MDListItemHeadlineText(text=headline_text),
            MDListItemSupportingText(text=supporting_text),
            MDListItemTertiaryText(text=tertiary_text),
        )
        self.container.add_widget(item)


CampaignListPrototype().run()
