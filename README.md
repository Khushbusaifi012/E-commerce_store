🛍️ E-commerce Clothing Store :-

This is a full-stack E-commerce web application built with Django. The store is focused on selling girls' clothing and includes essential features such as user authentication, product catalog, cart functionality, order tracking, and admin dashboard.

🚀 Features :-
- 👗 Product catalog for girls' clothing
- 🛒 Add to cart and checkout functionality
- 👤 User registration and login
- 🧾 Order management
- 🛠️ Admin panel for managing products and orders
- 📋 Clean UI using Django templates, Tailwind (CDN), and static files

🧑‍💻 Tech Stack :-

| Category     | Technology         |
|--------------|--------------------|
| Backend      | Django (Python)    |
| Database     | MySQL **or** SQLite (see below) |
| Frontend     | HTML, Tailwind CDN, Django templates |
| Authentication | Django's built-in auth system |
| Admin Panel  | Django Admin       |

📁 Project Structure (inside `E-commerce_store/girlstore/`)

```
girlstore/
├── manage.py
├── requirements.txt
├── .env.example          # copy to .env (not committed)
├── shop/                 # Django app (models, views, URLs)
├── girlstore/            # project settings (settings.py, urls.py)
├── static/               # CSS, JS, images
├── templates/            # HTML templates
└── media/                # uploaded product images (local)
```

🔧 Installation

Follow the steps below to run the project locally:

```bash
# 1. Clone the repository (use your fork URL if different)
git clone https://github.com/your-username/E-commerce_store.git
cd E-commerce_store/girlstore

# 2. Create & activate virtual environment (Windows vs macOS/Linux)
python -m venv venv
# macOS/Linux: source venv/bin/activate
# Windows:       venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

Then open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

🛡️ Admin panel

Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and sign in with the superuser you created.
