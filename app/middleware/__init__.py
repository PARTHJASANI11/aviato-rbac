from fastapi import Request
from urllib.parse import urlparse


class MiddlewareHelper:
    @staticmethod
    def request_to_exclude(
        request: Request, endpoints_to_exclude: dict
    ):
        """
        Method to check whether endpoint is exclude from token verification or not

        :param request: Request object
        :param endpoints_to_exclude: List of endpoints
        :return bool: True if it is in the list to exclude else False
        """
        request_url = urlparse(str(request.url))
        method = str(request.method)

        if (
            method in endpoints_to_exclude
            and request_url.path in endpoints_to_exclude[method]
        ):
            return True
        else:
            return False


middleware_helper = MiddlewareHelper()
