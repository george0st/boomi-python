# RuntimeObservabilitySettingsRequest

**Properties**

| Name                  | Type            | Required | Description |
| :-------------------- | :-------------- | :------- | :---------- |
| general_settings      | GeneralSettings | ✅       |             |
| log_settings          | LogSettings     | ✅       |             |
| metric_settings       | MetricSettings  | ✅       |             |
| runtime_id            | str             | ✅       |             |
| trace_settings        | TraceSettings   | ✅       |             |
| should_restart_plugin | bool            | ❌       |             |
