🛍️ E-commerce Clothing Store :-

This is a full-stack E-commerce web application built with Django. The store is focused on selling girls' clothing and includes essential features such as user authentication, product catalog, cart functionality, order tracking, and admin dashboard.

🚀 Features :-
- 👗 Product catalog for girls' clothing
- 🛒 Add to cart and checkout functionality
- 👤 User registration and login
- 🧾 Order management
- 🛠️ Admin panel for managing products and orders
- 📦 Inventory management
- 📋 Clean UI using Django templates and static files

🧑‍💻 Tech Stack :-

| Category     | Technology         |
|--------------|--------------------|
| Backend      | Django (Python)    |
| Database     | MYSQL             |
| Frontend     | HTML, CSS, Bootstrap |
| Authentication | Django's built-in auth system |
| Admin Panel  | Django Admin       |

📁 Project Structure:- E-commerce_store/

├── shop/ # Main Django app (models, views, URLs)

├── static/ # Static files (CSS, JS, images)

├── templates/ # HTML templates

├── media/ # Uploaded product images

├── db.sqlite3 # Default database but I have used MYSQL

├── manage.py # Django management script

└── requirements.txt # Python dependencies (optional)

🔧 Installation
Follow the steps below to run the project locally:
# 1. Clone the repository
git clone https://github.com/your-username/E-commerce_store.git

cd E-commerce_store

cd girlstore

# 2. Create a virtual environment
python -m venv venv

# On Macos:
source venv/bin/activate 

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations

python manage.py migrate

# 5. Create a superuser (for admin access)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver

Then open your browser and go to :
👉 http://127.0.0.1:8000/

🛡️ Admin Panel Access
After running the server :
http://127.0.0.1:8000/admin/,
Login using the superuser credentials you created like Username and Password.
