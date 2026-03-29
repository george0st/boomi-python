"""Tests for the OpenAPI spec update: new CloudAttachmentProperties service,
ChangeListenerStatus path fix, As2PartnerInfo new fields, and
AccountCloudAttachmentProperties validation tightening."""

import asyncio
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boomi.models import (
    CloudAttachmentProperties,
    CloudAttachmentPropertiesAsyncResponse,
    As2PartnerInfo,
    AccountCloudAttachmentProperties,
    AccountCloudAttachmentPropertiesAsyncResponse,
    ListenerStatusQueryConfig,
    ListenerStatusAsyncResponse,
)
from boomi.net.transport.utils import parse_xml_to_dict
from boomi.services.cloud_attachment_properties import CloudAttachmentPropertiesService
from boomi.services.async_.cloud_attachment_properties import (
    CloudAttachmentPropertiesServiceAsync,
)
from boomi.services.change_listener_status import ChangeListenerStatusService
from boomi.services.account_cloud_attachment_properties import (
    AccountCloudAttachmentPropertiesService,
)
from boomi.services.listener_status import ListenerStatusService
from boomi import Boomi
from boomi.sdk_async import BoomiAsync


def _capture_request(service, response_body, status=200, content_type="application/json"):
    captured = {}
    service.set_access_token("test-token")
    service.set_basic_auth("test-user", "test-pass")

    def fake_send_request(request):
        captured["request"] = request
        return response_body, status, content_type

    service.send_request = fake_send_request
    return captured


# ---------- CloudAttachmentProperties model ----------

class TestCloudAttachmentPropertiesModel:
    def test_map(self):
        props = CloudAttachmentProperties(
            archive_processed_documents=True,
            container_name="myCloud",
            container_purge_days=30,
            container_purge_immediately=False,
            default_time_zone_for_account_schedules="America/New_York",
            low_latency_warning_threshold=100,
            partial_update=True,
            purge_schedule_for_components=15,
            purge_schedule_for_logs=7,
            purge_schedule_for_processed_documents=10,
            purge_schedule_for_temporary_data=5,
            runtime_id="abc-123",
        )
        mapped = props._map()
        assert mapped["archiveProcessedDocuments"] is True
        assert mapped["containerName"] == "myCloud"
        assert mapped["containerPurgeDays"] == 30
        assert mapped["containerPurgeImmediately"] is False
        assert mapped["defaultTimeZoneForAccountSchedules"] == "America/New_York"
        assert mapped["lowLatencyWarningThreshold"] == 100
        assert mapped["partialUpdate"] is True
        assert mapped["purgeScheduleForComponents"] == 15
        assert mapped["purgeScheduleForLogs"] == 7
        assert mapped["purgeScheduleForProcessedDocuments"] == 10
        assert mapped["purgeScheduleForTemporaryData"] == 5
        assert mapped["runtimeId"] == "abc-123"

    def test_unmap(self):
        data = {
            "archiveProcessedDocuments": False,
            "containerName": "cloud2",
            "containerPurgeDays": 60,
            "runtimeId": "xyz-789",
        }
        obj = CloudAttachmentProperties._unmap(data)
        assert obj.archive_processed_documents is False
        assert obj.container_name == "cloud2"
        assert obj.container_purge_days == 60
        assert obj.runtime_id == "xyz-789"


# ---------- CloudAttachmentPropertiesAsyncResponse model ----------

class TestCloudAttachmentPropertiesAsyncResponse:
    def test_map(self):
        inner = CloudAttachmentProperties(container_name="c1", runtime_id="r1")
        resp = CloudAttachmentPropertiesAsyncResponse(
            response_status_code=200,
            number_of_results=1,
            result=[inner],
        )
        mapped = resp._map()
        assert mapped["responseStatusCode"] == 200
        assert mapped["numberOfResults"] == 1
        assert len(mapped["result"]) == 1

    def test_unmap(self):
        data = {
            "responseStatusCode": 200,
            "numberOfResults": 2,
            "result": [
                {"containerName": "a", "runtimeId": "r1"},
                {"containerName": "b", "runtimeId": "r2"},
            ],
        }
        obj = CloudAttachmentPropertiesAsyncResponse._unmap(data)
        assert obj.response_status_code == 200
        assert obj.number_of_results == 2
        assert len(obj.result) == 2
        assert obj.result[0].container_name == "a"
        assert obj.result[1].runtime_id == "r2"


