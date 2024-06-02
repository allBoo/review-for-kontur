import os


class Config:
    DEBUG = os.environ.get('DEBUG', False)
    API_TOKEN = os.environ.get('API_TOKEN', 'test-your-luck')

    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

    CMS_API_BASE_URL = os.environ.get('CMS_API_BASE_URL', 'http://cms:8000')
    CMS_API_TOKEN = os.environ.get('CMS_API_TOKEN', '')
