
from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .list_queues import ListQueues


@JsonMap(
    {
        "number_of_results": "numberOfResults",
        "response_status_code": "responseStatusCode",
    }
)
class ListQueuesAsyncResponse(BaseModel):
    """ListQueuesAsyncResponse

    :param number_of_results: number_of_results, defaults to None
    :type number_of_results: int, optional
    :param response_status_code: response_status_code, defaults to None
    :type response_status_code: int, optional
    :param result: result, defaults to None
    :type result: List[ListQueues], optional
    """

    def __init__(
        self,
        response_status_code: int = SENTINEL,
        number_of_results: int = SENTINEL,
        result: List[ListQueues] = SENTINEL,
        **kwargs,
    ):
        """ListQueuesAsyncResponse

        :param number_of_results: number_of_results, defaults to None
        :type number_of_results: int, optional
        :param response_status_code: response_status_code, defaults to None
        :type response_status_code: int, optional
        :param result: result, defaults to None
        :type result: List[ListQueues], optional
        """
        if number_of_results is not SENTINEL:
            self.number_of_results = int(number_of_results)
        if response_status_code is not SENTINEL:
            self.response_status_code = int(response_status_code)
        if result is not SENTINEL:
            self.result = self._define_list(result, ListQueues)
        self._kwargs = kwargs
