# AtomLogService

A list of all methods in the `AtomLogService` service. Click on the method name to view detailed information about that method.

| Methods                             | Description                                                                       |
| :---------------------------------- | :-------------------------------------------------------------------------------- |
| [create_atom_log](#create_atom_log)     | You can use the Download Atom Log operation to request and download Runtime logs. |
| [download_atom_log](#download_atom_log) | Request and download Runtime logs.                                                |

## create_atom_log

You can use the Download Atom Log operation to request and download Runtime logs.

- HTTP Method: `POST`
- Endpoint: `/AtomLog`

**Parameters**

| Name         | Type                            | Required | Description       |
| :----------- | :------------------------------ | :------- | :---------------- |
| request_body | [AtomLog](../models/AtomLog.md) | ❌       | The request body. |

**Return Type**

`LogDownload`

**Example Usage Code Snippet**

```python
from boomi import Boomi
from boomi.models import AtomLog

sdk = Boomi(
    access_token="YOUR_ACCESS_TOKEN",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account_id="YOUR_ACCOUNT_ID",
    timeout=10000
)

request_body = AtomLog(
    atom_id="3456789a-bcde-f012-3456-789abcdef012",
    include_bin="true",
    log_date="2016-02-05"
)

result = sdk.atom_log.create_atom_log(request_body=request_body)

print(result)
```

## download_atom_log

Request and download Runtime logs.

- HTTP Method: `POST`, followed by polling the returned download URL
- Endpoint: `/AtomLog`

**Parameters**

| Name          | Type                            | Required | Description                                 |
| :------------ | :------------------------------ | :------- | :------------------------------------------ |
| request_body  | [AtomLog](../models/AtomLog.md) | ❌       | The request body.                           |
| max_retries   | int                             | ❌       | Maximum number of polling attempts.         |
| initial_delay | float                           | ❌       | Initial delay in seconds between retries.   |

**Return Type**

`bytes`

**Example Usage Code Snippet**

```python
from boomi import Boomi
from boomi.models import AtomLog

sdk = Boomi(
    access_token="YOUR_ACCESS_TOKEN",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    account_id="YOUR_ACCOUNT_ID",
    timeout=10000
)

request_body = AtomLog(
    atom_id="3456789a-bcde-f012-3456-789abcdef012",
    include_bin="true",
    log_date="2016-02-05"
)

content = sdk.atom_log.download_atom_log(request_body=request_body)

print(len(content))
```
