"""Tests for BUG-09: PersistedProcessProperties deserialization fix."""

import pytest
from boomi.models.persisted_process_properties import PersistedProcessProperties
from boomi.models.persisted_process_properties_async_response import (
    PersistedProcessPropertiesAsyncResponse,
)
from boomi.models.deployed_process import DeployedProcess


class TestPersistedProcessPropertiesUnmap:
    """Test that _unmap() correctly deserializes API response dicts."""

    def test_persisted_process_properties_with_atom_id(self):
        data = {"atomId": "abc-123", "Process": []}
        obj = PersistedProcessProperties._unmap(data)
        assert obj.atom_id == "abc-123"

    def test_persisted_process_properties_without_atom_id(self):
        data = {"Process": []}
        obj = PersistedProcessProperties._unmap(data)
        assert not hasattr(obj, "atom_id")

    def test_persisted_process_properties_empty_dict(self):
        obj = PersistedProcessProperties._unmap({})
        assert not hasattr(obj, "atom_id")
        assert not hasattr(obj, "process")


class TestDeployedProcessUnmap:
    """Test DeployedProcess deserialization."""

    def test_deployed_process_with_fields(self):
        data = {
            "processId": "proc-1",
            "ProcessProperties": {"ProcessProperty": []},
        }
        obj = DeployedProcess._unmap(data)
        assert obj.process_id == "proc-1"

    def test_deployed_process_empty_dict(self):
        obj = DeployedProcess._unmap({})
        assert not hasattr(obj, "process_id")
        assert not hasattr(obj, "process_properties")


class TestAsyncResponseUnmap:
    """Test full async response deserialization chain."""

    def test_full_response_deserialization(self):
        data = {
            "responseStatusCode": 200,
            "numberOfResults": 1,
            "result": [
                {
                    "atomId": "atom-1",
                    "Process": [
                        {
                            "processId": "p1",
                            "ProcessProperties": {
                                "ProcessProperty": [
                                    {
                                        "ProcessPropertyValue": [
                                            {"key": "prop1", "value": "val1"}
                                        ]
                                    }
                                ]
                            },
                        }
                    ],
                }
            ],
        }
        obj = PersistedProcessPropertiesAsyncResponse._unmap(data)
        assert obj.response_status_code == 200
        assert obj.number_of_results == 1
        assert len(obj.result) == 1
        props = obj.result[0]
        assert props.atom_id == "atom-1"
        assert len(props.process) == 1
        assert props.process[0].process_id == "p1"

    def test_response_without_results(self):
        data = {"responseStatusCode": 202}
        obj = PersistedProcessPropertiesAsyncResponse._unmap(data)
        assert obj.response_status_code == 202
        assert not hasattr(obj, "result")
