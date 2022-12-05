def megabytes_to_bytes(mb):
    return mb * 1024 *1024


def get_all_user_comments_id(value):
    user_ids = []
    for user in value:
        user_ids.append(user.user.pk)

    return user_ids
