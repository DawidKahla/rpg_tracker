from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition


class NavigationManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_campaign_id = None

    def switch_to_screen(self, screen_name):
        """
        Przełącza na ekran o podanej nazwie.
        """
        self.transition = SlideTransition(direction="right")
        if screen_name in self.screen_names:
            self.current = screen_name
        else:
            raise ValueError(f"Ekran {screen_name} nie został zarejestrowany.")

    def set_campaign(self, campaign_id):
        self.current_campaign_id = campaign_id

    def get_campaign(self):
        return self.current_campaign_id
