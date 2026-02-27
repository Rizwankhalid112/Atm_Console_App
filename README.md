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


## 📁 Project Structure
- `main.py`: Application entry point and UI loops.
- `models.py`: OOP Class definitions (Account, User, Admin).
- `admin_controller.py`: Business logic for administrative tasks.
- `data_manager.py`: JSON file handling and persistence logic.
- `data/`: Directory containing `users.json` and `admins.json`.
