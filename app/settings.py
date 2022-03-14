from decouple import config


class Settings:
    DEBUG = True
    ENVIRONMENT = config('FLASK_CONFIG', 'development')
    FLASK_APP = config('FLASK_APP', None)
    FLASK_DEBUG = config('FLASK_DEBUG', 1)

    # POSTGRESQL_URL = config('DATABASE_URL')
    # POSTGRESQL_DATABASE = config('DATABASE')
    # POSTGRESQL_USERNAME = config('USERNAME')
    # POSTGRESQL_PASSWORD = config('PASSWORD')

    CARD_TABLE_NAME = config('CARD_TABLE_NAME', 'test_card')
    TAG_TABLE_NAME = config('TAG_TABLE_NAME', 'test_tag')

    TOKEN_SECRET_KEY = config('JWT_SECRET_KEY', '')


current_config = Settings()
