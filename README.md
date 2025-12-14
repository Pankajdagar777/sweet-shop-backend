# 🍬 Sweet Shop Management System – Backend

A RESTful backend for a **Sweet Shop Management System** built using **Django** and **Django REST Framework**.  
This backend serves as the core of the application, handling authentication, sweet inventory management, purchasing, restocking, and admin-level controls.

---

## 🚀 Features

### 🔐 Authentication
- User Registration
- User Login using JWT (JSON Web Tokens)
- Secure token-based authentication
- Role-based access control (Admin vs Normal User)

---

### 🍭 Sweet Management
- Add sweets (**Admin only**)
- View list of all available sweets
- Update sweet details (**Admin only**)
- Delete sweets (**Admin only**)

Each sweet contains:
- Unique ID
- Name
- Category
- Price
- Quantity in stock

---

### 🛒 Inventory Operations
- Purchase sweets (decreases quantity dynamically)
- Prevent purchase when stock is zero
- Restock sweets with custom quantity (**Admin only**)

---

### 🔍 Search & Filter
- Search sweets by name
- Filter sweets by category

---

## 🛠 Tech Stack

- **Backend Framework:** Django
- **API Framework:** Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **Database:** SQLite (easily replaceable with PostgreSQL/MySQL)
- **Language:** Python 3

---


## My AI Usage (Mandatory)
🔧 AI Tools Used

ChatGPT (OpenAI)

🧠 How I Used AI

To understand Django REST Framework concepts clearly

To brainstorm API endpoint structures

To generate initial boilerplate code for:

Views

Serializers

JWT authentication setup

To debug runtime errors and logic issues

To refine business logic (purchase, restock, permissions)

To improve code readability and structure

---

## ⚙️ Setup Instructions (Run Locally)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Pankajdagar777/sweet-shop-backend.git
cd sweet-shop-backend
