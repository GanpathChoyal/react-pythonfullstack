from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Note


class SummaryEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="alice", password="pass123")
        self.other_user = User.objects.create_user(username="bob", password="pass123")
        self.note = Note.objects.create(title="Test note", content="Hello world", author=self.user)

    def test_user_can_get_summary_for_their_note(self):
        self.client.force_authenticate(self.user)

        with patch("api.views.summarize_text_with_gemini", return_value="Short summary") as mock_summary:
            response = self.client.get(f"/api/notes/{self.note.pk}/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"summary": "Short summary"})
        mock_summary.assert_called_once_with("Hello world")

    def test_falls_back_to_local_summary_when_gemini_is_unavailable(self):
        self.client.force_authenticate(self.user)

        with patch("api.views.summarize_text_with_gemini", side_effect=Exception("quota exceeded")):
            response = self.client.get(f"/api/notes/{self.note.pk}/summary/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["summary"], "API is not working right now. Please try again later.")
        self.assertTrue(response.json()["fallback"])

    def test_user_cannot_get_summary_for_other_users_note(self):
        other_note = Note.objects.create(title="Other", content="Secret", author=self.other_user)
        self.client.force_authenticate(self.user)

        response = self.client.get(f"/api/notes/{other_note.pk}/summary/")

        self.assertEqual(response.status_code, 404)
