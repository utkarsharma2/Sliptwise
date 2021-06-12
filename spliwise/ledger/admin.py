from django.contrib import admin

from . import models

admin.site.register(models.Contributions)
admin.site.register(models.Event)
admin.site.register(models.Group)
admin.site.register(models.Ledger)
admin.site.register(models.User)