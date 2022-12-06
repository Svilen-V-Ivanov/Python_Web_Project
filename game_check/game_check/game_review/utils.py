def megabytes_to_bytes(mb):
    return mb * 1024 * 1024


def get_game_by_id(model, value):
    return model.objects.filter(pk=value).get()


def get_has_commented(comments, user_id, game_id):
    has_commented = False
    for comment in comments:
        if comment.user_id == user_id and comment.game_id == game_id.pk:
            has_commented = True

    return has_commented


def get_rating(ratings, user_id, game_id):
    current_rating = 11
    for rating in ratings:
        if rating.user_id == user_id and rating.game_id == game_id.pk:
            current_rating = rating.value

    return current_rating


def get_average_rating(ratings):
    score = 0
    count = 0

    for rating in ratings:
        score += rating.value
        count += 1

    if count == 0:
        return 0
    else:
        return round(score / count, 2)

