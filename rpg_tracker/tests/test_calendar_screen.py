import unittest
from unittest.mock import MagicMock, patch
from kivymd.app import MDApp
from screens.calendar_screen import CalendarScreen
from database.models import Session
from kivymd.uix.list import MDListItem


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

    def test_build_ui(self):
        nav_bar = self.screen.children[0].children[1]
        self.assertEqual(
            len(nav_bar.children), 2, "Nav bar should have back button and title"
        )
        self.assertEqual(
            nav_bar.children[0].text, "Calendar", "Title should be 'Calendar'"
        )

    @patch("screens.calendar_screen.SessionLocal")
    def test_get_sessions(self, mock_db):
        """Testuje, czy sesje są poprawnie pobierane z bazy danych."""

        mock_session = MagicMock(spec=Session)
        mock_session.title = "Test Session"
        mock_session.session_date = "2024-01-01"

        mock_query = MagicMock()
        mock_query.filter.return_value = [mock_session]
        mock_db.return_value.query.return_value = mock_query

        mock_navigation = MagicMock()
        screen = CalendarScreen(navigation=mock_navigation)

        screen.list_view.clear_widgets = MagicMock()

        screen.get_sessions(campaign_id=1)

        screen.list_view.clear_widgets.assert_called_once()

        self.assertEqual(
            len(screen.list_view.children), 1, "List view should have one item"
        )

        list_item = screen.list_view.children[0]
        self.assertIsInstance(
            list_item, MDListItem, "First item should be of type MDListItem"
        )

    def test_on_enter_with_navigation(self):
        """Testuje, czy `on_enter` poprawnie wywołuje `get_sessions`."""
        self.mock_navigation.get_campaign.return_value = 1
        self.screen.get_sessions = MagicMock()

        self.screen.on_enter()

        self.mock_navigation.get_campaign.assert_called_once()
        self.screen.get_sessions.assert_called_once_with(1)

    def test_on_enter_without_navigation(self):
        """Testuje, czy `on_enter` obsługuje brak nawigacji."""
        self.screen.navigation = None
        with patch("builtins.print") as mock_print:
            self.screen.on_enter()
            mock_print.assert_called_with("No campaign selected")

    def test_go_back(self):
        """Testuje działanie przycisku powrotu."""
        self.screen.go_back()
        self.mock_navigation.switch_to_screen.assert_called_once_with("campaign_screen")

    def test_open_session(self):
        """Testuje działanie metody `open_session`."""
        with patch("builtins.print") as mock_print:
            self.screen.open_session(23)
            mock_print.assert_called_once_with("Fetching session: 23")