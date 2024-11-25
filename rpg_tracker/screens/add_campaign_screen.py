from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Campaign
from datetime import date
from rpg_tracker.resources.icons import ICONS


class AddCampaignScreen(MDScreen):
    def __init__(self, navigation=None, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.navigation = navigation
        self.selected_date = date.today()
        self.icon = "dice-d20-outline"  # Default icon
        self.build_ui()

    def build_ui(self, *args):
        layout = MDGridLayout(cols=1, padding=20, spacing=20)

        # Navigation Bar
        self.nav_bar = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=50
        )
        back_button = MDIconButton(icon="arrow-left", on_release=self.go_back)
        self.nav_bar.add_widget(back_button)

        self.title_label = MDLabel(text="Add Campaign", halign="center")
        self.nav_bar.add_widget(self.title_label)
        layout.add_widget(self.nav_bar)

        # Campaign Name Input
        self.name_input = MDTextField(
            MDTextFieldHintText(text="Campaign Name"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.name_input)

        # Campaign System Input
        self.system_input = MDTextField(
            MDTextFieldHintText(text="System"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.system_input)

        # Notes Input
        self.notes_input = MDTextField(
            MDTextFieldHintText(text="Notes (optional)"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            multiline=True,
        )
        layout.add_widget(self.notes_input)

        # Date Picker Button
        self.date_button = MDButton(
            MDButtonText(text="Select Start Date"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            on_release=self.open_date_picker,
        )
        layout.add_widget(self.date_button)

        # Icon Picker Button
        self.icon_button = MDButton(
            MDButtonText(text="Select Icon"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            on_release=self.open_icon_picker,
        )
        layout.add_widget(self.icon_button)

        # Save Button
        save_button = MDButton(
            MDButtonText(text="Save Campaign"),
            pos_hint={"center_x": 0.5},
            on_release=self.save_campaign,
        )
        layout.add_widget(save_button)

        self.add_widget(layout)

    def go_back(self, *args):
        self.navigation.switch_to_screen("campaign_screen")

    def open_date_picker(self, *args):
        date_picker = MDDockedDatePicker(mark_today=True)
        date_picker.bind(on_ok=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance_date_picker):
        self.selected_date = instance_date_picker.get_date()[0]
        self.date_button.children[0].text = f"Start Date: {self.selected_date}"
        instance_date_picker.dismiss()

    def open_icon_picker(self, *args):
        icons = [
            {
                "text": icon,
                "leading_icon": icon,
                "on_release": lambda x=icon: self.set_icon(x),
            }
            for icon in ICONS
        ]
        self.icon_menu = MDDropdownMenu(caller=self.icon_button, items=icons)
        self.icon_menu.open()

    def set_icon(self, icon_name):
        self.icon = icon_name
        self.icon_button.children[0].text = f"Icon: {icon_name}"
        self.icon_menu.dismiss()

    def save_campaign(self, *args):
        if not self.name_input.text or not self.system_input.text:
            dialog = MDDialog(
                MDDialogHeadlineText(text="Name and System are required."),
                MDDialogButtonContainer(
                    MDButton(
                        MDButtonText(text="OK"),
                        on_release=lambda x: dialog.dismiss(),
                    ),
                ),
            )
            dialog.open()
            return

        campaign = Campaign(
            name=self.name_input.text or "Unknown Campaign",
            system=self.system_input.text or "Unknown System",
            start_date=self.selected_date,
            notes=self.notes_input.text or None,
            icon=self.icon,
        )
        self.session.add(campaign)
        self.session.commit()
        self.navigation.switch_to_screen("campaign_screen")

    def on_leave(self, *args):
        self.name_input = ""
        self.selected_date = date.today()
        self.system_input.text = ""
        self.notes_input.text = ""
        self.icon = "dice-d20-outline"
