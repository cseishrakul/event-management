# 🎉 Event Management System (Django)

## 📄 Description  
This is a full-featured **Event Management System** built using **Django's MVT architecture**. It supports multiple user roles including **Admin**, **Organizer**, and **Participant**. Organizers can create and manage events, while participants can browse and attend them. The admin has full control over users, events, and system settings.

---

## 🚀 Features  
- Role-based access: Admin, Organizer, Participant  
- Organizer dashboard to create and manage events  
- Participant panel to view and attend events  
- Admin panel for full control of users, events, and data  
- Clean and responsive frontend built with CSS  
- Secure authentication and authorization system  

---

## 🛠️ Technologies Used  
- **Backend:** Django (Python) using MVT pattern  
- **Frontend:** HTML, CSS  
- **Database:** PostgreSQL  

---

## 👥 Roles & Permissions  

| Role        | Capabilities                                |
|-------------|---------------------------------------------|
| Admin       | Manage all users, events, and system config |
| Organizer   | Create and manage their own events          |
| Participant | Browse and attend events                    |

---

## 🧑‍💻 Local Setup Instructions

To run this project locally, follow these steps:
# 1. Clone the repository
git clone https://github.com/cseishrakul/event-management.git
cd event-management

# 2. Create and activate virtual environment
python -m venv event_env
# On Windows:
event_env\Scripts\activate
# On Mac/Linux:
source event_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver

# 7. Open in browser
# Visit: http://127.0.0.1:8000
