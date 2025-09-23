import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6e0e0a43d505c3d5e496b4cc'#TO BE CHANGED TO you-will-never-guess
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'ums.sqlite')#TO BE CONVERTED TO APP.DB
    SESSION_PERMANENT = False#CHANGE IN PRODUCTION
    SESSION_TYPE = 'filesystem'#CHANGE IN PRODUCTION