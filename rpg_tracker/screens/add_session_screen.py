from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.label import MDLabel
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Session, Campaign
from kivymd.uix.gridlayout import MDGridLayout
from datetime import date


class AddSessionScreen(MDScreen):
    def __init__(self, navigation=None, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.navigation = navigation
        self.selected_date = date.today()
        self.date_button = None
        self.build_ui()

    def build_ui(self, *args):
        layout = MDGridLayout(cols=1, padding=20, spacing=20)

        self.nav_bar = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=50
        )
        back_button = MDIconButton(icon="arrow-left", on_release=self.go_back)
        self.nav_bar.add_widget(back_button)

        self.title_label = MDLabel(text="Add Session", halign="center")
        self.nav_bar.add_widget(self.title_label)
        layout.add_widget(self.nav_bar)

        # Input fields
        self.title_input = MDTextField(
            MDTextFieldHintText(text="Title (optional)"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.title_input)

        self.notes_input = MDTextField(
            MDTextFieldHintText(text="Notes (optional)"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            multiline=True,
        )
        layout.add_widget(self.notes_input)

        self.date_button = MDButton(
            MDButtonText(text="Select Date"),
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5},
            on_release=self.open_date_picker,
        )

        save_button = MDButton(
            MDButtonText(text="Save Session"),
            pos_hint={"center_x": 0.8},
            on_release=self.save_session,
        )
        button_layout = MDBoxLayout(
            height=50,
            spacing=20,
            size_hint_x=1,
            pos_hint={"center_x": 0.9},
        )
        layout.add_widget(self.date_button)
        button_layout.add_widget(save_button)

        self.add_widget(button_layout)
        self.add_widget(layout)

    def on_enter(self):
        if self.navigation:
            campaign_id = self.navigation.get_campaign()
            campaign_name = (
                self.session.query(Campaign)
                .filter(Campaign.id == campaign_id)
                .first()
                .name
            )
            self.title_label.text = f"Add Session to {campaign_name}"

    def go_back(self, *args):
        self.navigation.switch_to_screen("calendar_screen")

    def open_date_picker(self, *args):
        date_picker = MDDockedDatePicker(mark_today=False)
        date_picker.bind(on_ok=self.on_ok)
        date_picker.open()

    def on_ok(self, instance_date_picker):
        self.selected_date = instance_date_picker.get_date()[0]
        self.date_button.children[0].text = f"Selected Date: {self.selected_date}"
        instance_date_picker.dismiss()

    def save_session(self, *args):
        campaign_id = self.navigation.get_campaign()
        session = Session(
            campaign_id=campaign_id,
            session_date=self.selected_date,
            title=self.title_input.text or "Unknown Session",
            notes=self.notes_input.text or None,
        )
        self.session.add(session)
        self.session.commit()
        self.navigation.switch_to_screen("calendar_screen")

    def on_leave(self, *args):
        self.title_input.text = ""
        self.notes_input.text = ""
        self.selected_date = date.today()
        self.date_button.children[0].text = "Select Date"
