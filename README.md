# 💸 TrackMySpend ( Expense management system )

> A full-stack personal finance dashboard built with **FastAPI**, **Streamlit**, and **MySQL** — featuring a modern dark UI, interactive Plotly charts, real-time analytics, and a clean sidebar layout.

---

## 🚀 Live Demo Preview

| Add / Update Expenses | Analytics by Category | Analytics by Month |
|---|---|---|
| 📅 Date-based entry with metric cards | 📊 Plotly bar + donut charts | 📆 Area chart with monthly trends |
| Pre-filled existing data | Percentage breakdowns + detail table | Peak month & average spend |
| Dark themed form with icons | Animated hover interactions | Sorted chronologically |

---

## 🧠 About the Project

Managing day-to-day expenses can be messy. This project solves that with a clean, modern dashboard that lets users:

- **Log** daily expenses with amounts, categories, and notes
- **Visualize** spending patterns by category with interactive Plotly charts
- **Track** monthly expense trends with an area chart and average line
- **Update** any past entry without duplicates — smart delete-then-insert logic

Built as a full-stack project to demonstrate end-to-end software development — from database design to REST APIs to a polished, production-grade frontend.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         Streamlit Frontend (Dark UI)         │
│   Sidebar | Add/Update | Category | Monthly  │
└───────────────────┬─────────────────────────┘
                    │  HTTP (REST)
                    ▼
┌─────────────────────────────────────────────┐
│            FastAPI Backend Server            │
│     GET /expenses  |  POST /analytics        │
└───────────────────┬─────────────────────────┘
                    │  mysql-connector
                    ▼
┌─────────────────────────────────────────────┐
│             MySQL Database                   │
│           expense_manager schema             │
└─────────────────────────────────────────────┘
```

---

## ✨ Features

### 🎨 Modern Dark UI
- Deep slate dark theme (`#0F172A`) with emerald green accents (`#10B981`)
- Custom CSS injected globally for buttons, tabs, inputs, and tables
- Google Fonts (`DM Sans` + `DM Mono`) for a clean, professional look
- Branded sidebar with stack tags and app description

### 📝 Expense Tracking
- Add and update up to 5 expenses per day through a styled card form
- Category icons for quick visual recognition (🏠 Rent, 🍔 Food, 🛍️ Shopping, 🎬 Entertainment, 📦 Other)
- Live metric strip showing day total, entry count, and top category
- Existing data pre-fills the form when you revisit a date — no re-entry needed

### 📊 Analytics by Category
- Select a custom date range and get a full spending breakdown
- Interactive **Plotly bar chart** showing expense percentage per category
- **Donut chart** with grand total in the center for at-a-glance share view
- Sortable detail table with totals and formatted figures
- Metric cards for total spent, top category, and number of categories

### 📆 Analytics by Month
- Automatic month-over-month summary pulled from the database
- **Plotly area chart** with line markers and a dotted average spend line
- Metric cards for all-time total, peak month, and monthly average
- Chronologically sorted monthly breakdown table

### 🔧 Backend & Infrastructure
- **Context-managed DB connections** — no connection leaks
- **Structured logging** — all operations logged to `server.log` with timestamps
- **Pytest test suite** — unit tests for core DB operations with edge case coverage

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Visualization** | Plotly |
| **Backend** | FastAPI + Uvicorn |
| **Database** | MySQL |
| **ORM / Driver** | mysql-connector-python |
| **Data Processing** | Pandas |
| **Testing** | Pytest |
| **Validation** | Pydantic v2 |
| **HTTP Client** | Requests |

---

## 📁 Project Structure

