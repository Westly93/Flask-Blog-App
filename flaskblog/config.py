import os

class Config:
    SECRET_KEY= 'westly2001'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///site.db'
    MAIL_SERVER= 'smtp.googlemail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS= True
    MAIL_USERNAME= os.environ.get('MAIL_USEER')
    MAIL_PASWORD= os.environ.get('MAIL_PASSWORD')
