# CloudAttachmentSecretsConfigurationService

A list of all methods in the `CloudAttachmentSecretsConfigurationService` service. Click on the method name to view detailed information about that method.

| Methods                                                                                             | Description                                                                    |
| :-------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| [create_cloud_attachment_secrets_configuration](#create_cloud_attachment_secrets_configuration)     | Creates a CloudAttachmentSecretsConfiguration for the specified container.     |

## create_cloud_attachment_secrets_configuration

Creates a CloudAttachmentSecretsConfiguration for the specified container.

- HTTP Method: `POST`
- Endpoint: `/cloudAttachmentSecretsConfiguration/{containerId}`

**Parameters**

| Name           | Type                                                                                                            | Required | Description       |
| :------------- | :-------------------------------------------------------------------------------------------------------------- | :------- | :---------------- |
| request_body   | [CloudAttachmentSecretsConfigurationRequest](../models/CloudAttachmentSecretsConfigurationRequest.md)           | ❌       | The request body. |
| container_id   | str                                                                                                             | ✅       | The container ID. |

**Return Type**

`CloudAttachmentSecretsConfigurationResponse`

**Example Usage Code Snippet**

```python
from boomi import Boomi
from boomi.models import CloudAttachmentSecretsConfigurationRequest

sdk = Boomi(
    access_token="YOUR_ACCESS_TOKEN",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account_id="YOUR_ACCOUNT_ID",
    timeout=10000
)

request_body = CloudAttachmentSecretsConfigurationRequest(
    container_id="containerId",
    secrets_manager_provider={
        "aws": {
            "aws_access_key_id": "AKIA...",
            "aws_region": "us-east-1",
            "aws_secret_access_key": "secret",
        }
    },
)

result = sdk.cloud_attachment_secrets_configuration.create_cloud_attachment_secrets_configuration(
    request_body=request_body,
    container_id="containerId"
)

print(result)
```
