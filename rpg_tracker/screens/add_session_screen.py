from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.pickers import MDDockedDatePicker
from kivymd.uix.label import MDLabel
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Session, Campaign
from kivymd.uix.gridlayout import MDGridLayout


class AddSessionScreen(MDScreen):
    def __init__(self, navigation=None, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.navigation = navigation
        self.selected_date = None
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
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.title_input)

        self.notes_input = MDTextField(
            MDTextFieldHintText(text="Notes (optional)"),
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            multiline=True,
        )
        layout.add_widget(self.notes_input)

        date_picker_button = MDButton(
            MDButtonText(text="Select Date"),
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            on_release=self.open_date_picker,
        )
        layout.add_widget(date_picker_button)

        save_button = MDButton(
            MDButtonText(text="Save Session"),
            size_hint_x=0.5,
            pos_hint={"center_x": 0.5},
            on_release=self.save_session,
        )
        layout.add_widget(save_button)

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
        self.clear_inputs()
        self.navigation.switch_to_screen("calendar_screen")

    def open_date_picker(self, *args):
        date_picker = MDDockedDatePicker(mark_today=False)
        date_picker.bind(on_ok=self.on_ok)
        date_picker.open()

    def on_ok(self, instance_date_picker):
        self.selected_date = instance_date_picker.get_date()[0]
        print(f"Wybrano datę: {self.selected_date}")
        instance_date_picker.dismiss()

    def save_session(self, *args):
        if not self.selected_date:
            print("Date is required.")
            return

        campaign_id = self.navigation.get_campaign()
        session = Session(
            campaign_id=campaign_id,
            session_date=self.selected_date,
            title=self.title_input.text or None,
            notes=self.notes_input.text or None,
        )
        self.session.add(session)
        self.session.commit()
        self.clear_inputs()
        self.navigation.switch_to_screen("calendar_screen")

    def clear_inputs(self, *args):
        self.title_input.text = ""
        self.notes_input.text = ""
        self.selected_date = None
