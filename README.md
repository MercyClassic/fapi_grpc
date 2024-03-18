**<h2> Startup: </h2>**
- **<h3> Create .env files in `main_service` and `log_service` </h3>**
- **<h3> `docker compose up -d && docker logs -f log_service_consumer` </h3>**

***<h3>[\*Examples after `About project` section](#examples) </h3>***

**<h1> About project: </h1>**
**<h3> In service you can create json "file" and get it data if file doesn't have forbidden keys</h3>**
**<h3> File creation steps: </h3>**
- **<h3> Save file in main microservice db (`postgresql`)  </h3>**
- **<h3> `grpc` request to log microservice </h3>**
- **<h3> Save file in log microservice db (`mongo`) </h3>**
- **<h3> Send process request to `kafka` </h3>**
- **<h3> Process request </h3>**
- **<h3> Send `update file status` request by result of processing </h3>**

**<h3> About processing: </h3>**
- **<h4> Logging file data, current date </h4>**
- **<h4> Random async sleep (7-12 seconds) </h4>**
- **<h4> Check all keys in file data: </h4>**
- - **<h4> If any key in "error" keys, then file `status = failed` </h4>**
- - **<h4> Otherwise file `status = success` </h4>**

**<h4> Error keys: `('error', 'forbidden')` </h4>**
**<h4> Warning keys: `('warning', 'warn', 'deprecated')` </h4>**

**<h2> Log microservice provides: </h2>**
- **<h3> Create json file (`grpc`) and send process request to `kafka` consumer</h3>**
- **<h3> Process logging </h3>**
- **<h3> Get json file data (`grpc`) </h3>**

**<h3> Log microservice stack: </h3>**
- **<h4> Python 3.11 </h4>**
- **<h4> grpc </h4>**
- **<h4> AioKafka </h4>**
- **<h4> MongoDB </h4>**
- **<h4> Odmantic (ODM) </h4>**

**<h2> Main microservice provides: </h2>**
- **<h3> Create json file (`grpc` request to log service) </h3>**
- **<h3> Get all json files (uuid, status) </h3>**
- **<h3> Get json file detail. If file doesn't have "error" keys (`status = success`) then data will be attached to this file </h3>**
- **<h3> Update file status. It's api for `log service` </h3>**

**<h3> Main microservice stack: </h3>**
- **<h4> Python 3.11 </h4>**
- **<h4> grpc </h4>**
- **<h4> FastAPI </h4>**
- **<h4> PostgreSQL </h4>**
- **<h4> SQLAlchemy </h4>**

## Examples:

**<h2> #1 </h2>**
`request data: `
```json
{
  "data": {
    "some_key": "some_value"
  }
}
```

`log output`:
```
[INFO] - Processing file with uuid: 5a6939af-d91f-46a4-8f29-ca7a8f5e7e28
UTC time: 2024-03-18 22:10:28
Moscow time: 2024-03-19 01:10:28
File data: {
    "some_key": "some_value"
}

[INFO] - File [5a6939af-d91f-46a4-8f29-ca7a8f5e7e28] process finished. Sleep time: 7 seconds, status: success
```

`get_file endpoint`
```json
{
  "uuid": "5a6939af-d91f-46a4-8f29-ca7a8f5e7e28",
  "status": "success",
  "data": {
    "some_key": "some_value"
  }
}
```

**<h2> #2 </h2>**
`request data`
```json
{
  "data": {
    "foo": "bar",
    "baz": {
        "nested_foo": "nested_bar",
        "deprecated": "deprecated_value"
    }
  }
}
```

`log output:`
```
[INFO] - Processing file with uuid: 47962bf0-1131-40bd-b6fc-f72ea679ec0c
UTC time: 2024-03-18 22:17:36
Moscow time: 2024-03-19 01:17:36
File data: {
    "uuid": "47962bf0-1131-40bd-b6fc-f72ea679ec0c",
    "status": "success",
    "data": {
        "foo": "bar",
        "baz": {
            "nested_foo": "nested_bar",
            "deprecated": "deprecated_value"
        }
    }
}
[WARNING]: File [47962bf0-1131-40bd-b6fc-f72ea679ec0c] - Key "deprecated" in WARNING keys
[INFO] - File [47962bf0-1131-40bd-b6fc-f72ea679ec0c] process finished. Sleep time: 12 seconds, status: success
```

`get_file endpoint`
```json
{
  "uuid": "47962bf0-1131-40bd-b6fc-f72ea679ec0c",
  "status": "success",
  "data": {
    "foo": "bar",
    "baz": {
      "nested_foo": "nested_bar",
      "deprecated": "deprecated_value"
    }
  }
}
```

**<h2> #3 </h2>**
`request data`
```json
{
  "data": {
    "foo": "bar",
      "baz": {
          "nested_foo": "nested_bar",
          "another_nested_foo": {
              "error": "error_value"
          }
      }
  }
}
```

`log output:`
```
[INFO] - Processing file with uuid: 1ec47941-7336-408e-a34e-8d46e919d579
UTC time: 2024-03-18 22:22:41
Moscow time: 2024-03-19 01:22:41
File data: File data: {
    "foo": "bar",
    "baz": {
        "nested_foo": "nested_bar",
        "another_nested_foo": {
            "error": "error_value"
        }
    }
}

[ERROR]: File [1ec47941-7336-408e-a34e-8d46e919d579] - Key "error" in ERROR keys, process failed
[INFO] - File [1ec47941-7336-408e-a34e-8d46e919d579] process finished. Sleep time: 10 seconds, status: failed
```

`get_file endpoint`
```json
{
  "uuid": "1ec47941-7336-408e-a34e-8d46e919d579",
  "status": "failed",
  "data": null
}
```
