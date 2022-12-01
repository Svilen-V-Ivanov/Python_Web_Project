from django.core import exceptions

from game_check.game_review.utils import megabytes_to_bytes


def username_validator(value):
    for x in value:
        if not x.isalnum() and x != '_':
            raise exceptions.ValidationError("Please make sure username contains \
            only letters, numbers, and underscore.")


def age_validator(value):
    max_age = 100
    if value > max_age:
        raise exceptions.ValidationError(f"User cannot be older than {max_age}!")


def validate_file_less_than_one(file):
    filesize = file.file.size
    megabyte_limit = 1.0
    if filesize > megabytes_to_bytes(megabyte_limit):
        raise exceptions.ValidationError(f"Max file size is {megabyte_limit}MB")


def score_validator(value):
    min_value = 0.0
    max_value = 10.0
    if value < min_value or value > max_value:
        raise exceptions.ValidationError(f"Score must be between {min_value} and {max_value}")