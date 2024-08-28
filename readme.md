
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

## 새로운 모델 추가 시

### 1. 모델 정의

새로운 모델을 추가하려면 `app/models/models.py` 파일에 클래스를 정의하세요. 예를 들어, `Comment` 모델을 추가하려면:

```python
class Comment(db.Model):
    __tablename__ = 'comments'  # 테이블 이름을 명시적으로 지정
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment {self.content[:20]}>'
```

### 2. 마이그레이션 생성 및 적용

모델을 정의한 후에는 데이터베이스에 해당 변경 사항을 반영해야 합니다:

```bash
flask db migrate -m "Added Comment model"
flask db upgrade
```

이 명령어를 통해 새로운 테이블이 생성되고, 데이터베이스 스키마가 최신 상태로 유지됩니다.

### 3. 컨트롤러 및 템플릿 추가 (선택 사항)

새로운 모델을 추가하고, 이를 처리하거나 사용자에게 보여주기 위해서는 새로운 컨트롤러와 템플릿을 추가해야 할 수 있습니다. 여기서는 `Comment` 모델을 예시로 설명하겠습니다.

#### 1. 컨트롤러 추가

컨트롤러는 특정 URL에 대해 애플리케이션이 어떻게 응답할지를 정의합니다. 새로운 모델에 대한 컨트롤러를 추가하려면, `app/controllers` 디렉터리 내에 새로운 파일을 만들거나 기존 컨트롤러에 해당 로직을 추가합니다.

예를 들어, `comments_controller.py`라는 파일을 추가해보겠습니다:

```python
# app/controllers/comments_controller.py

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models.models import Comment

@app.route('/comments', methods=['GET'])
def comments():
    all_comments = Comment.query.all()
    return render_template('comments.html', comments=all_comments)

@app.route('/comments/add', methods=['POST'])
def add_comment():
    content = request.form['content']
    user_id = request.form['user_id']
    post_id = request.form['post_id']
    
    new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('comments'))
```

이 컨트롤러는 두 가지 주요 기능을 담당합니다:

- **`/comments` (GET)**: 모든 댓글을 조회하여 `comments.html` 템플릿에 전달합니다.
- **`/comments/add` (POST)**: 새로운 댓글을 데이터베이스에 추가한 후, 댓글 목록 페이지로 리디렉션합니다.

#### 2. 템플릿 추가

새로운 컨트롤러에서 렌더링할 템플릿 파일을 `app/templates` 디렉터리에 추가해야 합니다. 예를 들어, `comments.html`이라는 파일을 추가해보겠습니다:

```html
<!-- app/templates/comments.html -->

{% extends 'layout.html' %}

{% block content %}
    <h2>Comments</h2>
    <ul>
        {% for comment in comments %}
            <li>
                <strong>Comment:</strong> {{ comment.content }}<br>
                <em>By User ID:</em> {{ comment.user_id }} on Post ID: {{ comment.post_id }}
            </li>
        {% endfor %}
    </ul>

    <h3>Add a new comment</h3>
    <form action="{{ url_for('add_comment') }}" method="post">
        <label for="content">Content:</label><br>
        <textarea name="content" id="content"></textarea><br>
        <label for="user_id">User ID:</label><br>
        <input type="number" name="user_id" id="user_id"><br>
        <label for="post_id">Post ID:</label><br>
        <input type="number" name="post_id" id="post_id"><br>
        <input type="submit" value="Add Comment">
    </form>
{% endblock %}
```

이 템플릿은 다음을 수행합니다:

- **댓글 목록**: 데이터베이스에서 가져온 댓글을 목록으로 표시합니다.
- **댓글 추가 폼**: 사용자로부터 새로운 댓글을 입력받아 `/comments/add` 경로로 POST 요청을 보냅니다.

#### 3. 컨트롤러를 `__init__.py`에 등록

새로 만든 컨트롤러를 애플리케이션에서 사용할 수 있도록 `app/__init__.py` 파일에 등록해야 합니다.

```python
from app.controllers import comments_controller
```

이렇게 하면 애플리케이션이 실행될 때 `comments_controller.py`에 정의된 라우트들이 포함됩니다.

---

### 요약

- **컨트롤러 파일**: 새로운 모델에 대응하는 비즈니스 로직과 URL 라우트를 정의합니다. 이 파일은 `app/controllers` 디렉터리에 위치시킵니다.
- **템플릿 파일**: 데이터를 사용자에게 보여주기 위한 HTML 파일을 작성합니다. 이 파일은 `app/templates` 디렉터리에 위치시킵니다.
- **컨트롤러 등록**: 새로운 컨트롤러 파일을 `app/__init__.py`에 등록하여 애플리케이션이 이를 인식하고 사용할 수 있게 합니다.

이 과정을 통해 새로운 모델과 상호작용할 수 있는 기능을 추가하고, 이를 사용자 인터페이스에 반영할 수 있습니다.