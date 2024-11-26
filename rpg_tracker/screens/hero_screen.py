from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFabButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from rpg_tracker.database.db_setup import SessionLocal
from rpg_tracker.database.models import Hero, Campaign


class HeroScreen(MDScreen):
    def __init__(self, navigation=None, **kwargs):
        super().__init__(**kwargs)
        self.session = SessionLocal()
        self.navigation = navigation
        self.menu = None
        self.build_ui()

    def build_ui(self):
        # Scrollable list of heroes
        scroll_view = MDScrollView()
        self.hero_list = MDBoxLayout(
            orientation="vertical", spacing=10, padding=10, size_hint_y=None
        )
        self.hero_list.bind(minimum_height=self.hero_list.setter("height"))
        scroll_view.add_widget(self.hero_list)

        # Navigation bar
        self.nav_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
        )

        # Back button
        back_button = MDIconButton(icon="arrow-left", on_release=self.go_back)
        left_anchor = MDBoxLayout(size_hint=(None, None), width=50)
        left_anchor.add_widget(back_button)

        # Title
        self.title = MDLabel(text="Campaign Heroes", halign="center", valign="center")
        center_anchor = MDBoxLayout(size_hint=(1, 1))
        center_anchor.add_widget(self.title)

        # Dropdown menu button
        menu_button = MDIconButton(icon="menu", on_release=self.open_menu)
        right_anchor = MDBoxLayout(size_hint=(None, None), width=50)
        right_anchor.add_widget(menu_button)

        self.nav_bar.add_widget(left_anchor)
        self.nav_bar.add_widget(center_anchor)
        self.nav_bar.add_widget(right_anchor)

        # Add the dropdown menu
        self.menu = MDDropdownMenu(
            items=[
                {
                    "text": "Calendar",
                    "on_release": lambda: self.switch_to_screen_from_menu(
                        "calendar_screen"
                    ),
                },
                {
                    "text": "Edit Campaign",
                    "on_release": lambda: self.switch_to_screen_from_menu(
                        "edit_campaign_screen"
                    ),
                },
            ],
            width_mult=4,
        )

        # Layout for the entire screen
        layout = MDBoxLayout(orientation="vertical")
        layout.add_widget(self.nav_bar)
        layout.add_widget(scroll_view)

        # Add button
        fab_button = MDFabButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self.add_hero,
        )
        layout.add_widget(fab_button)

        self.add_widget(layout)

    def on_enter(self):
        if self.navigation:
            campaign_id = self.navigation.get_campaign()
            self.load_heroes(campaign_id)
        else:
            print("No campaign selected")

    def load_heroes(self, campaign_id):
        self.hero_list.clear_widgets()

        # Fetch heroes for the selected campaign
        heroes = self.session.query(Hero).filter(Hero.campaign_id == campaign_id)
        for hero in heroes:
            card = self.create_hero_card(hero)
            self.hero_list.add_widget(card)

        # Update campaign name in the title
        campaign = (
            self.session.query(Campaign).filter(Campaign.id == campaign_id).first()
        )
        if campaign:
            self.title.text = f"Heroes of {campaign.name}"

    def create_hero_card(self, hero):
        card = MDCard(
            size_hint=(1, None),
            height=80,
            padding=10,
            orientation="horizontal",
        )
        text_layout = MDBoxLayout(orientation="vertical", size_hint=(0.8, 1))
        text_layout.add_widget(MDLabel(text=hero.name, halign="left"))
        text_layout.add_widget(MDLabel(text=f"Status: {hero.status}", halign="left"))

        delete_button = MDIconButton(
            icon="trash-can-outline",
            size_hint=(0.2, 1),
            on_release=lambda x: self.confirm_delete_hero(hero),
        )

        card.add_widget(text_layout)
        card.add_widget(delete_button)
        return card

    def edit_hero(self, hero):
        # Navigate to the edit_hero_screen with the hero's ID
        print(f"Editing hero: {hero.name}")
        self.navigation.set_hero(hero.id)
        self.navigation.switch_to_screen("edit_hero_screen")

    def confirm_delete_hero(self, hero):
        # Confirmation dialog for deleting a hero
        dialog = MDDialog(
            title="Delete Hero",
            text=f"Are you sure you want to delete {hero.name}?",
            buttons=[
                MDIconButton(text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDIconButton(
                    text="Delete",
                    on_release=lambda x: self.delete_hero(hero, dialog),
                ),
            ],
        )
        dialog.open()

    def delete_hero(self, hero, dialog):
        # Remove the hero from the database
        dialog.dismiss()
        self.session.delete(hero)
        self.session.commit()
        self.on_enter()  # Reload heroes after deletion

    def add_hero(self, *args):
        # Navigate to the add_hero_screen
        self.navigation.switch_to_screen("add_hero_screen")

    def go_back(self, *args):
        # Navigate back to the campaigns_screen
        self.navigation.switch_to_screen("campaigns_screen")

    def open_menu(self, button):
        self.menu.caller = button
        self.menu.open()

    def switch_to_screen_from_menu(self, screen_name):
        self.menu.dismiss()
        self.navigation.switch_to_screen(screen_name)

    def on_leave(self):
        self.hero_list.clear_widgets()
