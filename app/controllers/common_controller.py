# /app/controllers/common_controller.py
from flask import render_template
from app import app
from app.models.models import User

@app.route('/')
def index():
    return render_template('index.html')
