# AccountCloudAttachmentPropertiesDefault

**Properties**

| Name                                      | Type                                     | Required | Description |
| :---------------------------------------- | :--------------------------------------- | :------- | :---------- |
| account_disk_usage                        | int                                      | ❌       |             |
| as2_workload                              | As2WorkloadDefault                       | ❌       |             |
| atom_input_size                           | int                                      | ❌       |             |
| atom_output_overflow_size                 | int                                      | ❌       |             |
| atom_working_overflow_size                | int                                      | ❌       |             |
| cloud_account_execution_limit             | int                                      | ❌       |             |
| cloud_account_execution_warning_offset    | int                                      | ❌       |             |
| container_id                              | str                                      | ❌       |             |
| download_runnerlogs                       | bool                                     | ❌       |             |
| enable_account_data_archiving             | bool                                     | ❌       |             |
| enable_atom_worker_warmup                 | bool                                     | ❌       |             |
| flow_control_parallel_process_type_override | FlowControlParallelProcessTypeOverrideDefault | ❌   |             |
| http_request_rate                         | int                                      | ❌       |             |
| http_workload                             | HttpWorkloadDefault                      | ❌       |             |
| listener_max_concurrent_executions        | int                                      | ❌       |             |
| max_connector_track_docs                  | int                                      | ❌       |             |
| min_numberof_atom_workers                 | int                                      | ❌       |             |
| numberof_atom_workers                     | int                                      | ❌       |             |
| queue_commit_batch_limit                  | int                                      | ❌       |             |
| queue_incoming_message_rate_limit         | int                                      | ❌       |             |
| queue_max_batch_size                      | int                                      | ❌       |             |
| queue_max_doc_size                        | int                                      | ❌       |             |
| queue_msg_throttle_rate                   | int                                      | ❌       |             |
| queue_use_file_persistence                | bool                                     | ❌       |             |
| test_mode_max_doc_bytes                   | int                                      | ❌       |             |
| test_mode_max_docs                        | int                                      | ❌       |             |
| worker_elastic_scaling_threshold          | int                                      | ❌       |             |
| worker_max_execution_time                 | int                                      | ❌       |             |
| worker_max_general_execution_time         | int                                      | ❌       |             |
| worker_max_queued_executions              | int                                      | ❌       |             |
| worker_max_running_executions             | int                                      | ❌       |             |
| worker_queued_execution_timeout           | int                                      | ❌       |             |

# As2WorkloadDefault

**Properties**

| Name            | Type | Required | Description         |
| :-------------- | :--- | :------- | :------------------ |
| GENERAL         | str  | ✅       | "GENERAL"           |
| LOWLATENCYDEBUG | str  | ✅       | "LOW_LATENCY_DEBUG" |

# FlowControlParallelProcessTypeOverrideDefault

**Properties**

| Name      | Type | Required | Description |
| :-------- | :--- | :------- | :---------- |
| NONE      | str  | ✅       | "NONE"      |
| THREADS   | str  | ✅       | "THREADS"   |
| PROCESSES | str  | ✅       | "PROCESSES" |

# HttpWorkloadDefault

**Properties**

| Name            | Type | Required | Description         |
| :-------------- | :--- | :------- | :------------------ |
| GENERAL         | str  | ✅       | "GENERAL"           |
| LOWLATENCYDEBUG | str  | ✅       | "LOW_LATENCY_DEBUG" |
| LOWLATENCY      | str  | ✅       | "LOW_LATENCY"       |
