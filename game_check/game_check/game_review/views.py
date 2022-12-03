from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model

from game_check.game_review.forms import SignUpForm
from game_check.game_review.models import Profile

UserModel = get_user_model()


class IndexView(views.TemplateView):
    template_name = 'index.html'


class UserSignUpView(views.CreateView):
    template_name = 'sign-up-user.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class UserSignInView(auth_views.LoginView):
    template_name = 'sign-in-user.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.get_redirect_url() or self.get_default_redirect_url()


class UserSignOutView(auth_views.LogoutView):
    template_name = 'sign-out-user.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.get_redirect_url() or self.get_default_redirect_url()


class ProfileView(views.DetailView):
    context_object_name = 'profile'
    model = Profile
    template_name = 'info-profile.html'


class UserDetailsView(views.DetailView):
    context_object_name = 'user_details'
    model = Profile
    template_name = 'details-profile.html'


class UserEditView(views.UpdateView):
    model = Profile
    fields = ('avatar', 'name', 'age', 'gender', 'bio')
    template_name = 'edit-profile.html'
    # TODO: fix success_url to redirect to proper url
    success_url = reverse_lazy('index')

    # def get_success_url(self):
    #     result = reverse_lazy('details profile', kwargs={
    #         'slug': self.object.slug,
    #         'pk': self.object.pk,
    #     })
    #
    #     return result


class PasswordEditView(auth_views.PasswordChangeView):
    pass


class EmailEditView(views.UpdateView):
    pass


class OtherProfileView(views.DetailView):
    pass


class GamesReviewedView(views.DetailView):
    pass


class GamesFavouriteView(views.DetailView):
    pass


class GameCreateView(views.CreateView):
    pass


class GameDetailsView(views.DetailView):
    pass
