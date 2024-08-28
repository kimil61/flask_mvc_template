# /app/controllers/posts_controller.py
from flask import render_template
from app import app
from app.models.models import Post

@app.route('/posts')
def posts():
    users_posts = Post.query.all()
    return render_template('posts.html', posts=users_posts)