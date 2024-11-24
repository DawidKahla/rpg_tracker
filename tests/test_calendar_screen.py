import unittest
from unittest.mock import MagicMock, patch
from kivymd.app import MDApp
from rpg_tracker.screens.calendar_screen import CalendarScreen
from kivymd.uix.list import MDList
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFabButton
from kivymd.uix.boxlayout import MDBoxLayout


class TestApp(MDApp):
    def build(self):
        return None


class TestCalendarScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()

    @classmethod
    def tearDownClass(cls):
        cls.app.stop()

    def setUp(self):
        self.mock_navigation = MagicMock()
        self.screen = CalendarScreen(navigation=self.mock_navigation)

    def test_initialization(self):
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.navigation, self.mock_navigation)

    def test_build_ui_creates_correct_structure(self):
        calendar_screen = CalendarScreen()
        calendar_screen.build_ui()

        root_layout = calendar_screen.children[0]
        assert isinstance(root_layout, MDBoxLayout)

        # Sprawdzenie elementów w głównym layout
        assert len(root_layout.children) == 3  # FAB button, ScrollView, NavBar

        # Sprawdzenie NavBar
        nav_bar = root_layout.children[2]
        assert isinstance(nav_bar, MDBoxLayout)
        assert len(nav_bar.children) == 3

        # Sprawdzenie FAB buttona
        fab_button = root_layout.children[0]
        assert isinstance(fab_button, MDFabButton)
        assert fab_button.icon == "plus"

        # Sprawdzenie ScrollView
        scroll_view = root_layout.children[1]
        assert isinstance(scroll_view, MDScrollView)
        assert isinstance(scroll_view.children[0], MDList)
        assert calendar_screen.list_view == scroll_view.children[0]

    def test_get_sessions_no_sessions(self):
        screen = CalendarScreen()
        screen.list_view = MDList()
        screen.session = MagicMock()
        screen.session.query().filter.return_value = []
        screen.get_sessions(campaign_id=1)
        self.assertEqual(len(screen.list_view.children), 0)

    def test_on_enter_with_navigation(self):
        self.mock_navigation.get_campaign.return_value = 1
        self.screen.get_sessions = MagicMock()

        self.screen.on_enter()

        self.mock_navigation.get_campaign.assert_called_once()
        self.screen.get_sessions.assert_called_once_with(1)

    def test_on_enter_without_navigation(self):
        self.screen.navigation = None
        with patch("builtins.print") as mock_print:
            self.screen.on_enter()
            mock_print.assert_called_with("No campaign selected")

    def test_go_back(self):
        self.screen.go_back()
        self.mock_navigation.switch_to_screen.assert_called_once_with("campaign_screen")

    def test_open_session(self):
        with patch("builtins.print") as mock_print:
            self.screen.open_session(23)
            mock_print.assert_called_once_with("Fetching session: 23")
