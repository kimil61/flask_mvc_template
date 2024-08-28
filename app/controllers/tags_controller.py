# app/controllers/tags_controller.py

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models.models import Tag, Post

@app.route('/tags', methods=['GET'])
def tags():
    all_tags = Tag.query.all()
    return render_template('tags.html', tags=all_tags)

@app.route('/tags/add', methods=['POST'])
def add_tag():
    name = request.form['name']
    post_ids = request.form.getlist('post_ids')  # 여러 게시물 ID를 받기 위해 getlist 사용
    
    new_tag = Tag(name=name)
    for post_id in post_ids:
        post = Post.query.get(post_id)
        if post:
            new_tag.posts.append(post)
    
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect(url_for('tags'))