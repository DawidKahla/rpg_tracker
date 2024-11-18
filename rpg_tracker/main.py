from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens.campaigns_screen import CampaignScreen
from screens.calendar_screen import CalendarScreen
from database.db_setup import init_db


class RPGTrackerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        init_db()

        self.screen_manager = MDScreenManager()
        self.campaign_screen = CampaignScreen(name="campaign_list")
        self.calendar_screen = CalendarScreen(name="calendar_screen")

        # Przechodzenie między ekranami
        self.screen_manager.add_widget(self.campaign_screen)
        self.screen_manager.add_widget(self.calendar_screen)

        # Przekazanie referencji do metod nawigacji
        self.campaign_screen.open_calendar = self.open_calendar

        return self.screen_manager

    def open_calendar(self, campaign_id):
        # Przekazanie campaign_id do calendar_screen
        self.calendar_screen.selected_campaign_id = campaign_id
        self.screen_manager.current = "calendar_screen"


if __name__ == "__main__":
    RPGTrackerApp().run()
