from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

UserModel = get_user_model()


# TODO: Fix admin
# @admin.register(UserModel)
# class SiteUserAdmin(auth_admin.UserAdmin):
#     pass
