from django.apps import AppConfig
from mongoengine import connect


class AppV1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_v1'
    def ready(self):
        connect(db='SBB',
                host='mongodb+srv://pascallino90_db_user:UH4v0BOeHKXmD2nt@sbb.z7e6caa.mongodb.net/?appName=SBB',)