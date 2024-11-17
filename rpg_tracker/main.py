from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens.campaigns_screen import CampaignListScreen
from database.db_setup import init_db


class RPGTrackerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        # Inicjalizacja bazy danych
        init_db()

        # Menedżer ekranów
        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(CampaignListScreen(name="campaign_list"))
        return self.screen_manager


if __name__ == "__main__":
    RPGTrackerApp().run()
