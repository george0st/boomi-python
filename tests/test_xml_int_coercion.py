"""XML string-to-int coercion regression tests.

When the Boomi API returns XML, parse_xml_to_dict() produces string values
for all fields. The async response models must coerce response_status_code
and number_of_results to int. These tests verify the coercion works for
both string input (XML path) and int input (JSON path).
"""

import pytest
from boomi.models.listener_status_async_response import ListenerStatusAsyncResponse
from boomi.models.runtime_observability_settings_async_response import RuntimeObservabilitySettingsAsyncResponse
from boomi.models.persisted_process_properties_async_response import PersistedProcessPropertiesAsyncResponse
from boomi.models.list_queues_async_response import ListQueuesAsyncResponse
from boomi.models.atom_counters_async_response import AtomCountersAsyncResponse
from boomi.models.atom_disk_space_async_response import AtomDiskSpaceAsyncResponse
from boomi.models.account_cloud_attachment_properties_async_response import AccountCloudAttachmentPropertiesAsyncResponse
from boomi.models.runtime_properties_async_response import RuntimePropertiesAsyncResponse
from boomi.models.cloud_attachment_properties_async_response import CloudAttachmentPropertiesAsyncResponse
from boomi.models.atom_security_policies_async_response import AtomSecurityPoliciesAsyncResponse
from boomi.models.account_cloud_attachment_properties_default_async_response import AccountCloudAttachmentPropertiesDefaultAsyncResponse
from boomi.models.async_operation_token_result import AsyncOperationTokenResult
from boomi.models.release_integration_pack_status import ReleaseIntegrationPackStatus


# Models with both response_status_code AND number_of_results
MODELS_WITH_BOTH = [
    ListenerStatusAsyncResponse,
    RuntimeObservabilitySettingsAsyncResponse,
    PersistedProcessPropertiesAsyncResponse,
    ListQueuesAsyncResponse,
    AtomCountersAsyncResponse,
    AtomDiskSpaceAsyncResponse,
    AccountCloudAttachmentPropertiesAsyncResponse,
    RuntimePropertiesAsyncResponse,
    CloudAttachmentPropertiesAsyncResponse,
    AtomSecurityPoliciesAsyncResponse,
    AccountCloudAttachmentPropertiesDefaultAsyncResponse,
]

# Models with only response_status_code
MODELS_STATUS_ONLY = [
    AsyncOperationTokenResult,
    ReleaseIntegrationPackStatus,
]

ALL_MODELS = MODELS_WITH_BOTH + MODELS_STATUS_ONLY


@pytest.mark.parametrize("model_cls", ALL_MODELS, ids=lambda c: c.__name__)
class TestResponseStatusCodeCoercion:
    """response_status_code must be int regardless of input type."""

    def test_string_coerced_to_int(self, model_cls):
        """XML path: parse_xml_to_dict returns string values."""
        obj = model_cls._unmap({"responseStatusCode": "202"})
        assert isinstance(obj.response_status_code, int)
        assert obj.response_status_code == 202

    def test_int_passthrough(self, model_cls):
        """JSON path: values are already int."""
        obj = model_cls._unmap({"responseStatusCode": 200})
        assert isinstance(obj.response_status_code, int)
        assert obj.response_status_code == 200


@pytest.mark.parametrize("model_cls", MODELS_WITH_BOTH, ids=lambda c: c.__name__)
class TestNumberOfResultsCoercion:
    """number_of_results must be int regardless of input type."""

    def test_string_coerced_to_int(self, model_cls):
        obj = model_cls._unmap({"responseStatusCode": "200", "numberOfResults": "5"})
        assert isinstance(obj.number_of_results, int)
        assert obj.number_of_results == 5

    def test_int_passthrough(self, model_cls):
        obj = model_cls._unmap({"responseStatusCode": 200, "numberOfResults": 1})
        assert isinstance(obj.number_of_results, int)
        assert obj.number_of_results == 1
