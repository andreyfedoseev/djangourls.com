from mock import MagicMock, patch
from trends.utils import Untiny
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
            "http://example.com?extracted=true",
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


class UtilsTestCase(unittest.TestCase):

    def test_clean_url(self):
        from trends.utils import clean_url

        url = "http://www.slideshare.net/mpirnat/web-development-with-python-and-django?utm_source=Python+Weekly+Newsletter&utm_campaign=7fc9a4c2e2-Python_Weekly_Issue_70_January_17_2013&utm_medium=email"
        reference = "http://www.slideshare.net/mpirnat/web-development-with-python-and-django"
        self.assertEquals(clean_url(url), reference)

        url = "http://www.youtube.com/watch?v=DDjpOrlfh0Y"
        reference = url
        self.assertEquals(clean_url(url), reference)

        url = "http://www.youtube.com/watch?v=DDjpOrlfh0Y&utm_medium=email"
        reference = "http://www.youtube.com/watch?v=DDjpOrlfh0Y"
        self.assertEquals(clean_url(url), reference)


if __name__ == '__main__':
    unittest.main()
