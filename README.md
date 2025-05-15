# Inventory Management System

## Overview
This is a web-based Inventory Management System built with Flask. It allows users to manage products, locations (warehouses), and track inventory movements between locations. The application provides a user-friendly interface for adding, editing, and viewing products, locations, and inventory transactions, as well as generating balance reports.

## Features
- **Product Management:** Add, edit, view, and list products with descriptions.
- **Location Management:** Add, edit, view, and list storage locations (warehouses).
- **Inventory Movements:** Record and track product movements between locations, ensuring stock consistency.
- **Balance Report:** View current stock levels of all products at all locations.
- **Validation:** Prevents negative stock and duplicate IDs, and ensures valid movement operations.
- **Responsive UI:** Built with Bootstrap for modern, responsive design.

## Technology Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-WTF
- **Frontend:** HTML, Bootstrap, JavaScript (with DataTables)
- **Database:** SQLite (default, can be changed)

## Directory Structure
```
.
├── app.py                # Main Flask application
├── models.py             # Database models (Product, Location, ProductMovement)
├── forms.py              # WTForms classes for forms
├── inventory.db          # SQLite database file
├── static/               # Static assets (CSS, JS)
│   ├── css/style.css     # Custom styles
│   └── js/script.js      # Custom scripts
├── templates/            # HTML templates
│   ├── base.html         # Base layout
│   ├── index.html        # Home page
│   ├── product/          # Product-related templates
│   ├── location/         # Location-related templates
│   ├── movement/         # Movement-related templates
│   └── report/           # Report templates
└── README.md             # Project documentation
```

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd inventory_app
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-WTF WTForms
   ```
4. **Run the application:**
   ```bash
   python app.py
   ```
5. **Access the app:**
   Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
- Use the navigation bar to access Products, Locations, Movements, and Reports.
- Add new products and locations before recording movements.
- Use the Balance Report to view current stock at each location.

## Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- WTForms
- (Optional) DataTables (via CDN in templates)

## Database
- The app uses SQLite by default (`inventory.db`). Tables are created automatically on first run.

## Customization
- To use a different database, update the `SQLALCHEMY_DATABASE_URI` in `app.py`.
- Static assets can be customized in `static/css/style.css` and `static/js/script.js`.

## Application Screenshots
-You can see it in screenshots folder
---

