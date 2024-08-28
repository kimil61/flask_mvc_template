import os
from app import app, db
from flask_migrate import upgrade

def apply_migrations():
    with app.app_context():
        upgrade()  # 최신 마이그레이션을 적용

if __name__ == '__main__':
    apply_migrations()  # 앱 실행 전 마이그레이션 적용
    app.run(debug=True)
