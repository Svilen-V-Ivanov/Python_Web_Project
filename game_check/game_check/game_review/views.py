from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model, mixins as auth_mixins

from game_check.game_review.forms import SignUpForm, ChangeUserPasswordForm, GameCommentForm, GameRatingForm
from game_check.game_review.models import Profile, Game, GameComment, GameScore
from game_check.game_review.utils import get_game_by_id, get_has_commented, get_rating, get_average_rating

UserModel = get_user_model()


def index(request):
    context = {
        'games': Game.objects.all(),
    }
    return render(request, 'index.html', context)


# class IndexView(views.TemplateView):
#     template_name = 'index.html'


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


class ProfileView(auth_mixins.LoginRequiredMixin, views.ListView):
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
    form_class = ChangeUserPasswordForm
    template_name = 'edit_password.html'
    success_url = reverse_lazy('index')


# TODO: Maybe make changing email look a bit better, also if enough time add signal to send email for email change
class EmailEditView(views.UpdateView):
    model = UserModel
    fields = ('email',)
    template_name = 'edit-email.html'
    success_url = reverse_lazy('index')


class OtherProfileView(views.DetailView):
    pass


class GameCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'create-game.html'
    model = Game
    fields = ('title', 'image')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GameCreateView, self).form_valid(form)


def games_details(request, pk):
    current_game = get_game_by_id(Game, pk)
    current_user_id = request.user.pk

    comment_form = GameCommentForm()
    rating_form = GameRatingForm()

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=current_game.pk)
    has_commented = get_has_commented(comments, current_user_id, current_game)

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user_id, current_game)
    average_rating = get_average_rating(ratings)

    context = {
        'game': current_game,
        'user_id': current_user_id,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'has_commented': has_commented,
        'game_comments': current_game_comments,
        'personal_rating': current_user_rating,
        'average': average_rating,
    }

    return render(request, 'details-game.html', context)


# TODO: Make it log in required
def comment_game(request, pk):
    game = Game.objects.filter(pk=pk) \
        .get()
    current_user = request.user
    game_id = game.pk

    form = GameCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.game = game
        comment.user = current_user
        comment.save()
        return redirect('details game', game_id)


def rate_game(request, pk):
    game = Game.objects.filter(pk=pk) \
        .get()
    current_user = request.user
    game_id = game.pk

    form = GameRatingForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.game = game
        comment.user = current_user
        comment.save()
        return redirect('details game', game_id)