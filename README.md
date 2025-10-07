# My To-Do List App

A dark-themed Django to-do list with priority tags, due-date picker, and undo delete.

## Features

- Add, edit, delete tasks  
- Priority levels (Urgent, Important…)  
- Calendar date selector  
- Glassmorphism UI

## Setup & Run

```bash
git clone https://github.com/OfficialNafe/To-Do-List.git
cd To-Do-List
python -m venv env
env\Scripts\activate       # Windows
source env/bin/activate    # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