# ---------- As2PartnerInfo new fields ----------

class TestAs2PartnerInfoNewFields:
    def test_map_new_fields(self):
        info = As2PartnerInfo(
            require_encrypted_messages=True,
            require_signed_messages=False,
        )
        mapped = info._map()
        assert mapped["requireEncryptedMessages"] is True
        assert mapped["requireSignedMessages"] is False

    def test_unmap_new_fields(self):
        data = {
            "requireEncryptedMessages": False,
            "requireSignedMessages": True,
        }
        obj = As2PartnerInfo._unmap(data)
        assert obj.require_encrypted_messages is False
        assert obj.require_signed_messages is True


# ---------- ChangeListenerStatus URL ----------

class TestChangeListenerStatusUrl:
    def test_uses_lowercase_path_and_serializes_body(self):
        svc = ChangeListenerStatusService(base_url="https://api.example.com")
        captured = _capture_request(svc, {}, status=200, content_type="")

        svc.create_change_listener_status(
            request_body={
                "action": "pause",
                "container_id": "container-1",
                "listener_id": "listener-1",
            }
        )

        req = captured["request"]
        assert req.method == "POST"
        assert req.url == "https://api.example.com/changeListenerStatus"
        assert "/ChangeListenerStatus" not in req.url
        assert req.body["action"] == "pause"
        assert req.body["containerId"] == "container-1"
        assert req.body["listenerId"] == "listener-1"


# ---------- AccountCloudAttachmentProperties validation ----------

class TestAccountCloudAttachmentPropertiesValidation:
    def test_rejects_missing_request_body(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        with pytest.raises(TypeError):
            svc.update_account_cloud_attachment_properties(id_="test-id", request_body=None)

    def test_missing_container_id_defaults_to_id(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc, {"containerId": "test-id", "accountDiskUsage": 100},
        )
        body = AccountCloudAttachmentProperties(account_disk_usage=100)
        svc.update_account_cloud_attachment_properties(id_="test-id", request_body=body)
        assert captured["request"].body["containerId"] == "test-id"

    def test_container_id_fallback_does_not_mutate_caller_model(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        body = AccountCloudAttachmentProperties(account_disk_usage=100)

        # First call with id_="first-id"
        cap1 = _capture_request(svc, {"containerId": "first-id", "accountDiskUsage": 100})
        svc.update_account_cloud_attachment_properties(id_="first-id", request_body=body)
        assert cap1["request"].body["containerId"] == "first-id"

        # Same body reused with a different id_
        cap2 = _capture_request(svc, {"containerId": "second-id", "accountDiskUsage": 100})
        svc.update_account_cloud_attachment_properties(id_="second-id", request_body=body)
        assert cap2["request"].body["containerId"] == "second-id"

        # Original model must remain unmodified
        assert not getattr(body, 'container_id', None)

    def test_valid_request_serializes_expected_path_and_body(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc,
            {"containerId": "container-1", "testModeMaxDocs": 101},
        )
        body = AccountCloudAttachmentProperties(
            container_id="container-1",
            test_mode_max_docs=101,
        )

        svc.update_account_cloud_attachment_properties(
            id_="test-id",
            request_body=body,
        )

        req = captured["request"]
        assert req.method == "POST"
        assert req.url == "https://api.example.com/AccountCloudAttachmentProperties/test-id"
        assert req.body["containerId"] == "container-1"
        assert req.body["testModeMaxDocs"] == 101


# ---------- Service request serialization ----------

class TestCloudAttachmentPropertiesServiceSerialization:
    def test_update_cloud_attachment_properties_defaults_runtime_id_to_path_id(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc,
            {"runtimeId": "runtime-1", "containerName": "cloud-1"},
        )
        body = CloudAttachmentProperties(
            container_name="cloud-1",
            container_purge_days=31,
            partial_update=True,
        )

        svc.update_cloud_attachment_properties(id_="runtime-1", request_body=body)

        req = captured["request"]
        assert req.body["runtimeId"] == "runtime-1"
        assert not getattr(body, "runtime_id", None)

    def test_update_cloud_attachment_properties_serializes_request(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc,
            {"runtimeId": "runtime-1", "containerName": "cloud-1", "containerPurgeDays": 31, "partialUpdate": True},
        )
        body = CloudAttachmentProperties(
            runtime_id="runtime-1",
            container_name="cloud-1",
            container_purge_days=31,
            partial_update=True,
        )

        svc.update_cloud_attachment_properties(id_="runtime-1", request_body=body)

        req = captured["request"]
        assert req.method == "POST"
        assert req.url == "https://api.example.com/CloudAttachmentProperties/runtime-1"
        assert req.body["runtimeId"] == "runtime-1"
        assert req.body["containerName"] == "cloud-1"
        assert req.body["containerPurgeDays"] == 31
        assert req.body["partialUpdate"] is True

    def test_async_get_cloud_attachment_properties_serializes_request(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc,
            {"asyncToken": {"token": "tok-1"}, "responseStatusCode": 202},
        )

        result = svc.async_get_cloud_attachment_properties(id_="runtime-1")

        req = captured["request"]
        assert req.method == "GET"
        assert req.url == "https://api.example.com/async/CloudAttachmentProperties/runtime-1"
        assert req.body is None
        assert result.async_token.token == "tok-1"
        assert result.response_status_code == 202

    def test_async_token_cloud_attachment_properties_serializes_request(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"runtimeId": "runtime-1", "containerName": "cloud-1"}],
            },
        )

        result = svc.async_token_cloud_attachment_properties(token="token-123")

        req = captured["request"]
        assert req.method == "GET"
        assert (
            req.url
            == "https://api.example.com/async/CloudAttachmentProperties/response/token-123"
        )
        assert req.body is None
        assert result.response_status_code == 200
        assert result.number_of_results == 1
        assert len(result.result) == 1


