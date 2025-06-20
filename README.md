# Digital Asset Management System

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/MySQL-8.0%2B-orange" alt="MySQL Version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</div>

---

## 📌 Table of Contents
1. [Features](#-features)
2. [Prerequisites](#-prerequisites)
3. [Installation](#-installation)
4. [Database Setup](#-database-setup)
5. [Running the Application](#-running-the-application)
6. [Usage Guide](#-usage-guide)
7. [Testing](#-testing)
8. [Project Structure](#-project-structure)
9. [Troubleshooting](#-troubleshooting)
10. [Roadmap](#-roadmap)
11. [License](#-license)

---

## ✨ Features

| Feature              | Description                                      |
|----------------------|--------------------------------------------------|
| 🔐 **Authentication** | Admin/Employee roles with secure password hashing |
| 🏷️ **Asset Management** | Full CRUD operations for assets                  |
| 📊 **Allocation System** | Track asset assignments and reservations        |
| 🔧 **Maintenance**     | Record and track maintenance activities         |
| 📈 **Reporting**       | Generate various asset reports                  |

---

## ⚙️ Prerequisites

- **Python 3.8+**
- **MySQL Server 8.0+**
- **pip** (Python package manager)

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/asset-management-system.git
cd asset-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

#### Activate Environment

**Windows:**
```cmd
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🗃️ Database Setup

### 1. Create MySQL Database
```sql
CREATE DATABASE asset_management_db;
```

### 2. Initialize Schema
```bash
mysql -u root -p asset_management < schema.sql
```

### 3. Configure Connection

Edit `config.properties`:

```ini
[Database]
host=localhost
database=asset_management_db
user=your_username
password=your_password
```

---

## 🚀 Running the Application

```bash
python -m assets.main.main_module
```

### Default Credentials

| Role   | Email              | Password |
|--------|--------------------|----------|
| Admin  | admin@company.com  | secret   |

---
## 📂 Sample Data

Pre-populated sample data is available to help you test the system. The dataset includes:

### Employees
| Name    | Department | Email                   | Password   | Role    |
|---------|------------|-------------------------|------------|---------|
| Ruthra  | AIML       | ruthra@company.com    | password123| Employee|
| Varshan | HR         | varshan@company.com  | password123| Employee|

### Assets
| Name             | Type    | Status           | Assigned To     |
|------------------|---------|------------------|-----------------|
| MacBook Pro 16"  | Laptop  | In Use           | John Doe        |
| Canon EOS R5     | Camera  | In Use           | Jane Smith      |
| Dell XPS 15      | Laptop  | Decommissioned   | Unassigned      |

### How to Load Sample Data

**Using Python Script**:
```bash
   python -m assets.tests.insert_sample_data
````
--- 

## 💻 Usage Guide

### Admin Functions

```
1. Asset Management → Add/Edit/Delete assets  
2. User Management → Create/Manage employees  
3. Approvals → Review reservations/maintenance  
```

### Employee Functions
```
1. My Assets → View allocated assets  
2. Requests → Reserve assets/report issues  
3. Profile → Update personal details  
```

---

## 🧪 Testing

### Run Test Suite
```bash
pytest tests/
```

### Test Coverage
- Asset operations
- User authentication
- Maintenance tracking
- Exception handling

---

## 📂 Project Structure

```
asset-management/
├── assets/
│   ├── entity/        # Data models
│   ├── dao/           # Database operations
│   ├── exception/     # Custom exceptions
│   ├── util/          # Utilities
│   ├── main/          # Application entry
│   └── tests/         # Unit tests
├── schema.sql         # DB schema
├── config.properties  # Configuration
└── requirements.txt   # Dependencies
```

---

## 🛠 Troubleshooting

| Error              | Solution                               |
|--------------------|----------------------------------------|
| Connection failed  | Verify MySQL service and credentials   |
| Import errors      | Check Python path and virtual env      |
| Login failures     | Confirm user exists in database        |

---

## 🗺 Roadmap

- Web interface
- Email notifications
- Barcode integration
- Dashboard analytics

---

## 📜 License

**MIT License © 2025**
