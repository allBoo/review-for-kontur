import os


class Config:
    DEBUG: bool = bool(os.environ.get('DEBUG', False))
    API_TOKEN: str = os.environ.get('API_TOKEN', 'test-your-luck')

    ALLOWED_HOSTS: list[str] = os.environ.get('ALLOWED_HOSTS', '*').split(',')

    CMS_API_BASE_URL: str = os.environ.get('CMS_API_BASE_URL', 'http://cms:8000')
    CMS_API_TOKEN: str = os.environ.get('CMS_API_TOKEN', '')
