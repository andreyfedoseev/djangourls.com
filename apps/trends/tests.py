from mock import MagicMock, patch, call
from trends.utils import Untiny, URLFinder
import requests
import unittest


def fake_request_to_untiny(url, **kwargs):

    MAP = {
        "http://1u.ro/123": "http://2pl.us/234",
        "http://2pl.us/234": "http://example.com?extracted=true"
    }

    response = MagicMock()

    if url == Untiny.SERVICES_URL:
        response.text = ".tk, 1u.ro, 1url.com, 2pl.us"

    elif url == Untiny.EXTRACT_URL:
        u = kwargs["params"]["url"]
        response.text = MAP.get(u, u)

    else:
        raise requests.RequestException

    return response


class UntinyTestCase(unittest.TestCase):

    @patch("requests.get", fake_request_to_untiny)
    def test_get_services(self):
        untiny = Untiny()
        self.assertEquals(
            untiny.get_services(),
            set([".tk", "1u.ro", "1url.com", "2pl.us"])
        )
        with patch("requests.get", MagicMock(side_effect=requests.RequestException)):
            self.assertEquals(untiny.get_services(), set())

    @patch("requests.get", fake_request_to_untiny)
    def test_is_tiny(self):
        untiny = Untiny()
        self.assertFalse(untiny.is_tiny("http://example.com"))
        self.assertTrue(untiny.is_tiny("http://1u.ro/123"))
        self.assertTrue(untiny.is_tiny("http://2pl.us/234"))

    @patch("requests.get", fake_request_to_untiny)
    def test_untiny(self):
        untiny = Untiny()
        self.assertEquals(
            untiny.extract("http://2pl.us/234"),
            "http://example.com?extracted=true",
        )
        self.assertEquals(
            untiny.extract("http://1u.ro/123"),
            "http://2pl.us/234",
        )
        self.assertEquals(
            untiny.extract("http://example.com"),
            "http://example.com",
        )
        with patch("requests.get", MagicMock(side_effect=requests.RequestException)):
            self.assertEquals(
                untiny.extract("http://1u.ro/123"),
                "http://1u.ro/123",
            )


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
