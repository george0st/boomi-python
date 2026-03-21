# AtomWorkerLogService

A list of all methods in the `AtomWorkerLogService` service. Click on the method name to view detailed information about that method.

| Methods                                           | Description                                                                                   |
| :------------------------------------------------ | :-------------------------------------------------------------------------------------------- |
| [create_atom_worker_log](#create_atom_worker_log)     | Allows users to programmatically retrieve a link for downloading a given Runtime workers log. |
| [download_atom_worker_log](#download_atom_worker_log) | Request and download Runtime worker logs.                                                 |

## create_atom_worker_log

Allows users to programmatically retrieve a link for downloading a given Runtime workers log.

- HTTP Method: `POST`
- Endpoint: `/AtomWorkerLog`

**Parameters**

| Name         | Type                                        | Required | Description       |
| :----------- | :------------------------------------------ | :------- | :---------------- |
| request_body | [AtomWorkerLog](../models/AtomWorkerLog.md) | ❌       | The request body. |

**Return Type**

`LogDownload`

**Example Usage Code Snippet**

```python
from boomi import Boomi
from boomi.models import AtomWorkerLog

sdk = Boomi(
    access_token="YOUR_ACCESS_TOKEN",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account_id="YOUR_ACCOUNT_ID",
    timeout=10000
)

request_body = AtomWorkerLog(
    worker_id="workerId"
)

result = sdk.atom_worker_log.create_atom_worker_log(request_body=request_body)

print(result)
```

## download_atom_worker_log

Request and download Runtime worker logs.

- HTTP Method: `POST`, followed by polling the returned download URL
- Endpoint: `/AtomWorkerLog`

**Parameters**

| Name          | Type                                        | Required | Description                               |
| :------------ | :------------------------------------------ | :------- | :---------------------------------------- |
| request_body  | [AtomWorkerLog](../models/AtomWorkerLog.md) | ❌       | The request body.                         |
| max_retries   | int                                         | ❌       | Maximum number of polling attempts.       |
| initial_delay | float                                       | ❌       | Initial delay in seconds between retries. |

**Return Type**

`bytes`

**Example Usage Code Snippet**

```python
from boomi import Boomi
from boomi.models import AtomWorkerLog

sdk = Boomi(
    access_token="YOUR_ACCESS_TOKEN",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account_id="YOUR_ACCOUNT_ID",
    timeout=10000
)

request_body = AtomWorkerLog(
    worker_id="workerId"
)

content = sdk.atom_worker_log.download_atom_worker_log(request_body=request_body)

print(len(content))
```
