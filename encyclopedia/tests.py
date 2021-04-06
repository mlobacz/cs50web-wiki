"""
Encyclopedia app test suite.
"""

from unittest.mock import patch

import pytest
from django.test import TestCase
from django.urls import reverse


class ViewsTests(TestCase):
    """
    Tests for the encyclopedia views.
    """

    @patch("encyclopedia.util.list_entries")
    def test_index_lists_entries(self, list_entries_mock):
        """Index returns some entries in the contex.t"""
        response = self.client.get(reverse("encyclopedia:index"))
        assert response.status_code == 200
        assert list_entries_mock.called_once()
        assert response.context["entries"] is not None

    @patch("encyclopedia.util.get_entry")
    def test_show_entry(self, get_entry_mock):
        """Entry with requested title is returned."""
        get_entry_mock.return_value = "test_content"
        response = self.client.get(
            reverse("encyclopedia:entry", kwargs={"title": "test_title"})
        )
        assert response.status_code == 200
        assert get_entry_mock.called_once_with(title="test_title")
        assert response.context["entry"] is not None

    @patch("encyclopedia.util.get_entry")
    def test_show_entry_404(self, get_entry_mock):
        """404 is returned if there is no corresponding entry."""
        get_entry_mock.return_value = None
        response = self.client.get(
            reverse("encyclopedia:entry", kwargs={"title": "test_title"})
        )
        assert response.status_code == 404
        assert (
            response.context["exception"]
            == "test_title entry was not found in the Wiki."
        )

    @patch("encyclopedia.util.get_entry")
    def test_search_one_hit(self, get_entry_mock):
        """Search redirects to entry page on exact hit."""
        test_entry = "test_entry"
        response = self.client.get(reverse("encyclopedia:search"), {"q": test_entry})
        get_entry_mock.assert_called_once_with(test_entry)
        assert response.status_code == 302
        assert response.url == reverse(
            "encyclopedia:entry", kwargs={"title": test_entry}
        )

    @patch("encyclopedia.util.list_entries")
    def test_search_multiple_hits(self, list_entries_mock):
        """Search returns list of entries that match search string."""
        list_entries_mock.return_value=["entry_1", "entry_2"]
        test_entry_part = "try_1"
        response = self.client.get(
            reverse("encyclopedia:search"), {"q": test_entry_part}
        )
        assert response.status_code == 200
        assert response.context["entries"] == ["entry_1"]

    @patch("encyclopedia.util.list_entries")
    def test_new_entry_already_exsits(self, list_entries_mock):
        """Already exists error is raised on attempt to add duplicated entry."""
        from .views import AlreadyExistsError   # pylint: disable = C0415
        list_entries_mock.return_value=["entry_1", "entry_2"]
        with pytest.raises(AlreadyExistsError):
            self.client.post(
                reverse("encyclopedia:new"),
                {"title": "entry_1", "content": "test_content"},
            )

    @patch("encyclopedia.util.save_entry")
    def test_new_entry_saved(self, save_entry_mock):
        """New entry is saved with information from form."""
        response = self.client.post(
            reverse("encyclopedia:new"),
            {"title": "entry_1", "content": "test_content"},
        )
        save_entry_mock.assert_called_once_with(title="entry_1", content="test_content")
        assert response.status_code == 302
        assert response.url == reverse(
            "encyclopedia:entry", kwargs={"title": "entry_1"}
        )

    def test_new_entry_get_form(self):
        """Empty new entry form is returned on get request."""
        from .views import NewEntryForm     # pylint: disable = C0415
        response = self.client.get(reverse("encyclopedia:new"))
        assert response.status_code == 200
        assert isinstance(response.context["form"], NewEntryForm)

    @patch("encyclopedia.util.save_entry")
    def test_edit_entry(self, save_entry_mock):
        """Edited entry is saved with the values from form."""
        response = self.client.post(
            reverse("encyclopedia:edit", kwargs={"title": "entry_1"}),
            {"title": "entry_1", "content": "test_content"},
        )
        save_entry_mock.assert_called_once_with(title="entry_1", content="test_content")
        assert response.status_code == 302
        assert response.url == reverse(
            "encyclopedia:entry", kwargs={"title": "entry_1"}
        )

    def test_edit_entry_get(self):
        """Empty edit entry is returned on get request."""
        from .views import EditEntryForm    # pylint: disable = C0415
        response = self.client.get(reverse("encyclopedia:edit", kwargs={"title": "entry_1"}))
        assert response.status_code == 200
        assert isinstance(response.context["form"], EditEntryForm)
