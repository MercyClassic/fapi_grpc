

# JSON Processing Microservices Example

This project demonstrates a **two-microservice architecture** for processing JSON documents.
The **Main Service** receives JSON files, sends them for processing to the **Log Service**, which logs the data and updates the file status depending on its contents.
---

[\*Examples after `About project` section](#examples)

---

## 🏗 Project Overview

- **Main Service**:
  - Receives JSON documents via HTTP.
  - Stores documents in a PostgreSQL database.
  - Sends documents to the Log Service for processing.
  - Exposes endpoints to fetch all files and individual file details.

- **Log Service**:
  - Receives processing requests via Kafka.
  - Logs JSON file data with timestamps.
  - Checks keys in the JSON document:
    - If any **error keys** are present → `status = failed`.
    - Otherwise → `status = success`.
  - Updates status back in Main Service via gRPC.
  - Stores logs in MongoDB.

- **Processing Behavior**:
  - Logs file data and timestamps.
  - Random async sleep between 7–12 seconds to simulate processing.
  - Recognizes **error keys** (`error`, `forbidden`) and **warning keys** (`warning`, `warn`, `deprecated`).

---

## ⚙️ Technology Stack

**Main Service**:
- Python 3.11
- FastAPI
- gRPC
- PostgreSQL
- SQLAlchemy

**Log Service**:
- Python 3.11
- gRPC
- AioKafka
- MongoDB
- Odmantic (ODM)

**Common**:
- Docker & Docker Compose
- Alembic for migrations
- Poetry for dependency management

---

## 🚀 Startup

1. Create `.env` files in both `main_service` and `log_service`.
2. Start services with Docker Compose:

```bash
docker compose up -d
docker logs -f log_service_consumer
```

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
