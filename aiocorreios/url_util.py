import urllib.parse


class UrlUtil:
    @staticmethod
    def get_url(url, params):
        """
        Create a url with params.
        """
        return url + '?' + urllib.parse.urlencode(params)
