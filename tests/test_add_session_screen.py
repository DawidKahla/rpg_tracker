import unittest
from unittest.mock import MagicMock, patch
from kivymd.app import MDApp
from rpg_tracker.screens.add_session_screen import AddSessionScreen
from datetime import datetime, date


class TestApp(MDApp):
    def build(self):
        return None


class TestAddSessionScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()

    @classmethod
    def tearDownClass(cls):
        cls.app.stop()

    def setUp(self):
        self.mock_navigation = MagicMock()
        self.screen = AddSessionScreen(navigation=self.mock_navigation)

    def test_initialization(self):
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.navigation, self.mock_navigation)
        self.assertEqual(self.screen.selected_date, date.today())

    def test_on_enter_with_navigation(self):
        self.mock_navigation.get_campaign.return_value = 1
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value.name = "Campaign Name"
        self.screen.session.query = MagicMock(return_value=mock_query)

        self.screen.on_enter()

        self.mock_navigation.get_campaign.assert_called_once()
        self.assertEqual(self.screen.title_label.text, "Add Session to Campaign Name")

    def test_on_enter_without_navigation(self):
        self.screen.navigation = None
        self.screen.on_enter()

        # Tytuł pozostaje niezmieniony, ponieważ brak navigation
        self.assertEqual(self.screen.title_label.text, "Add Session")

    def test_go_back(self):
        self.screen.go_back()
        self.mock_navigation.switch_to_screen.assert_called_once_with("calendar_screen")

    def test_open_date_picker(self):
        with patch(
            "rpg_tracker.screens.add_session_screen.MDDockedDatePicker"
        ) as MockDatePicker:
            mock_date_picker = MockDatePicker.return_value
            self.screen.open_date_picker()

            mock_date_picker.bind.assert_called_once_with(on_ok=self.screen.on_ok)
            mock_date_picker.open.assert_called_once()

    def test_on_ok(self):
        mock_date_picker = MagicMock()
        mock_date_picker.get_date.return_value = [datetime(2024, 11, 20).date()]

        self.screen.date_button = MagicMock(children=[MagicMock()])
        self.screen.on_ok(mock_date_picker)

        self.assertEqual(self.screen.selected_date, datetime(2024, 11, 20).date())
        self.assertEqual(
            self.screen.date_button.children[0].text, "Selected Date: 2024-11-20"
        )
        mock_date_picker.dismiss.assert_called_once()

    def test_save_session_with_date(self):
        self.screen.selected_date = datetime(2024, 11, 20).date()
        self.mock_navigation.get_campaign.return_value = 1
        self.screen.title_input = MagicMock(text="Session Title")
        self.screen.notes_input = MagicMock(text="Session Notes")
        self.screen.session = MagicMock()

        self.screen.save_session()

        self.screen.session.add.assert_called_once()
        self.screen.session.commit.assert_called_once()
        self.mock_navigation.switch_to_screen.assert_called_once_with("calendar_screen")

        # Sprawdź dane sesji, które zostały dodane
        added_session = self.screen.session.add.call_args[0][0]
        self.assertEqual(added_session.session_date, datetime(2024, 11, 20).date())
        self.assertEqual(added_session.title, "Session Title")
        self.assertEqual(added_session.notes, "Session Notes")

    def test_on_leave_resets_fields(self):
        self.screen.title_input = MagicMock(text="Some Title")
        self.screen.notes_input = MagicMock(text="Some Notes")
        self.screen.selected_date = None
        self.screen.date_button = MagicMock(children=[MagicMock(text="Selected Date")])

        self.screen.on_leave()

        self.assertEqual(self.screen.title_input.text, "")
        self.assertEqual(self.screen.notes_input.text, "")
        self.assertEqual(self.screen.selected_date, date.today())
        self.assertEqual(self.screen.date_button.children[0].text, "Select Date")