# ---------- SDK wiring ----------

class TestSdkWiring:
    def test_boomi_has_cloud_attachment_properties(self):
        sdk = Boomi(access_token="test", account_id="test")
        assert hasattr(sdk, "cloud_attachment_properties")

    def test_boomi_async_has_cloud_attachment_properties(self):
        sdk = BoomiAsync(access_token="test", account_id="test")
        assert hasattr(sdk, "cloud_attachment_properties")


# ---------- CloudAttachmentProperties service path inspection ----------

class TestCloudAttachmentPropertiesServicePaths:
    @staticmethod
    def _read_service_source():
        import inspect
        source_file = inspect.getfile(CloudAttachmentPropertiesService)
        with open(source_file) as f:
            return f.read()

    def test_update_uses_correct_path_and_method(self):
        source = self._read_service_source()
        assert "/CloudAttachmentProperties/{{id}}" in source
        assert 'set_method("POST")' in source

    def test_async_get_uses_correct_path_and_method(self):
        source = self._read_service_source()
        assert "/async/CloudAttachmentProperties/{{id}}" in source
        assert 'set_method("GET")' in source

    def test_async_token_uses_correct_path_and_method(self):
        source = self._read_service_source()
        assert "/async/CloudAttachmentProperties/response/{{token}}" in source
        assert 'set_method("GET")' in source


# ---------- AccountCloudAttachmentProperties container_id fallback ----------

