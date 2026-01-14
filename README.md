# Webhook Receiver Service (Mini Task Option A)

A production-ready FastAPI service designed to handle webhooks with security validation, database persistence, and idempotency logic. This project was built as a technical assessment submission.

## 🚀 Features
* **Endpoint:** `POST /webhook` receiver.
* **Security:** Validates `X-Signature` headers to prevent unauthorized access.
* **Database:** Uses **SQLite** (via SQLAlchemy) to persist webhook payloads.
* **Idempotency:** Prevents duplicate processing by checking unique `event_id`s.
    * Returns `201 Created` for new events.
    * Returns `200 OK` for duplicate events (no database write).

## 🛠️ Tech Stack
* **Python 3.8+**
* **FastAPI** (Web Framework)
* **SQLAlchemy** (ORM)
* **Pydantic** (Data Validation)
* **SQLite** (Database)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Ali-Hamas/webhook-mini-task.git](https://github.com/Ali-Hamas/webhook-mini-task.git)
    cd webhook-mini-task
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

**Start the server:**
```bash
uvicorn main:app --reload
