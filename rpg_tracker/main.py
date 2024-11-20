from kivymd.app import MDApp
from screens.campaigns_screen import CampaignScreen
from screens.calendar_screen import CalendarScreen
from database.db_setup import init_db
from navigation_manager import NavigationManager


class RPGTrackerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        init_db()
        self.navigation_manager = NavigationManager()

        # Rejestrujemy ekrany
        self.navigation_manager.add_widget(
            CampaignScreen(name="campaign_screen", navigation=self.navigation_manager)
        )
        self.navigation_manager.add_widget(
            CalendarScreen(name="calendar_screen", navigation=self.navigation_manager)
        )

        return self.navigation_manager

    def open_calendar(self, campaign_id):
        # Przekazanie campaign_id do calendar_screen
        self.calendar_screen.selected_campaign_id = campaign_id
        self.screen_manager.current = "calendar_screen"


if __name__ == "__main__":
    RPGTrackerApp().run()
