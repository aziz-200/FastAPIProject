# 🚀 Delivery Order API — FastAPI Project

A high-performance **delivery order management REST API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. Features async request handling, custom JWT authentication with access/refresh token pairs, role-based authorization (`is_staff` guard), and full order lifecycle management — from placement to status updates and deletion.

---

## 🚀 Features

### 🔑 Authentication
- **Sign Up** — Register with username, email, and password; duplicate email/username validation enforced
- **Login** — Accepts username or email; returns access + refresh JWT token pair on success
- **Token Refresh** — Swap a valid refresh token for a new access + refresh pair
- **Custom JWT Implementation** — Hand-rolled `create_token()` / `decode_token()` using `PyJWT` with `HS256` algorithm
- **HTTPBearer Security Scheme** — FastAPI `HTTPBearer` extracts tokens from `Authorization: Bearer <token>` headers
- **Token Type Validation** — Access and refresh tokens carry a `type` claim; endpoints reject wrong token types
- **Password Hashing** — `werkzeug`'s `generate_password_hash` / `check_password_hash` for secure storage
- **AuthJWT Compatibility Wrapper** — Custom `AuthJWT` class bridges old `fastapi-jwt-auth` API with the new custom implementation seamlessly

### 📦 Orders
- **Place Order** — Authenticated users create orders by specifying product and quantity; `total_price` auto-calculated
- **My Orders** — Users retrieve all their own orders with full product and pricing details
- **My Order by ID** — Retrieve a specific order belonging to the current user
- **All Orders (Staff only)** — `is_staff` users can list every order in the system
- **Any Order by ID (Staff only)** — `is_staff` users can fetch any order by its ID
- **Update Order** — Order owner can update quantity and product (own orders only)
- **Update Order Status (Staff only)** — Staff can change order status: `Pending → IN_TRANSIT → Delivered`
- **Delete Order** — Owner can delete their own order — only if status is still `Pending`
- **Role-Based Guards** — Every sensitive endpoint checks `is_staff` flag and ownership before proceeding

### 🛠️ Infrastructure
- **FastAPI Routers** — Modular `APIRouter` setup: `auth_router` (`/auth`) and `order_router` (`/order`)
- **SQLAlchemy ORM** — Declarative models with relationships (`one-to-many`: User → Orders, Order → Product)
- **ChoiceType** — `sqlalchemy-utils` `ChoiceType` enforces valid order status values at the DB level
- **Pydantic v2 Schemas** — `BaseModel` with `model_config`, `json_schema_extra` examples, and `EmailStr` validation
- **Auto Interactive Docs** — FastAPI auto-generates **Swagger UI** at `/docs` and **ReDoc** at `/redoc`
- **DB Init Script** — `init_db.py` runs `Base.metadata.create_all()` to create all tables from models
- **`.http` Test File** — JetBrains HTTP Client test file included for quick manual endpoint testing

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.14 |
| **Framework** | FastAPI |
| **ASGI Server** | Uvicorn |
| **ORM** | SQLAlchemy + sqlalchemy-utils |
| **Database** | PostgreSQL (`psycopg2-binary`) |
| **Auth** | Custom JWT (`PyJWT`, `HS256`) + HTTPBearer |
| **Password Hashing** | Werkzeug |
| **Schema Validation** | Pydantic v2 |
| **API Docs** | Swagger UI (`/docs`) + ReDoc (`/redoc`) |
| **Package Manager** | Pipenv |

---

## 📁 Project Structure

```
FastAPIProject/
├── main.py               # FastAPI app entry point; includes routers
├── models.py             # SQLAlchemy ORM models: User, Order, Product
├── schemas.py            # Pydantic v2 schemas: SignUpModel, LoginModel, OrderModel, OrderStatusModel
├── database.py           # DB engine, session factory, get_db() dependency
├── auth_utils.py         # JWT create/decode, HTTPBearer extractor, get_current_subject()
├── auth_routes.py        # /auth router: signup, login, token refresh
├── order_routes.py       # /order router: full CRUD + status update (active version)
├── product_routes.py     # /order router: legacy version using fastapi-jwt-auth (reference)
├── init_db.py            # DB initializer: creates all tables from models
├── test_main.http        # JetBrains HTTP Client test file
└── Pipfile               # Dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/aziz-200/FastAPIProject.git
cd FastAPIProject
```

### 2. Install dependencies
```bash
pip install pipenv
pipenv install
pipenv shell
```

### 3. Configure the database

Open `database.py` and update the connection string:
```python
engine = create_engine("postgresql://your_user:your_password@localhost:5432/delivery_db")
```

Or set it via environment variable (recommended for production).

### 4. Create the PostgreSQL database
```sql
CREATE DATABASE delivery_db;
```

### 5. Initialize the database tables
```bash
python init_db.py
```

### 6. Run the development server
```bash
uvicorn main:app --reload
```

