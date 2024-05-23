import os


class Config:
    DEBUG = os.environ.get('DEBUG', False)
    API_TOKEN = os.environ.get('API_TOKEN', 'test-your-luck')

    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
