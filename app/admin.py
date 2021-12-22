from django.apps import apps
from django.contrib import admin

from leo_optimizer import QuickAdmin


for model in apps.get_app_config("app").get_models():
    admin.site.register(model, QuickAdmin)