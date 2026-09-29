from flask import Flask
from application.database import db
from application.models import User, Role
from api.resource import api
from application.config import LocalDevelopmentConfig
from flask_security import datastore, SQLAlchemyUserDatastore,Security
from flask_security import hash_password
from werkzeug.security import generate_password_hash
from application.celery_init import celery_init_app
from celery.schedules import crontab
from flask_caching import Cache
from extension import cache
from flask_cors import CORS
def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    app.config['CACHE_TYPE'] = 'RedisCache' 
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  
    CORS(app,origins=["http://localhost:5173", "http://127.0.0.1:5173"])
    return app


app=create_app()
celery=celery_init_app(app)
celery.autodiscover_tasks()
cache.init_app(app)
with app.app_context():
    db.create_all()
    app.security.datastore.find_or_create_role(name="admin", description="super user")
    app.security.datastore.find_or_create_role(name="user", description="general user")
    db.session.commit()
    
    if not app.security.datastore.find_user(email="user@admin.com"):
        app.security.datastore.create_user(email="user@admin.com",username="admin01",password=generate_password_hash("1234"),roles=['admin'])
    if not app.security.datastore.find_user(email="user@user.com"):
        app.security.datastore.create_user(email="user@user.com",username="user01",password=generate_password_hash("1234"),roles=['user'])
    if not app.security.datastore.find_user(email="user2@email.com"):
        app.security.datastore.create_user(email="user2@email.com",username="user02",password=generate_password_hash("1234"),roles=['user'])
    db.session.commit()
    
from api.routes import *

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        monthly_report.s(),
    )
if __name__ == "__main__":    
    app.run(debug=True)