class TestAccountCloudAttachmentPropertiesContainerIdFallback:
    def test_empty_container_id_defaults_to_id(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(svc, {"containerId": "test-id"})
        body = AccountCloudAttachmentProperties(container_id="")
        svc.update_account_cloud_attachment_properties(id_="test-id", request_body=body)
        assert captured["request"].body["containerId"] == "test-id"

    def test_none_container_id_defaults_to_id(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(svc, {"containerId": "test-id"})
        body = AccountCloudAttachmentProperties(container_id=None)
        svc.update_account_cloud_attachment_properties(id_="test-id", request_body=body)
        assert captured["request"].body["containerId"] == "test-id"

    def test_explicit_container_id_preserved(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(svc, {"containerId": "explicit"})
        body = AccountCloudAttachmentProperties(container_id="explicit")
        svc.update_account_cloud_attachment_properties(id_="other-id", request_body=body)
        assert captured["request"].body["containerId"] == "explicit"


# ---------- AccountCloudAttachmentProperties async token backfill ----------

class TestAccountCloudAsyncTokenBackfill:
    def test_async_token_backfills_container_id(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        # Step 1: async_get stores the token->container mapping
        _capture_request(
            svc, {"asyncToken": {"token": "tok-1"}, "responseStatusCode": 202}
        )
        svc.async_get_account_cloud_attachment_properties(id_="cid-1")

        # Step 2: async_token backfills container_id from the mapping
        _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"accountDiskUsage": 100}],
            },
        )
        result = svc.async_token_account_cloud_attachment_properties(token="tok-1")
        assert result.result[0].container_id == "cid-1"

    def test_async_token_preserves_existing_container_id(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        _capture_request(
            svc, {"asyncToken": {"token": "tok-2"}, "responseStatusCode": 202}
        )
        svc.async_get_account_cloud_attachment_properties(id_="cid-2")

        _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"containerId": "api-provided", "accountDiskUsage": 50}],
            },
        )
        result = svc.async_token_account_cloud_attachment_properties(token="tok-2")
        assert result.result[0].container_id == "api-provided"

    def test_multi_token_bookkeeping(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")

        # Register two different async_get calls
        _capture_request(
            svc, {"asyncToken": {"token": "tokA"}, "responseStatusCode": 202}
        )
        svc.async_get_account_cloud_attachment_properties(id_="container-A")

        _capture_request(
            svc, {"asyncToken": {"token": "tokB"}, "responseStatusCode": 202}
        )
        svc.async_get_account_cloud_attachment_properties(id_="container-B")

        # Resolve token B first
        _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"accountDiskUsage": 1}],
            },
        )
        result_b = svc.async_token_account_cloud_attachment_properties(token="tokB")
        assert result_b.result[0].container_id == "container-B"

        # Resolve token A second
        _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"accountDiskUsage": 2}],
            },
        )
        result_a = svc.async_token_account_cloud_attachment_properties(token="tokA")
        assert result_a.result[0].container_id == "container-A"

        # Tokens should be cleaned up
        assert len(svc._token_to_container) == 0

    def test_polling_202_then_200_backfills_on_completion(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        _capture_request(
            svc, {"asyncToken": {"token": "tok-poll"}, "responseStatusCode": 202}
        )
        svc.async_get_account_cloud_attachment_properties(id_="cid-poll")

        # First poll: 202 in-progress, no result items
        _capture_request(
            svc, {"responseStatusCode": 202}
        )
        interim = svc.async_token_account_cloud_attachment_properties(token="tok-poll")
        assert interim.response_status_code == 202
        # Mapping should still be retained
        assert "tok-poll" in svc._token_to_container

        # Second poll: 200 completed with result
        _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"accountDiskUsage": 42}],
            },
        )
        final = svc.async_token_account_cloud_attachment_properties(token="tok-poll")
        assert final.result[0].container_id == "cid-poll"
        assert "tok-poll" not in svc._token_to_container

    def test_intermediate_202_results_do_not_drop_container_id_backfill(self):
        svc = AccountCloudAttachmentPropertiesService(base_url="https://api.example.com")
        _capture_request(
            svc, {"asyncToken": {"token": "tok-partial"}, "responseStatusCode": 202}
        )
        svc.async_get_account_cloud_attachment_properties(id_="cid-partial")

        _capture_request(
            svc,
            {
                "responseStatusCode": 202,
                "numberOfResults": 1,
                "result": [{"accountDiskUsage": 5}],
            },
        )
        interim = svc.async_token_account_cloud_attachment_properties(
            token="tok-partial"
        )
        assert interim.result[0].container_id == "cid-partial"
        assert "tok-partial" in svc._token_to_container

        _capture_request(
            svc,
            {
                "responseStatusCode": 200,
                "numberOfResults": 1,
                "result": [{"accountDiskUsage": 6}],
            },
        )
        final = svc.async_token_account_cloud_attachment_properties(
            token="tok-partial"
        )
        assert final.result[0].container_id == "cid-partial"
        assert "tok-partial" not in svc._token_to_container


