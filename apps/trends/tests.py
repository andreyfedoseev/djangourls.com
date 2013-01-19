from mock import MagicMock, PropertyMock, patch, call
from trends.utils import Untiny, URLFinder
import requests
import unittest


class UntinyTestCase(unittest.TestCase):

    def test_get_services(self):
        untiny = Untiny()
        mock_response = MagicMock()
        mock_response_text = PropertyMock(return_value=".tk, 1u.ro, 1url.com, 2pl.us")
        type(mock_response).text = mock_response_text

        with patch("requests.get", MagicMock(return_value=mock_response)) as mock_get:
            # A request is sent to untiny.me and a set of supported services is
            # returned
            self.assertEquals(
                untiny.get_services(),
                set([".tk", "1u.ro", "1url.com", "2pl.us"])
            )
            self.assertEquals(mock_get.call_count, 1)
            self.assertTrue(mock_response_text.called)

        with patch("requests.get", MagicMock(side_effect=requests.RequestException)) as mock_get:
            # If a request to untiny.me fails and empty set should be returned.
            self.assertEquals(untiny.get_services(), set())
            self.assertEquals(mock_get.call_count, 1)

    def test_is_tiny(self):
        untiny = Untiny()
        untiny.get_services = MagicMock(return_value=set([".tk", "1u.ro", "1url.com", "2pl.us"]))
        self.assertFalse(untiny.is_tiny("http://example.com"))
        self.assertTrue(untiny.is_tiny("http://1u.ro/123"))
        self.assertTrue(untiny.is_tiny("http://2pl.us/234"))
        self.assertEquals(untiny.get_services.call_count, 3)

    def test_extract(self):
        untiny = Untiny()

        mock_response = MagicMock()
        mock_response_text = PropertyMock()
        type(mock_response).text = mock_response_text

        untiny.is_tiny = MagicMock()

        with patch("requests.get", MagicMock(return_value=mock_response)) as mock_get:

            # If the URL is tiny send a request to untiny.me to extract
            # full URL
            untiny.is_tiny.return_value = True
            mock_response_text.return_value = "http://foo.com"
            self.assertEquals(
                untiny.extract("http://2pl.us/234"),
                "http://foo.com",
            )
            self.assertEquals(mock_get.call_count, 1)
            self.assertEquals(mock_response_text.call_count, 1)

            # Check with another URL
            mock_response_text.return_value = "http://bar.com"
            self.assertEquals(
                untiny.extract("http://1u.ro/123"),
                "http://bar.com",
            )
            self.assertEquals(mock_get.call_count, 2)
            self.assertEquals(mock_response_text.call_count, 2)

            # If the URL is not tiny return it unchanged.
            untiny.is_tiny.return_value = False
            self.assertEquals(
                untiny.extract("http://example.com"),
                "http://example.com",
            )
            self.assertEquals(mock_get.call_count, 2)

        with patch("requests.get", MagicMock(side_effect=requests.RequestException)) as mock_get:
            # If a request to untiny.me fails return the original URL.
            untiny.is_tiny.return_value = True
            self.assertEquals(
                untiny.extract("http://1u.ro/123"),
                "http://1u.ro/123",
            )
            self.assertEquals(mock_get.call_count, 1)


class URLFinderTestCase(unittest.TestCase):

    def test_clean_url(self):
        finder = URLFinder()

        url = "http://www.slideshare.net/mpirnat/web-development-with-python-and-django?utm_source=Python+Weekly+Newsletter&utm_campaign=7fc9a4c2e2-Python_Weekly_Issue_70_January_17_2013&utm_medium=email"
        reference = "http://www.slideshare.net/mpirnat/web-development-with-python-and-django"
        self.assertEquals(finder.clean_params(url), reference)

        url = "http://www.youtube.com/watch?v=DDjpOrlfh0Y"
        reference = url
        self.assertEquals(finder.clean_params(url), reference)

        url = "http://www.youtube.com/watch?v=DDjpOrlfh0Y&utm_medium=email"
        reference = "http://www.youtube.com/watch?v=DDjpOrlfh0Y"
        self.assertEquals(finder.clean_params(url), reference)

    def test_is_blacklisted(self):
        finder = URLFinder()
        self.assertTrue(finder.is_blacklisted("http://instagr.am/12345"))
        self.assertFalse(finder.is_blacklisted("http://example.com"))

    def test_follow_redirects(self):

        def mock_requests_get(url, **kwargs):
            response = MagicMock()
            if url == "http://redirects.to":
                response.url = "http://finalurl.com"
            else:
                response.url = url
            return response

        with patch("requests.get", mock_requests_get):
            finder = URLFinder()
            self.assertEquals(
                finder.follow_redirects("http://redirects.to"),
                "http://finalurl.com",
            )
            self.assertEquals(
                finder.follow_redirects("http://example.com"),
                "http://example.com",
            )

        with patch("requests.get", MagicMock(side_effect=requests.RequestException)):
            finder = URLFinder()
            self.assertEquals(
                finder.follow_redirects("http://redirects.to"),
                None,
            )

    def test_find_urls(self):
        finder = URLFinder()
        finder.untiny.extract = MagicMock(side_effect=lambda x: x)
        finder.clean_params = MagicMock(side_effect=lambda x: x)
        finder.follow_redirects = MagicMock(side_effect=lambda x: x)
        finder.is_blacklisted = MagicMock(return_value=False)

        self.assertEquals(
            finder.find_urls("For http://spam.com bar http://ham.com"),
            set([
                "http://spam.com",
                "http://ham.com",
            ])
        )

        finder.untiny.extract.assert_has_calls([call("http://spam.com"), call("http://ham.com")])
        finder.clean_params.assert_has_calls([call("http://spam.com"), call("http://ham.com")])
        finder.follow_redirects.assert_has_calls([call("http://spam.com"), call("http://ham.com")])
        finder.is_blacklisted.assert_has_calls([call("http://spam.com"), call("http://ham.com")])




if __name__ == '__main__':
    unittest.main()
