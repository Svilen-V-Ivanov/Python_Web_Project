from enum import Enum

from django.core import validators
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils.text import slugify

from game_check.game_review.managers import SiteUserManager
from game_check.game_review.validators import username_validator, validate_file_less_than_one, age_validator, \
    score_validator


class ChoicesEnumMixin:
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class Gender(ChoicesEnumMixin, Enum):
    male = 'Male'
    female = 'Female'
    DoNotShow = 'Do not show'


class SiteUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    MAX_LEN_USERNAME = 20
    MIN_LEN_USERNAME = 6

    username = models.CharField(
        max_length=MAX_LEN_USERNAME,
        unique=True,
        null=False,
        blank=False,
        validators=(
            username_validator,
            validators.MinLengthValidator(MIN_LEN_USERNAME),
        ),
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        null=False,
        blank=True,
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.username)

        super(SiteUser, self).save(*args, **kwargs)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'username'

    objects = SiteUserManager()


class Profile(models.Model):
    MAX_NAME_LEN = 25
    MAX_LEN_BIO = 250

    name = models.CharField(
        max_length=MAX_NAME_LEN,
    )

    age = models.PositiveIntegerField(
        validators=(
            age_validator,
        ),
    )

    gender = models.CharField(
        choices=Gender.choices(),
        max_length=Gender.max_len(),
        default='Male',
    )

    avatar = models.ImageField(
        upload_to='avatars',
        validators=(
            validate_file_less_than_one,
        ),
        null=True,
        blank=True,
    )

    bio = models.TextField(
        max_length=MAX_LEN_BIO,
        default='Create your own bio here!',
    )

    user = models.OneToOneField(
        SiteUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    MAX_TITLE_LEN = 100
    MAX_LEN_TEXT = 250

    title = models.CharField(
        max_length=MAX_TITLE_LEN,
        unique=True,
    )

    image = models.ImageField(
        upload_to='game_images',
        validators=(
            validate_file_less_than_one,
        ),

    )

    user = models.ForeignKey(
        SiteUser,
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ('title', )


class GameScore(models.Model):

    value = models.FloatField(
        validators=(
            score_validator,
        ),
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        SiteUser,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return f"{self.user.username}/{self.game.title}"


class GameComment(models.Model):
    MAX_LEN_CONT = 250

    content = models.TextField(
        max_length=MAX_LEN_CONT,
        null=True,
        blank=True,
    )

    date_created = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        SiteUser,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.RESTRICT,
        related_name='comments',
    )

    def __str__(self):
        return f"{self.user.username}/{self.game.title}"

    class Meta:
        ordering = ('date_created', )


class GameFavourite(models.Model):
    is_favourite = models.BooleanField(
        default=False,
    )

    user = models.ForeignKey(
        SiteUser,
        on_delete=models.RESTRICT,
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return f"{self.user.username}/{self.game.title}"
