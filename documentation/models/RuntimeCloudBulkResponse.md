# RuntimeCloudBulkResponse

**Properties**

| Name     | Type                          | Required | Description |
| :------- | :---------------------------- | :------- | :---------- |
| response | List[RuntimeCloudBulkResponseResponse] | ❌  |             |

# RuntimeCloudBulkResponseResponse

**Properties**

| Name          | Type         | Required | Description |
| :------------ | :----------- | :------- | :---------- |
| result        | RuntimeCloud | ✅       |             |
| index         | int          | ❌       |             |
| id\_          | str          | ❌       |             |
| status_code   | int          | ❌       |             |
| error_message | str          | ❌       |             |
