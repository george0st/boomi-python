
from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .deployed_process import DeployedProcess


@JsonMap({"process": "Process", "atom_id": "atomId"})
class PersistedProcessProperties(BaseModel):
    """PersistedProcessProperties

    :param process: process, defaults to None
    :type process: List[DeployedProcess], optional
    :param atom_id: A unique ID assigned by the system to the Runtime., defaults to None
    :type atom_id: str, optional
    """

    def __init__(
        self, atom_id: str = SENTINEL, process: List[DeployedProcess] = SENTINEL, **kwargs
    ):
        """PersistedProcessProperties

        :param process: process, defaults to None
        :type process: List[DeployedProcess], optional
        :param atom_id: A unique ID assigned by the system to the Runtime., defaults to None
        :type atom_id: str, optional
        """
        if atom_id is not SENTINEL:
            self.atom_id = atom_id
        if process is not SENTINEL:
            self.process = self._define_list(process, DeployedProcess)
        self._kwargs = kwargs