Visit:
- **Swagger UI** → `http://127.0.0.1:8000/docs`
- **ReDoc** → `http://127.0.0.1:8000/redoc`

---

## 📦 Dependencies

```
fastapi
uvicorn
sqlalchemy
sqlalchemy-utils
psycopg2-binary
werkzeug
pydantic
pyjwt
fastapi-jwt-auth
fastapi-jwt-auth2
```

Install all:
```bash
pipenv install
```

---

## 🔐 Authentication Flow

```
Step 1 — Register
  POST /auth/signup
  Body: { "username": "aziz", "email": "aziz@example.com", "password": "..." }
  ← Returns: { success, message, data: { id, username, email, is_staff, is_active } }

Step 2 — Login
  POST /auth/login
  Body: { "username_or_email": "aziz", "password": "..." }
  ← Returns: { access: "<token>", refresh: "<token>" }

Step 3 — Use access token
  GET /order/user/orders
  Header: Authorization: Bearer <access_token>

Step 4 — Refresh token when expired
  GET /auth/login/refresh
  Header: Authorization: Bearer <refresh_token>
  ← Returns: { access_token, refresh_token }
```

**Token lifetimes:**
- Access token: `60 minutes`
- Refresh token: `3 days`

---

## 📌 API Endpoints

### 🔑 Auth (`/auth/`)

| Method | Endpoint | Auth | Request Body | Response |
|---|---|---|---|---|
| `POST` | `/auth/signup` | ❌ | `{ username, email, password, is_staff?, is_active? }` | `{ success, code: 201, message, data: { id, username, email } }` |
| `POST` | `/auth/login` | ❌ | `{ username_or_email, password }` | `{ success, code: 200, data: { access, refresh } }` |
| `GET` | `/auth/login/refresh` | ✅ Refresh token | — | `{ success, data: { access_token, refresh_token } }` |
| `GET` | `/auth/` | ✅ Access token | — | Welcome message |

---

### 📦 Orders (`/order/`)

| Method | Endpoint | Auth | Role | Request Body | Response |
|---|---|---|---|---|---|
| `POST` | `/order/make` | ✅ | Any user | `{ quantity, product_id }` | `{ id, product, quantity, order_status, total_price }` |
| `GET` | `/order/user/orders` | ✅ | Any user | — | List of own orders with product details |
| `GET` | `/order/user/order/{id}` | ✅ | Any user (owner) | — | Single own order detail |
| `PUT` | `/order/{id}/update` | ✅ | Owner only | `{ quantity, product_id }` | Updated order object |
| `DELETE` | `/order/{id}/delete` | ✅ | Owner only (Pending status) | — | `{ success, message }` |
| `GET` | `/order/list` | ✅ | Staff only | — | All orders in the system |
| `GET` | `/order/{id}` | ✅ | Staff only | — | Any order by ID |
| `PATCH` | `/order/{id}/update-status` | ✅ | Staff only | `{ order_status }` | `{ id, order_status }` |
| `GET` | `/order/` | ✅ | Any user | — | Welcome message |

---

### 📦 Sample Response — POST `/auth/login`

```json
{
  "success": true,
  "code": 200,
  "message": "User successfully login",
  "data": {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### 📦 Sample Response — POST `/order/make`

```json
{
  "success": true,
  "code": 201,
  "message": "Order is created successfully",
  "data": {
    "id": 5,
    "product": {
      "id": 2,
      "name": "Laptop",
      "price": 1200
    },
    "quantity": 3,
    "order_statuses": "Pending",
    "total_price": 3600
  }
}
```

### 📦 Sample Response — GET `/order/user/orders`

```json
[
  {
    "id": 5,
    "user": {
      "id": 1,
      "username": "aziz",
      "email": "aziz@example.com"
    },
    "product": {
      "id": 2,
      "name": "Laptop",
      "price": 1200
    },
    "quantity": 3,
    "order_statuses": "Pending",
    "total_price": 3600
  }
]
```

---

## 🗄️ Data Models

### User
| Field | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `username` | String(25) | Unique |
| `email` | String(70) | Unique |
| `password` | Text | Hashed with werkzeug |
| `is_staff` | Boolean | Default `False` — staff/admin flag |
| `is_active` | Boolean | Default `False` |
| `orders` | relationship | One-to-many → Order |

### Order
| Field | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `quantity` | Integer | Required |
| `order_status` | ChoiceType | `Pending` / `IN_TRANSIT` / `Delivered` |
| `user_id` | FK → User | |
| `product_id` | FK → Product | |

### Product
| Field | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto-increment |
| `name` | String(25) | Unique |
| `price` | Integer | Required |
| `orders` | relationship | One-to-many → Order |

---

## 🔄 Order Status Lifecycle

```
[Pending]  →  [IN_TRANSIT]  →  [Delivered]
    ↑
  Only deletable at this stage
  (Staff updates status; owner deletes only if Pending)
```

---

## 👤 Author

**Aziz** — [github.com/aziz-200](https://github.com/aziz-200)
