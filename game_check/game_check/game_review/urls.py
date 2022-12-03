from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from game_check.game_review.views import IndexView, UserSignUpView, UserSignInView, ProfileView, UserSignOutView, \
    UserDetailsView, UserEditView, PasswordEditView, EmailEditView, GamesReviewedView, GamesFavouriteView

# TODO: add slugs and pks where necessary(at profile/)
urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('sign-up/', UserSignUpView.as_view(), name='sign up user'),
    path('sign-in/', UserSignInView.as_view(), name='sign in user'),
    path('sign-out/', UserSignOutView.as_view(), name='sign out user'),
    path('profile/<slug:slug>/<int:pk>/', include([
        path('', ProfileView.as_view(), name='profile'),
        path('details/', include([
            path('', UserDetailsView.as_view(), name='details profile'),
            path('edit/', UserEditView.as_view(), name='edit profile'),
            path('password/', PasswordEditView.as_view(), name='edit password'),
            path('email/', EmailEditView.as_view(), name='edit email'),
        ])),
        path('games/', include([
            path('reviewed/', GamesReviewedView.as_view(), name='reviewed games'),
            path('favourite/', GamesFavouriteView.as_view(), name='favourite games'),
        ])),
    ])),
)

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)