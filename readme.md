# Flask MVC Web Application

## 프로젝트 구조

```console
/your-app
    /app
        __init__.py                 # Flask 앱과 데이터베이스 초기화
        /models
            __init__.py             # 모델 초기화 파일
            models.py               # 데이터베이스 모델 정의
        /templates
            layout.html             # 기본 레이아웃 템플릿
            users.html              # 사용자 목록 템플릿
            posts.html              # 게시물 목록 템플릿
        /controllers
            __init__.py             # 공통으로 사용될 모듈들 정의
            common_controller.py    # 기본 라우트 정의 (index 페이지 등)
            users_controller.py     # 사용자 관련 라우트 정의
            posts_controller.py     # 게시물 관련 라우트 정의
    config.py                       # Flask 설정 파일 (데이터베이스 설정 포함)
    run.py                          # 애플리케이션 실행 및 마이그레이션 적용
    migrations/                     # Flask-Migrate를 통해 생성된 마이그레이션 파일들
    README.md                       # 프로젝트 설명 파일
```

### 폴더 및 파일 설명
- **app/**: 애플리케이션의 핵심 모듈을 포함합니다.
  - **models/**: 데이터베이스 모델을 정의합니다.
  - **templates/**: HTML 템플릿 파일을 포함합니다.
  - **controllers/**: 각 기능별 라우트를 처리하는 컨트롤러를 포함합니다.
- **config.py**: 데이터베이스 연결 및 기타 환경 설정을 포함합니다.
- **run.py**: 애플리케이션을 실행하고 마이그레이션을 관리하는 파일입니다.
- **migrations/**: 데이터베이스 마이그레이션 기록이 저장되는 디렉터리입니다.

---

## 설치할 패키지들

프로젝트의 의존성을 설치하려면 아래의 명령을 실행하세요:

```bash
pip install flask flask_sqlalchemy Flask-Migrate
```

- `Flask`: Python 기반의 웹 프레임워크.
- `Flask-SQLAlchemy`: SQLAlchemy를 사용하는 Flask의 ORM 확장.
- `Flask-Migrate`: 데이터베이스 마이그레이션을 관리하기 위한 Flask 확장.

## Flask-Migrate 사용법

### 1. 마이그레이션 초기화

프로젝트에서 처음으로 마이그레이션을 설정하려면, 다음 명령어를 실행합니다:

```bash
flask db init
```

이 명령어는 `migrations/` 디렉터리를 생성하여 마이그레이션 기록을 관리합니다.

### 2. 모델 변경 사항 반영

모델에 변경 사항이 생겼다면, 이를 데이터베이스에 반영하기 위해 새로운 마이그레이션을 생성해야 합니다:

```bash
flask db migrate -m "Your migration message"
```

이 명령어는 데이터베이스 변경 사항을 추적하여 새로운 마이그레이션 파일을 생성합니다.

### 3. 마이그레이션 적용

생성된 마이그레이션 파일을 데이터베이스에 적용하려면:

```bash
flask db upgrade
```

이 명령어는 최신 마이그레이션을 데이터베이스에 적용하여 스키마를 업데이트합니다.

---

## 새로운 모델 추가 시

### 1. models.py 파일에 Tag 모델 추가

```python
from app import db

# 다대다 관계를 위한 중간 테이블 설정
post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.Text)
    
    # 다대다 관계 설정
    tags = db.relationship('Tag', secondary=post_tag, backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return f'<Post {self.title}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
```

#### 코드설명

- **`post_tag` 중간 테이블**: 이 테이블은 `post_id`와 `tag_id`를 포함하며, `Post`와 `Tag` 모델 간의 다대다 관계를 관리합니다.
  
- **`Post` 모델**: 
  - `tags` 관계를 통해 여러 태그를 가질 수 있습니다.
  - `secondary=post_tag`는 중간 테이블을 사용하여 `Post`와 `Tag`를 연결합니다.

- **`Tag` 모델**: 
  - `name` 필드는 태그의 이름을 나타내며, 고유(unique)하고 비어 있을 수 없습니다(nullable=False).
  - `Tag` 모델은 여러 `Post`와 연결될 수 있습니다.

### 2. 마이그레이션 생성 및 적용

모델을 정의한 후에는 데이터베이스에 해당 변경 사항을 반영해야 합니다:

```bash
flask db migrate -m "Added Tag model"
flask db upgrade
```

이 명령어를 통해 새로운 테이블이 생성되고, 데이터베이스 스키마가 최신 상태로 유지됩니다.

### 3. 컨트롤러 및 템플릿 추가

#### 1. 컨트롤러 추가

컨트롤러는 특정 URL에 대해 애플리케이션이 어떻게 응답할지를 정의합니다. 새로운 모델에 대한 컨트롤러를 추가하려면, `app/controllers` 디렉터리 내에 새로운 파일을 만들거나 기존 컨트롤러에 해당 로직을 추가합니다.

예를 들어, `tags_controller.py`라는 파일을 추가해보겠습니다:

```python
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
```

이 컨트롤러는 두 가지 주요 기능을 담당합니다:

- **`/tags` (GET)**: 모든 태그를 조회하여 `tags.html` 템플릿에 전달합니다.
- **`/tags/add` (POST)**: 새로운 태그를 데이터베이스에 추가하고, 여러 게시물과 관계를 맺은 후 태그 목록 페이지로 리디렉션합니다.

#### 3. 템플릿 추가

새로운 컨트롤러에서 렌더링할 템플릿 파일을 `app/templates` 디렉터리에 추가해야 합니다. 예를 들어, `tags.html`이라는 파일을 추가해보겠습니다:

```html
<!-- app/templates/tags.html -->

{% extends 'layout.html' %}

{% block content %}
    <h2>Tags</h2>
    <ul>
        {% for tag in tags %}
            <li>
                <strong>Tag:</strong> {{ tag.name }}
                <ul>
                    {% for post in tag.posts %}
                        <li>{{ post.title }}</li>
                    {% endfor %}
                </ul>
            </li>
        {% endfor %}
    </ul>

    <h3>Add a new tag</h3>
    <form action="{{ url_for('add_tag') }}" method="post">
        <label for="name">Tag Name:</label><br>
        <input type="text" name="name" id="name"><br>
        <label for="post_ids">Post IDs (comma-separated):</label><br>
        <input type="text" name="post_ids" id="post_ids"><br>
        <input type="submit" value="Add Tag">
    </form>
{% endblock %}
```

이 템플릿은 다음을 수행합니다:

- **태그 목록**: 데이터베이스에서 가져온 태그를 목록으로 표시하며, 각 태그가 연결된 게시물들도 함께 표시합니다.
- **태그 추가 폼**: 사용자로부터 새로운 태그와 연결할 게시물 ID를 입력받아 `/tags/add` 경로로 POST 요청을 보냅니다.

#### 4. 컨트롤러를 `__init__.py`에 등록

새로 만든 컨트롤러를 애플리케이션에서 사용할 수 있도록 `app/__init__.py` 파일에 등록해야 합니다.

```python
from app.controllers import common_controller, users_controller, posts_controller, tags_controller
```

이렇게 하면 애플리케이션이 실행될 때 `tags_controller.py`에 정의된 라우트들이 포함됩니다.
