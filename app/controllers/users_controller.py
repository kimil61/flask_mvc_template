# /app/controllers/users_controller.py
from flask import render_template
from app import app
from app.models.models import User

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
