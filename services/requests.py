import os

import httpx
from django.conf import settings
from httpx import Response
from httpx._types import URLTypes


class HTTPClient(httpx.Client):
    def request(
        self,
        method: str,
        url: URLTypes,
        *args,
        **kwargs,
    ) -> Response:
        return super().request(
            method=method,
            url=os.path.join(settings.PAYMENT_URL, url),
            auth=(settings.PAYMENT_LOGIN, settings.PAYMENT_PASS),
            **kwargs,
        )


http_client = HTTPClient()
