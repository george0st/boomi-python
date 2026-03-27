
from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .listener_status import ListenerStatus


@JsonMap(
    {
        "number_of_results": "numberOfResults",
        "response_status_code": "responseStatusCode",
    }
)
class ListenerStatusAsyncResponse(BaseModel):
    """ListenerStatusAsyncResponse

    :param number_of_results: number_of_results, defaults to None
    :type number_of_results: int, optional
    :param response_status_code: The status code returned from a request, as follows:   - 202 — Initialized the Listener status request and is in progress (QUERY response).  - 200 — Listener status request is complete (GET response)., defaults to None
    :type response_status_code: int, optional
    :param result: result, defaults to None
    :type result: List[ListenerStatus], optional
    """

    def __init__(
        self,
        response_status_code: int = SENTINEL,
        number_of_results: int = SENTINEL,
        result: List[ListenerStatus] = SENTINEL,
        **kwargs,
    ):
        """ListenerStatusAsyncResponse

        :param number_of_results: number_of_results, defaults to None
        :type number_of_results: int, optional
        :param response_status_code: The status code returned from a request, as follows:   - 202 — Initialized the Listener status request and is in progress (QUERY response).  - 200 — Listener status request is complete (GET response)., defaults to None
        :type response_status_code: int, optional
        :param result: result, defaults to None
        :type result: List[ListenerStatus], optional
        """
        if number_of_results is not SENTINEL:
            self.number_of_results = number_of_results
        if response_status_code is not SENTINEL:
            self.response_status_code = response_status_code
        if result is not SENTINEL:
            self.result = self._define_list(result, ListenerStatus)
        self._kwargs = kwargs