# ---------- ChangeListenerStatusRequest model ----------

class TestChangeListenerStatusRequestModel:
    def test_map_roundtrip(self):
        from boomi.models import ChangeListenerStatusRequest
        req = ChangeListenerStatusRequest(
            action="pause",
            container_id="c1",
            listener_id="l1",
        )
        mapped = req._map()
        assert mapped["action"] == "pause"
        assert mapped["containerId"] == "c1"
        assert mapped["listenerId"] == "l1"

    def test_unmap_camel_to_snake(self):
        from boomi.models import ChangeListenerStatusRequest
        data = {
            "action": "resume",
            "containerId": "c2",
            "listenerId": "l2",
        }
        obj = ChangeListenerStatusRequest._unmap(data)
        assert obj.action == "resume"
        assert obj.container_id == "c2"
        assert obj.listener_id == "l2"


# ---------- Extended SDK wiring ----------

class TestExtendedSdkWiring:
    def test_boomi_has_change_listener_status(self):
        sdk = Boomi(access_token="test", account_id="test")
        assert hasattr(sdk, "change_listener_status")

    def test_boomi_has_listener_status(self):
        sdk = Boomi(access_token="test", account_id="test")
        assert hasattr(sdk, "listener_status")

    def test_boomi_cloud_attachment_properties_methods(self):
        sdk = Boomi(access_token="test", account_id="test")
        cap = sdk.cloud_attachment_properties
        assert hasattr(cap, "update_cloud_attachment_properties")
        assert hasattr(cap, "async_get_cloud_attachment_properties")
        assert hasattr(cap, "async_token_cloud_attachment_properties")

    def test_boomi_async_has_change_listener_status(self):
        sdk = BoomiAsync(access_token="test", account_id="test")
        assert hasattr(sdk, "change_listener_status")

    def test_boomi_async_has_listener_status(self):
        sdk = BoomiAsync(access_token="test", account_id="test")
        assert hasattr(sdk, "listener_status")

    def test_boomi_async_cloud_attachment_properties_methods(self):
        sdk = BoomiAsync(access_token="test", account_id="test")
        cap = sdk.cloud_attachment_properties
        assert hasattr(cap, "update_cloud_attachment_properties")
        assert hasattr(cap, "async_get_cloud_attachment_properties")
        assert hasattr(cap, "async_token_cloud_attachment_properties")


# ---------- ListenerStatus request validation ----------

class TestListenerStatusValidation:
    def test_rejects_none_request_body(self):
        svc = ListenerStatusService(base_url="https://api.example.com")
        with pytest.raises(ValueError, match="request_body is required"):
            svc.async_get_listener_status(request_body=None)

    def test_rejects_missing_query_filter(self):
        svc = ListenerStatusService(base_url="https://api.example.com")
        body = ListenerStatusQueryConfig(query_filter=None)
        with pytest.raises(ValueError, match="query_filter"):
            svc.async_get_listener_status(request_body=body)

    def test_rejects_query_without_container_id(self):
        svc = ListenerStatusService(base_url="https://api.example.com")
        body = ListenerStatusQueryConfig(
            query_filter={
                "expression": {
                    "argument": ["some-listener"],
                    "operator": "EQUALS",
                    "property": "listenerId",
                }
            }
        )
        with pytest.raises(ValueError, match="containerId"):
            svc.async_get_listener_status(request_body=body)

    def test_accepts_valid_container_id_query(self):
        svc = ListenerStatusService(base_url="https://api.example.com")
        captured = _capture_request(
            svc, {"asyncToken": {"token": "t1"}, "responseStatusCode": 202}
        )
        body = ListenerStatusQueryConfig(
            query_filter={
                "expression": {
                    "argument": ["container-123"],
                    "operator": "EQUALS",
                    "property": "containerId",
                }
            }
        )
        result = svc.async_get_listener_status(request_body=body)
        assert result.async_token.token == "t1"

    def test_accepts_grouped_expression_with_container_id(self):
        svc = ListenerStatusService(base_url="https://api.example.com")
        captured = _capture_request(
            svc, {"asyncToken": {"token": "t2"}, "responseStatusCode": 202}
        )
        body = ListenerStatusQueryConfig(
            query_filter={
                "expression": {
                    "operator": "and",
                    "nestedExpression": [
                        {
                            "argument": ["container-123"],
                            "operator": "EQUALS",
                            "property": "containerId",
                        },
                        {
                            "argument": ["listener-456"],
                            "operator": "EQUALS",
                            "property": "listenerId",
                        },
                    ],
                }
            }
        )
        result = svc.async_get_listener_status(request_body=body)
        assert result.async_token.token == "t2"


