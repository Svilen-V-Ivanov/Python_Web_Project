from django.urls import reverse_lazy


def megabytes_to_bytes(mb):
    return mb * 1024 * 1024


def is_owner(request, obj):
    return request.user == obj.user


def get_game_by_id(model, value):
    return model.objects.filter(pk=value).get()


def get_user_by_id(model, value):
    return model.objects.filter(pk=value).get()


def get_comment(comments, user, game):
    for comment in comments:
        if comment.user_id == user.pk and comment.game_id == game.pk:
            return comment

    return None


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


def get_current_rating(ratings, user_id, game_id):
    for rating in ratings:
        if rating.user_id == user_id.pk and rating.game_id == game_id.pk:
            return rating

    return None


def get_average_rating(ratings, game_id):
    score = 0
    count = 0

    for rating in ratings:
        if rating.game_id == game_id.pk:
            score += rating.value
            count += 1

    if count == 0:
        return 0.0
    else:
        return round(score / count, 2)


def get_current_favourite(favourites, user_id, game_id):
    current_favourite = None
    for favourite in favourites:
        if favourite.user_id == user_id and favourite.game_id == game_id.pk:
            current_favourite = favourite
            return current_favourite

    return current_favourite


def get_reviewed_games(games, scores, comments, user):
    user_pk = user.pk
    game_id_list = []
    filtered_games = []
    for comment in comments:
        if comment.user_id == user_pk:
            game_id = comment.game_id
            if game_id not in game_id_list:
                game_id_list.append(game_id)

    for score in scores:
        if score.user_id == user_pk:
            game_id = score.game_id
            if game_id not in game_id_list:
                game_id_list.append(game_id)

    for game in games:
        if game.pk in game_id_list:
            filtered_games.append(game)

    return filtered_games


def get_favourite_games(games, favourites, user):
    user_pk = user.pk
    game_id_list = []
    filtered_games = []

    for favourite in favourites:
        if favourite.user_id == user_pk and favourite.is_favourite:
            game_id = favourite.game_id
            if game_id not in game_id_list:
                game_id_list.append(game_id)

    for game in games:
        if game.pk in game_id_list:
            filtered_games.append(game)

    return filtered_games


def get_len(item):
    return len(item)


def get_redirect_url(model, user_model, self):
    user = model.objects.filter(pk=self.request.user.pk).get()
    site_user = user_model.objects.filter(pk=user.user.pk).get()
    result = reverse_lazy('details profile', kwargs={
        'slug': site_user.slug,
        'pk': site_user.pk,
    })

    return result
