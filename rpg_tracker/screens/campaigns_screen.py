from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    MDListItem,
    MDListItemHeadlineText,
    MDListItemSupportingText,
    MDListItemLeadingIcon,
    MDListItemTrailingIcon,
)
from kivymd.uix.scrollview import MDScrollView
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Campaign
from kivymd.uix.button import MDFabButton, MDIconButton, MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivy.uix.widget import Widget


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
        fab_button = MDFabButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            # on_release=
        )
        self.add_widget(fab_button)

    def on_enter(self):
        self.populate_campaign_list()

    def populate_campaign_list(self):
        self.list_view.clear_widgets()

        campaigns = self.session.query(Campaign).all()

        for campaign in campaigns:
            item_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None)

            item = MDListItem(
                MDListItemLeadingIcon(icon=campaign.icon),
                MDListItemHeadlineText(
                    text=campaign.name,
                    on_release=lambda x: self.open_calendar(campaign.id),
                ),
                MDListItemSupportingText(text=f"System: {campaign.system}"),
                MDListItemSupportingText(text=f"Start: {campaign.start_date}"),
                MDListItemTrailingIcon(
                    icon="trash-can",
                    on_release=lambda x: self.confirm_delete_campaign(campaign),
                ),
            )
            item_layout.add_widget(item)

            delete_button = MDIconButton(
                icon="trash-can",
                on_release=lambda x: self.confirm_delete_campaign(campaign),
            )
            item_layout.add_widget(delete_button)

            self.list_view.add_widget(item_layout)

    def open_calendar(self, campaign_id):
        if self.navigation:
            self.navigation.set_campaign(campaign_id)
            self.navigation.switch_to_screen("calendar_screen")
        else:
            raise ValueError("Navigation manager is not set!")

    def delete_campaign(self, cam):
        self.session.delete(cam)
        self.session.commit()
        self.on_enter()

    def confirm_delete_campaign(self, campaign):
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=f"Are you sure you want to delete the session '{campaign.name}'?"
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="DELETE"),
                    on_release=lambda x: self.delete_campaign(campaign),
                ),
                MDButton(
                    MDButtonText(text="CANCEL"),
                    on_release=lambda x: self.dismiss_dialog(),
                ),
                spacing=20,
            ),
        )
        self.dialog.open()
