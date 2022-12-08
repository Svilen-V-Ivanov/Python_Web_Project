from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model, mixins as auth_mixins

from game_check.game_review.forms import SignUpForm, ChangeUserPasswordForm, GameCommentForm, GameRatingForm, \
    GameFavouriteForm, CommentEditForm, RatingEditForm, EditFavouriteForm
from game_check.game_review.models import Profile, Game, GameComment, GameScore, GameFavourite
from game_check.game_review.utils import get_game_by_id, get_has_commented, get_rating, get_average_rating, \
    get_current_favourite, get_comment, get_current_rating, get_reviewed_games, get_favourite_games, get_len

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


class UserSignOutView(auth_mixins.LoginRequiredMixin, auth_views.LogoutView):
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


@login_required
def profile_reviewed_games(request, slug, pk):
    user = request.user
    user_scores = GameScore.objects.filter(user_id=pk)
    user_comments = GameComment.objects.filter(user_id=pk)
    all_games = Game.objects.all()
    reviewed_games = get_reviewed_games(all_games, user_scores, user_comments, user)
    game_len = get_len(reviewed_games)

    context = {
        'games': reviewed_games,
        'len': game_len,
    }

    return render(request, 'reviewed-games.html', context)


@login_required
def profile_favourite_games(request, slug, pk):
    user = request.user
    user_favourites = GameFavourite.objects.filter(user_id=pk)
    all_games = Game.objects.all()
    favourite_games = get_favourite_games(all_games, user_favourites, user)
    game_len = get_len(favourite_games)

    context = {
        'games': favourite_games,
        'len': game_len,
    }

    return render(request, 'favourite-games.html', context)


class UserDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    context_object_name = 'user_details'
    model = Profile
    template_name = 'details-profile.html'


class UserEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
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


# TODO : Fix redirect on password change or make changes to 'index.html'
class PasswordEditView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = ChangeUserPasswordForm
    template_name = 'edit_password.html'
    success_url = reverse_lazy('index')


# TODO: Maybe make changing email look a bit better, also if enough time add signal to send email for email change
class EmailEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = UserModel
    fields = ('email',)
    template_name = 'edit-email.html'
    success_url = reverse_lazy('index')


# TODO: make this view
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


@login_required()
def games_details(request, pk):
    current_game = get_game_by_id(Game, pk)
    current_user_id = request.user.pk

    comment_form = GameCommentForm()
    comment_edit = CommentEditForm()
    rating_form = GameRatingForm()
    rating_edit = RatingEditForm()
    favourite_form = GameFavouriteForm()
    edit_favourite = EditFavouriteForm()

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=current_game.pk)
    has_commented = get_has_commented(comments, current_user_id, current_game)

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user_id, current_game)
    average_rating = get_average_rating(ratings, current_game)

    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user_id, current_game)

    context = {
        'game': current_game,
        'user_id': current_user_id,

        'comment_form': comment_form,
        'edit_comment': comment_edit,
        'rating_form': rating_form,
        'edit_rating': rating_edit,
        'favourite_form': favourite_form,
        'edit_favourite': edit_favourite,

        'has_commented': has_commented,
        'game_comments': current_game_comments,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'user_favourite': user_favourite,
    }

    return render(request, 'details-game.html', context)


@login_required
def comment_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk
    comments = GameComment.objects.all()
    current_comment = get_comment(comments, current_user, game)

    if request.method == 'POST':
        if not current_comment:
            form = GameCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.game = game
                comment.user = current_user
                comment.save()
                return redirect('details game', game_id)
        else:
            form = CommentEditForm(request.POST, instance=current_comment)
            if form.is_valid():
                form.save()
                return redirect('details game', game_id)


@login_required
def rate_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk
    ratings = GameScore.objects.all()
    current_rating = get_current_rating(ratings, current_user, game)

    if request.method == 'POST':
        if not current_rating:
            form = GameRatingForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.game = game
                comment.user = current_user
                comment.save()
                return redirect('details game', game_id)
        else:
            form = RatingEditForm(request.POST, instance=current_rating)
            if form.is_valid():
                form.save()
                return redirect('details game', game_id)


@login_required
def favourite_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk
    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    if request.method == "POST":
        if not user_favourite:
            form = GameFavouriteForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.game = game
                comment.user = current_user
                comment.save()
                return redirect('details game', game_id)
        else:
            form = EditFavouriteForm(request.POST, instance=user_favourite)
            if form.is_valid():
                form.save()
                return redirect('details game', game_id)


