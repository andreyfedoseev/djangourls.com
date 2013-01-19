import unittest


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
