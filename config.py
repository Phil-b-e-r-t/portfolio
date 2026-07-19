import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # -----------------------------
    # Flask
    # -----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY")

    # -----------------------------
    # Database
    # -----------------------------
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {
            "ssl": {
                "ca": os.path.join(BASE_DIR, "certs", "ca.pem")
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # Mail
    # -----------------------------
    MAIL_SERVER = "smtp-relay.brevo.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    MAIL_TIMEOUT = 10