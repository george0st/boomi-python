
from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .async_token import AsyncToken


@JsonMap({"async_token": "asyncToken", "response_status_code": "responseStatusCode"})
class AsyncOperationTokenResult(BaseModel):
    """AsyncOperationTokenResult

    :param async_token: async_token, defaults to None
    :type async_token: AsyncToken, optional
    :param response_status_code: The status code returned from a request, as follows:   - 202 — Initialized the Listener status request and is in progress (QUERY response).  - 200 — Listener status request is complete (GET response)., defaults to None
    :type response_status_code: int, optional
    """

    def __init__(self, async_token: AsyncToken = SENTINEL, response_status_code: int = SENTINEL, **kwargs):
        """AsyncOperationTokenResult

        :param async_token: async_token, defaults to None
        :type async_token: AsyncToken, optional
        :param response_status_code: The status code returned from a request, as follows:   - 202 — Initialized the Listener status request and is in progress (QUERY response).  - 200 — Listener status request is complete (GET response)., defaults to None
        :type response_status_code: int, optional
        """
        if async_token is not SENTINEL:
            self.async_token = self._define_object(async_token, AsyncToken)
        if response_status_code is not SENTINEL:
            self.response_status_code = response_status_code
        self._kwargs = kwargs