# ---------- ListenerStatusAsyncResponse int ----------

class TestListenerStatusAsyncResponseInt:
    def test_response_status_code_is_int(self):
        resp = ListenerStatusAsyncResponse._unmap(
            {"responseStatusCode": 200, "numberOfResults": 0}
        )
        assert resp.response_status_code == 200
        assert isinstance(resp.response_status_code, int)

    def test_response_status_code_500(self):
        resp = ListenerStatusAsyncResponse._unmap({"responseStatusCode": 500})
        assert resp.response_status_code == 500
        assert isinstance(resp.response_status_code, int)

    def test_response_status_code_from_xml_string(self):
        """XML path: string values are coerced to int for consistency."""
        resp = ListenerStatusAsyncResponse._unmap({"responseStatusCode": "202"})
        assert resp.response_status_code == 202
        assert isinstance(resp.response_status_code, int)


# ---------- CloudAttachmentProperties update guard ----------

class TestCloudAttachmentPropertiesUpdateGuard:
    def test_rejects_missing_request_body(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        with pytest.raises(TypeError):
            svc.update_cloud_attachment_properties(id_="test-id", request_body=None)

    def test_rejects_missing_container_name(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        body = CloudAttachmentProperties(runtime_id="r1")
        with pytest.raises(ValueError, match="container_name is required"):
            svc.update_cloud_attachment_properties(id_="test-id", request_body=body)

    def test_valid_request_passes(self):
        svc = CloudAttachmentPropertiesService(base_url="https://api.example.com")
        captured = _capture_request(
            svc, {"containerName": "c1", "runtimeId": "r1"}
        )
        body = CloudAttachmentProperties(container_name="c1", runtime_id="r1")
        result = svc.update_cloud_attachment_properties(id_="test-id", request_body=body)
        assert result.container_name == "c1"


# ---------- CloudAttachmentProperties update guard (async parity) ----------

class TestCloudAttachmentPropertiesUpdateGuardAsync:
    def test_async_rejects_missing_request_body(self):
        svc = CloudAttachmentPropertiesServiceAsync(base_url="https://api.example.com")
        with pytest.raises(TypeError):
            asyncio.run(svc.update_cloud_attachment_properties(id_="test-id", request_body=None))

    def test_async_rejects_missing_container_name(self):
        svc = CloudAttachmentPropertiesServiceAsync(base_url="https://api.example.com")
        body = CloudAttachmentProperties(runtime_id="r1")
        with pytest.raises(ValueError, match="container_name is required"):
            asyncio.run(svc.update_cloud_attachment_properties(id_="test-id", request_body=body))

    def test_async_valid_request_passes(self):
        svc = CloudAttachmentPropertiesServiceAsync(base_url="https://api.example.com")
        captured = _capture_request(
            svc, {"containerName": "c1", "runtimeId": "r1"}
        )
        body = CloudAttachmentProperties(container_name="c1", runtime_id="r1")
        result = asyncio.run(svc.update_cloud_attachment_properties(id_="test-id", request_body=body))
        assert result.container_name == "c1"


# ---------- AccountCloudAttachmentProperties queue fields ----------

class TestAccountCloudAttachmentPropertiesQueueFields:
    def test_unmap_queue_fields(self):
        data = {
            "containerId": "c1",
            "queueCommitBatchLimit": 50,
            "queueMaxBatchSize": 100,
            "queueMaxDocSize": 2048,
            "queueMsgThrottleRate": 500,
            "queueUseFilePersistence": True,
            "queueIncomingMessageRateLimit": 1000,
        }
        obj = AccountCloudAttachmentProperties._unmap(data)
        assert obj.queue_commit_batch_limit == 50
        assert obj.queue_max_batch_size == 100
        assert obj.queue_max_doc_size == 2048
        assert obj.queue_msg_throttle_rate == 500
        assert obj.queue_use_file_persistence is True
        assert obj.queue_incoming_message_rate_limit == 1000
        # Ensure they are NOT only in _kwargs
        for key in (
            "queueCommitBatchLimit",
            "queueMaxBatchSize",
            "queueMaxDocSize",
            "queueMsgThrottleRate",
            "queueUseFilePersistence",
        ):
            assert key not in obj._kwargs

    def test_map_queue_fields(self):
        obj = AccountCloudAttachmentProperties(
            container_id="c1",
            queue_commit_batch_limit=50,
            queue_max_batch_size=100,
            queue_max_doc_size=2048,
            queue_msg_throttle_rate=500,
            queue_use_file_persistence=True,
        )
        mapped = obj._map()
        assert mapped["queueCommitBatchLimit"] == 50
        assert mapped["queueMaxBatchSize"] == 100
        assert mapped["queueMaxDocSize"] == 2048
        assert mapped["queueMsgThrottleRate"] == 500
        assert mapped["queueUseFilePersistence"] is True


# ---------- AsyncOperationResult single-item list wrapping regression ----------

class TestAsyncOperationResultListWrapping:
    """Regression: AsyncOperationResult with a single <result> element must be
    wrapped in a list so *AsyncResponse models deserialize correctly."""

    SINGLE_ITEM_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AsyncOperationResult xmlns:bns="http://api.platform.boomi.com/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' responseStatusCode="200" numberOfResults="1">'
        '<bns:result containerName="cloud-1" runtimeId="rt-1"'
        ' archiveProcessedDocuments="true" lowLatencyWarningThreshold="30"'
        ' partialUpdate="false"'
        ' containerPurgeDays="15" containerPurgeImmediately="false"/>'
        '</bns:AsyncOperationResult>'
    )

    EMPTY_RESULT_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AsyncOperationResult xmlns:bns="http://api.platform.boomi.com/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' responseStatusCode="200" numberOfResults="0">'
        '<bns:result xsi:type="bns:CloudAttachmentProperties"/>'
        '</bns:AsyncOperationResult>'
    )

    ACCOUNT_SINGLE_ITEM_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AsyncOperationResult xmlns:bns="http://api.platform.boomi.com/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' responseStatusCode="200" numberOfResults="1">'
        '<bns:result containerId="cid-1"/>'
        '</bns:AsyncOperationResult>'
    )

    def test_single_item_cloud_attachment_properties(self):
        parsed = parse_xml_to_dict(self.SINGLE_ITEM_XML)
        obj = CloudAttachmentPropertiesAsyncResponse._unmap(parsed)
        # XML attributes arrive as strings; verify int coercion works at model level
        assert int(obj.response_status_code) == 200
        assert int(obj.number_of_results) == 1
        assert isinstance(obj.result, list)
        assert len(obj.result) == 1
        item = obj.result[0]
        assert item.container_name == "cloud-1"
        assert item.runtime_id == "rt-1"
        assert item.archive_processed_documents == "true" or item.archive_processed_documents is True
        assert int(item.low_latency_warning_threshold) == 30
        assert item.partial_update == "false" or item.partial_update is False
        assert int(item.container_purge_days) == 15

    def test_single_item_account_cloud_attachment_properties(self):
        parsed = parse_xml_to_dict(self.ACCOUNT_SINGLE_ITEM_XML)
        obj = AccountCloudAttachmentPropertiesAsyncResponse._unmap(parsed)
        assert int(obj.response_status_code) == 200
        assert int(obj.number_of_results) == 1
        assert isinstance(obj.result, list)
        assert len(obj.result) == 1
        assert obj.result[0].container_id == "cid-1"

    def test_empty_result_stays_none(self):
        parsed = parse_xml_to_dict(self.EMPTY_RESULT_XML)
        obj = CloudAttachmentPropertiesAsyncResponse._unmap(parsed)
        assert int(obj.response_status_code) == 200
        assert not hasattr(obj, 'result') or obj.result is None


