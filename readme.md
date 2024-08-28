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

새로운 모델을 추가하려면 `app/models/models.py` 파일에 클래스를 정의하세요. 예를 들어, `Tag` 모델을 추가하려면:

```python
class Tag(db.Model):
    __tablename__ = 'tags'  # 테이블 이름을 명시적으로 지정
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Tag {self.name}>'
```

### 2. 마이그레이션 생성 및 적용

모델을 정의한 후에는 데이터베이스에 해당 변경 사항을 반영해야 합니다:

```bash
flask db migrate -m "Added Tag model"
flask db upgrade
```

이 명령어를 통해 새로운 테이블이 생성되고, 데이터베이스 스키마가 최신 상태로 유지됩니다.
