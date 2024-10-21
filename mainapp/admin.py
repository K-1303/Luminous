from django.contrib import admin

from .models import usage, solar, tariff

admin.site.register(usage)

admin.site.register(solar)

admin.site.register(tariff)

# Register your models here.
