from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from game_check.game_review.forms import SignUpForm
from game_check.game_review.models import Game, GameScore, GameComment, GameFavourite, Profile

UserModel = get_user_model()


# TODO: Fix admin
@admin.register(UserModel)
class SiteUserAdmin(auth_admin.UserAdmin):
    list_display = ['id', 'username', 'email', 'last_login', "date_joined", 'is_staff', ]
    ordering = ('username',)
    list_filter = ('is_staff', )
    search_fields = ('username', 'email', )
    add_form = SignUpForm
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            "Primary Details",
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2',),
            },
        ),
        (
            "Extra Information",
            {
                'classes': ('wide',),
                'fields': ('name', 'age', ),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'age', 'user', ]
    search_fields = ('name', 'age', 'user__username', )
    list_filter = ('user', 'name',)
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "name",
                    "age",
                    "gender",
                    "avatar",
                    "bio",
                    "user",
                )
            },
        ),
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', ]
    list_filter = ('user', 'title', )
    search_fields = ('title', 'user',)
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "title",
                    "image",
                    "user",
                )
            },
        ),
    )


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'game', ]
    list_filter = ('user', 'game__title', )
    search_fields = ('user__username', 'game__title', )
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "value",
                    "user",
                    "game",
                )
            },
        ),
    )


@admin.register(GameComment)
class GameCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'game', ]
    list_filter = ('user', 'game__title', )
    search_fields = ('user__username', 'game__title',)
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "content",
                    "user",
                    "game",
                )
            },
        ),
    )


@admin.register(GameFavourite)
class GameFavouriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'game', ]
    list_filter = ('user', 'game__title',)
    search_fields = ('user__username', 'game__title',)
    fieldsets = (
        (
            "Details",
            {
                "fields": (
                    "is_favourite",
                    "user",
                    "game",
                )
            },
        ),
    )