# ---------- Nested list fields in async responses (singleton xmltodict fix) ----------

class TestNestedListFieldsSingletonFix:
    """Regression: models with list fields (QueueRecord, counter, DiskSpaceDirectory,
    Process) must not break when xmltodict returns a singleton dict instead of a list."""

    PERSISTED_PROCESS_PROPS_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AsyncOperationResult xmlns:bns="http://api.platform.boomi.com/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' responseStatusCode="200" numberOfResults="1">'
        '<bns:result atomId="atom-1">'
        '<bns:Process processId="p1">'
        '<bns:ProcessProperties>'
        '<bns:ProcessProperty name="prop1" value="val1"/>'
        '</bns:ProcessProperties>'
        '</bns:Process>'
        '</bns:result>'
        '</bns:AsyncOperationResult>'
    )

    LIST_QUEUES_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AsyncOperationResult xmlns:bns="http://api.platform.boomi.com/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' responseStatusCode="200" numberOfResults="1">'
        '<bns:result>'
        '<bns:QueueRecord queueName="q1" queueType="TOPIC"'
        ' messagesCount="5" deadLettersCount="0"/>'
        '</bns:result>'
        '</bns:AsyncOperationResult>'
    )

    ATOM_DISK_SPACE_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AsyncOperationResult xmlns:bns="http://api.platform.boomi.com/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        ' responseStatusCode="200" numberOfResults="1">'
        '<bns:result quotaLimit="10GB" rawQuotaLimit="10737418240"'
        ' rawTotalSize="1024" totalSize="1KB">'
        '<bns:DiskSpaceDirectory file="/data" rawSize="512" size="512B"/>'
        '</bns:result>'
        '</bns:AsyncOperationResult>'
    )

    ATOM_COUNTERS_XML = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<bns:AtomCounters xmlns:bns="http://api.platform.boomi.com/"'
        ' atomId="atom-1">'
        '<bns:counter name="executions" value="42"/>'
        '</bns:AtomCounters>'
    )

    def test_persisted_process_properties_single_process(self):
        from boomi.models import PersistedProcessPropertiesAsyncResponse
        parsed = parse_xml_to_dict(self.PERSISTED_PROCESS_PROPS_XML)
        obj = PersistedProcessPropertiesAsyncResponse._unmap(parsed)
        assert isinstance(obj.result, list)
        assert len(obj.result) == 1
        props = obj.result[0]
        assert props.atom_id == "atom-1"
        assert isinstance(props.process, list)
        assert len(props.process) == 1
        assert props.process[0].process_id == "p1"

    def test_list_queues_single_queue_record(self):
        from boomi.models import ListQueuesAsyncResponse
        parsed = parse_xml_to_dict(self.LIST_QUEUES_XML)
        obj = ListQueuesAsyncResponse._unmap(parsed)
        assert isinstance(obj.result, list)
        assert len(obj.result) == 1
        queues = obj.result[0]
        assert isinstance(queues.queue_record, list)
        assert len(queues.queue_record) == 1
        assert queues.queue_record[0].queue_name == "q1"

    def test_atom_disk_space_single_directory(self):
        from boomi.models import AtomDiskSpaceAsyncResponse
        parsed = parse_xml_to_dict(self.ATOM_DISK_SPACE_XML)
        obj = AtomDiskSpaceAsyncResponse._unmap(parsed)
        assert isinstance(obj.result, list)
        assert len(obj.result) == 1
        disk = obj.result[0]
        assert isinstance(disk.disk_space_directory, list)
        assert len(disk.disk_space_directory) == 1
        assert disk.disk_space_directory[0].file == "/data"

    def test_atom_counters_single_counter(self):
        from boomi.models import AtomCounters
        parsed = parse_xml_to_dict(self.ATOM_COUNTERS_XML)
        obj = AtomCounters._unmap(parsed)
        assert obj.atom_id == "atom-1"
        assert isinstance(obj.counter, list)
        assert len(obj.counter) == 1
        assert obj.counter[0].name == "executions"
        assert obj.counter[0].value == "42"