```
Project-expense-tracking/
│
├── .streamlit/
│   └── config.toml           # Dark theme configuration
│
├── backend/
│   ├── db_helper.py          # All DB operations (fetch, insert, delete, summary)
│   ├── logging_setup.py      # Reusable logging configuration
│   └── server.py             # FastAPI app with all REST endpoints
│
├── frontend/
│   ├── app.py                # Streamlit entry point — sidebar + tab layout
│   ├── add_update.py         # Add/Update expenses tab with metric cards
│   ├── analytics_by_category.py  # Category analytics — bar + donut charts
│   └── analytics_by_months.py    # Monthly analytics — area chart + table
│
├── tests/
│   ├── backend/
│   │   └── test_db_helper.py # Unit tests for DB helper functions
│   ├── frontend/             # (Frontend tests — in progress)
│   └── conftest.py           # Pytest path configuration
│
├── requirements.txt
└── README.md
```

---

## ⚡ Getting Started

### Prerequisites
- Python 3.9+
- MySQL Server running locally
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/AdarshRaj2602/TrackMySpend.git
cd TrackMySpend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up the Database
Log into MySQL and create the schema:
```sql
CREATE DATABASE expense_manager;

USE expense_manager;

CREATE TABLE expenses (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    amount       FLOAT NOT NULL,
    category     VARCHAR(50),
    notes        VARCHAR(255)
);
```

### 4. Configure Database Credentials
In `backend/db_helper.py`, update the connection settings:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="your_username",      # 👈 update this
    password="your_password",  # 👈 update this
    database="expense_manager"
)
```

### 5. Start the Backend Server
```bash
cd backend
uvicorn server:app --reload
```
The API will be live at `http://localhost:8000`
> Interactive docs available at `http://localhost:8000/docs` (Swagger UI)

### 6. Launch the Frontend
Open a **new terminal** and run:
```bash
cd frontend
streamlit run app.py
```
The app opens at `http://localhost:8501`

> ⚠️ **Both terminals must be running at the same time.** The frontend calls the backend API on every interaction.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/expenses/{expense_date}` | Fetch all expenses for a specific date |
| `GET` | `/expenses/` | Fetch monthly expense summary |
| `POST` | `/expenses/{expense_date}` | Add or update expenses for a date |
| `POST` | `/analytics/` | Get category-wise analytics for a date range |

### Example — Fetch Expenses
```bash
curl http://localhost:8000/expenses/2024-08-15
```

### Example — Get Analytics
```bash
curl -X POST http://localhost:8000/analytics/ \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2024-08-01", "end_date": "2024-08-31"}'
```

---

## 🧪 Running Tests

```bash
cd tests
pytest -v
```

Current test coverage includes:
- ✅ Fetch expenses for a valid date with correct data assertions
- ✅ Fetch expenses for an invalid/future date (expects empty result)
- ✅ Fetch expense summary for an invalid date range (expects empty result)

---

## 🔍 Key Design Decisions

**Context Manager for DB Connections**
All database access uses a `@contextmanager`, ensuring connections are always properly closed — even if an error occurs mid-operation.

**Delete-then-Insert Strategy**
Rather than complex update logic, the API deletes all expenses for a given date before inserting the new set. This keeps the code simple and prevents partial update bugs.

**Separation of Concerns**
The project cleanly separates the database layer (`db_helper.py`), API layer (`server.py`), and each UI view into its own module — making the codebase easy to navigate and extend.

**Structured Logging**
Every DB function logs its inputs using a shared `setup_logging()` utility, making debugging and monitoring straightforward in production.

**Component-based CSS**
All styling lives in a single `st.markdown()` block in `app.py` using CSS variables and data-testid selectors — keeping styles centralized and easy to update.

---

## 📈 Potential Improvements

- [ ] User authentication & multi-user support
- [ ] Budget limits with overspend alerts
- [ ] Light / Dark theme toggle
- [ ] CSV / PDF export of expense reports
- [ ] Dockerize the full stack for one-command setup
- [ ] Frontend test coverage with `pytest` + `selenium`
- [ ] Mobile responsive layout optimizations
- [ ] Environment-based config (`.env` file for DB credentials)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Adarsh Raj Verma**
- LinkedIn: https://www.linkedin.com/in/adarsh-raj-verma-99b71436a/
- Email: adarshrajverma2602@gmail.com

---

<p align="center">
  Made with ❤️ and Python
</p>
