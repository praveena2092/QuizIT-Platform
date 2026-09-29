class Config(object):
    DEBUG=False
    TESTING=False
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    
class LocalDevelopmentConfig(Config):
    #configuratin
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///quiz.db"
    # config for security
    
    SECRET_KEY="this-is-a-secretkey" #hash user cred in session
    SECURITY_PASSWORD_HASH="bcrypt" #mechanism for hashing password
    SECURITY_PASSWORD_SALT="this-is-a-password-salt" # helps in hashing password
    WTF_CSRF_ENABLED=False
    SECURITY_TOKEN_AUTHENTICATION_HEADER="Authentication-Token"
    