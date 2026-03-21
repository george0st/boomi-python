# AccountCloudAttachmentSummaryBulkResponse

**Properties**

| Name     | Type                                                    | Required | Description |
| :------- | :------------------------------------------------------ | :------- | :---------- |
| response | List[AccountCloudAttachmentSummaryBulkResponseResponse] | ❌       |             |

# AccountCloudAttachmentSummaryBulkResponseResponse

**Properties**

| Name          | Type                          | Required | Description |
| :------------ | :---------------------------- | :------- | :---------- |
| result        | AccountCloudAttachmentSummary | ✅       |             |
| index         | int                           | ❌       |             |
| id\_          | str                           | ❌       |             |
| status_code   | int                           | ❌       |             |
| error_message | str                           | ❌       |             |
