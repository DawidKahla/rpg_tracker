import unittest
from unittest.mock import MagicMock
from kivymd.app import MDApp
from rpg_tracker.screens.campaigns_screen import CampaignScreen


class TestApp(MDApp):
    def build(self):
        return None


class TestCampaignScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()

    @classmethod
    def tearDownClass(cls):
        cls.app.stop()

    def setUp(self):
        """Set up a CampaignScreen instance with mocked dependencies."""
        self.mock_navigation = MagicMock()
        self.mock_session = MagicMock()
        self.screen = CampaignScreen(navigation=self.mock_navigation)
        self.screen.session = self.mock_session

    def test_initialization(self):
        """Test that the CampaignScreen initializes correctly."""
        self.assertIsNotNone(self.screen)
        self.assertEqual(self.screen.navigation, self.mock_navigation)

    def test_build_ui(self):
        """Test that the UI is built correctly."""
        self.screen.build_ui()
        print(len(self.screen.children))
        self.assertEqual(len(self.screen.children), 2)
        print(len(self.screen.children))

    def test_on_enter_calls_populate_campaign_list(self):
        """Test that `on_enter` calls `populate_campaign_list`."""
        self.screen.populate_campaign_list = MagicMock()
        self.screen.on_enter()
        self.screen.populate_campaign_list.assert_called_once()

    def test_populate_campaign_list_with_campaigns(self):
        """Test that campaigns are populated in the list."""
        mock_campaigns = MagicMock(
            name="Campaign2", icon="star", system="sys2", start_date="2024, 1, 2"
        )

        self.screen.session.query().all.return_value = mock_campaigns

        self.screen.list_view = MagicMock()
        self.screen.populate_campaign_list()

        self.assertEqual(
            self.screen.list_view.add_widget.call_count,
            len(mock_campaigns),
            "Number of added widgets should match the number of campaigns.",
        )

    def test_populate_campaign_list_with_no_campaigns(self):
        """Test that no widgets are added when there are no campaigns."""
        self.screen.session.query().all.return_value = []

        self.screen.list_view = MagicMock()
        self.screen.populate_campaign_list()

        self.screen.list_view.add_widget.assert_not_called()

    def test_open_calendar_calls_navigation(self):
        """Test that `open_calendar` switches to the calendar screen."""
        self.screen.open_calendar(1)
        self.mock_navigation.switch_to_screen.assert_called_once_with("calendar_screen")
