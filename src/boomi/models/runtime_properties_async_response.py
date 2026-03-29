
from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .runtime_properties import RuntimeProperties


@JsonMap(
    {
        "number_of_results": "numberOfResults",
        "response_status_code": "responseStatusCode",
    }
)
class RuntimePropertiesAsyncResponse(BaseModel):
    """RuntimePropertiesAsyncResponse

    :param response_status_code: response_status_code, defaults to None
    :type response_status_code: int, optional
    :param number_of_results: number_of_results, defaults to None
    :type number_of_results: int, optional
    :param result: result, defaults to None
    :type result: List[RuntimeProperties], optional
    """

    def __init__(
        self,
        response_status_code: int = SENTINEL,
        number_of_results: int = SENTINEL,
        result: List[RuntimeProperties] = SENTINEL,
        **kwargs,
    ):
        """RuntimePropertiesAsyncResponse

        :param response_status_code: response_status_code, defaults to None
        :type response_status_code: int, optional
        :param number_of_results: number_of_results, defaults to None
        :type number_of_results: int, optional
        :param result: result, defaults to None
        :type result: List[RuntimeProperties], optional
        """
        if number_of_results is not SENTINEL:
            self.number_of_results = int(number_of_results)
        if response_status_code is not SENTINEL:
            self.response_status_code = int(response_status_code)
        if result is not SENTINEL:
            self.result = self._define_list(result, RuntimeProperties)
        self._kwargs = kwargs
