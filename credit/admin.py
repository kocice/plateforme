from django.contrib import admin

from credit.models import TypeCredit


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(TypeCredit, AuthorAdmin)
