# ATM Console Application 🏦

**Developer:** Muhammad Rizwan Ul Hassan  
**Position:** Associate Software Engineer  

A professional, PEP 8-compliant Python simulation of an ATM system. This project demonstrates core Software Engineering principles, including Object-Oriented Programming (OOP), Data Persistence, and robust Error Handling.

---

## 🛠️ Getting Started

### 🔑 Default Credentials
To test the administrative features and system management logic, use the following **Master Admin** credentials:

| Role | Username | Password |
| :--- | :--- | :--- |
| **System Admin** | `admin` | `1234` |

*Note: Once logged in, the System Admin can create additional Admin and User accounts.*

---

## 🚀 Key Features

### 👨‍💼 Admin Dashboard
- **User Management**: Create, Read, Update, and Delete (CRUD) user accounts.
- **Admin Management**: Manage secondary administrative roles.
- **Transaction Control**: View global logs and clear transaction histories.
- **System Limits**: Set custom withdrawal and transfer limits per user.
- **Security**: Only the Master Admin (`admin`) can reset passwords for other accounts.

### 👤 User Dashboard
- **Banking Ops**: Real-time Balance Inquiry, Deposits, and Withdrawals.
- **Funds Transfer**: Secure transfers between accounts with limit validation.
- **Transaction History**: Filterable logs for the last 7, 30, and 90 days.

---

## 📚 Core Concepts Implemented

This project fulfills the requirements for demonstrating the following Python basics:

* **Inheritance**: `User` and `Admin` classes inherit from a base `Account` class.
* **Encapsulation**: Using Class methods to manage internal state (balance, limits).
* **Data Structures**: 
    * **Lists**: Storing transaction histories.
    * **Dictionaries**: Managing user/admin records for $O(1)$ lookup.
* **Comprehensions**: Used **List Comprehension** for selective date filtering in transaction history.
* **File CRUD**: Reading and writing system data to **JSON** for persistent storage.
* **Error Handling**: Used `try/except` and conditional checks to prevent crashes from invalid inputs or insufficient funds.
* **Utility Methods**: Implemented `@staticmethod` for authentication logic.

---

## 📁 Project Structure
- `main.py`: Application entry point and UI loops.
- `models.py`: OOP Class definitions (Account, User, Admin).
- `admin_controller.py`: Business logic for administrative tasks.
- `data_manager.py`: JSON file handling and persistence logic.
- `data/`: Directory containing `users.json` and `admins.json`.
