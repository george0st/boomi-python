"""Fixture-based deserialization tests.

Loads real-ish API payloads from tests/fixtures/ and verifies the full
deserialization chain works without crashes. These act as integration
tests for the BaseModel + JsonMap + model constructor pipeline.
"""

import json
import pytest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())


class TestBulkResponseMixedFixture:

    def test_deserialize_mixed_bulk_response(self):
        from boomi.models.environment_map_extension_bulk_response import (
            EnvironmentMapExtensionBulkResponse,
        )

        data = load_fixture("bulk_response_mixed.json")
        obj = EnvironmentMapExtensionBulkResponse._unmap(data)
        assert obj is not None
        # Should have response list with mixed success/error items
        assert hasattr(obj, "response")
        assert len(obj.response) > 0


class TestSparseAsyncResponseFixture:

    def test_deserialize_sparse_async(self):
        from boomi.models.persisted_process_properties_async_response import (
            PersistedProcessPropertiesAsyncResponse,
        )

        data = load_fixture("sparse_async_response.json")
        obj = PersistedProcessPropertiesAsyncResponse._unmap(data)
        assert obj is not None
        assert obj.response_status_code == 202


class TestFullAsyncResponseFixture:

    def test_deserialize_full_async(self):
        from boomi.models.persisted_process_properties_async_response import (
            PersistedProcessPropertiesAsyncResponse,
        )

        data = load_fixture("full_async_response.json")
        obj = PersistedProcessPropertiesAsyncResponse._unmap(data)
        assert obj.response_status_code == 200
        assert hasattr(obj, "result")
        assert len(obj.result) > 0


class TestUdfListWrapFixture:

    def test_deserialize_udf_with_nested_wrappers(self):
        from boomi.models.environment_map_extension_user_defined_function import (
            EnvironmentMapExtensionUserDefinedFunction,
        )
        from boomi.models.map_extensions_inputs import MapExtensionsInputs

        data = load_fixture("udf_with_list_wrap.json")
        obj = EnvironmentMapExtensionUserDefinedFunction._unmap(data)
        assert obj is not None
        assert isinstance(obj.inputs, MapExtensionsInputs)


class TestNormalModelPartialFixture:

    def test_deserialize_partial_model(self):
        from boomi.models.account import Account

        data = load_fixture("normal_model_partial.json")
        obj = Account._unmap(data)
        assert obj is not None
        assert obj.account_id == "acct-partial"
