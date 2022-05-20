from django.contrib import admin
from .models import Account, Settings, Transaction

# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Settings)