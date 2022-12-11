from django.urls import path, include

from game_check.game_review.views import UserSignUpView, UserSignInView, UserSignOutView, \
    UserDetailsView, UserEditView, PasswordEditView, EmailEditView, GameCreateView, index, \
    comment_game, games_details, rate_game, favourite_game, profile_reviewed_games, profile_favourite_games, \
    delete_comment, edit_favourite_game, edit_rating, edit_comment, delete_user_profile

urlpatterns = (
    path('', index, name='index'),
    path('sign-up/', UserSignUpView.as_view(), name='sign up user'),
    path('sign-in/', UserSignInView.as_view(), name='sign in user'),
    path('sign-out/', UserSignOutView.as_view(), name='sign out user'),
    path('profile/<slug:slug>/<int:pk>/', include([
        path('details/', include([
            path('', UserDetailsView.as_view(), name='details profile'),
            path('edit/', UserEditView.as_view(), name='edit profile'),
            path('password/', PasswordEditView.as_view(), name='edit password'),
            path('email/', EmailEditView.as_view(), name='edit email'),
        ])),
        path('games/', include([
            path('reviewed/', profile_reviewed_games, name='reviewed games'),
            path('favourite/', profile_favourite_games, name='favourite games'),
        ])),
    ])),
    # path('admin/<slug:slug>/<int:pk>/', include([
    #     path('delete/user/', delete_user_profile, name='delete user'),
    #
    # ])),
    path('game/', include([
        path('', GameCreateView.as_view(), name='create game'),
        path('details/', include([
            path('<int:pk>/', games_details, name='details game'),
            path('comment/<int:pk>/', comment_game, name='comment game'),
            path('comment/edit/<int:pk>/', edit_comment, name='edit comment'),
            path('comment/delete/<int:pk>/', delete_comment, name='delete comment'),
            path('rating/<int:pk>/', rate_game, name='rate game'),
            path('rating/edit/<int:pk>/', edit_rating, name='edit rating'),
            path('favourite/<int:pk>/', favourite_game, name='favourite game'),
            path('favourite/edit/<int:pk>/', edit_favourite_game, name='edit favourite'),
        ])),
    ])),
)

