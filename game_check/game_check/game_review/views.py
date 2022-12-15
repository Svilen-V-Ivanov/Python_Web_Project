from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, get_user_model, mixins as auth_mixins

from game_check.game_review.forms import SignUpForm, ChangeUserPasswordForm, GameCommentForm, GameRatingForm, \
    GameFavouriteForm, CommentEditForm, RatingEditForm, EditFavouriteForm
from game_check.game_review.models import Profile, Game, GameComment, GameScore, GameFavourite
from game_check.game_review.utils import get_game_by_id, get_has_commented, get_rating, get_average_rating, \
    get_current_favourite, get_comment, get_current_rating, get_reviewed_games, get_favourite_games, get_len, \
    get_redirect_url

UserModel = get_user_model()


def page_does_not_exist(request, *args, **kwargs):

    return render(request, 'core/404.html', status=404)


def bad_request(request):
    return render(request, 'core/bad-credentials.html')


def index(request):
    games = Game.objects.all()
    paginator = Paginator(games, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'games': games,
        'page_obj': page_obj,
    }
    return render(request, 'core/index.html', context)


def search_bar(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        games = Game.objects.filter(title__contains=searched)
        return render(request, 'core/search-bar.html', {
            'searched': searched,
            'games': games,
        })
    else:
        games = Game.objects.all()
        return render(request, 'core/search-bar.html', {
            'games': games,
        })


def redirect_when_not_logged_in(request):
    return render(request, 'core/not-logged-in.html')


class UserSignUpView(views.CreateView):
    template_name = 'core/sign-up-user.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, self.object)
        return result


class UserSignInView(auth_views.LoginView):
    template_name = 'core/sign-in-user.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.get_redirect_url() or self.get_default_redirect_url()


class UserSignOutView(auth_mixins.LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'core/sign-out-user.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.get_redirect_url() or self.get_default_redirect_url()


@login_required
def profile_reviewed_games(request, slug, pk):
    try:
        request_user = UserModel.objects.filter(pk=pk, slug=slug).get()
    except UserModel.DoesNotExist as error:
        return redirect('bad request')

    user = request.user
    user_scores = GameScore.objects.filter(user_id=pk)
    user_comments = GameComment.objects.filter(user_id=pk)
    all_games = Game.objects.all()
    reviewed_games = get_reviewed_games(all_games, user_scores, user_comments, user)
    games_len = get_len(reviewed_games)

    paginator = Paginator(reviewed_games, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'games': reviewed_games,
        'page_obj': page_obj,
        'len': games_len,
    }

    return render(request, 'user/reviewed-games.html', context)


@login_required
def profile_favourite_games(request, slug, pk):
    try:
        request_user = UserModel.objects.filter(pk=pk, slug=slug).get()
    except UserModel.DoesNotExist as error:
        return redirect('bad request')

    user = request.user
    user_favourites = GameFavourite.objects.filter(user_id=pk)
    all_games = Game.objects.all()
    favourite_games = get_favourite_games(all_games, user_favourites, user)
    games_len = get_len(favourite_games)

    paginator = Paginator(favourite_games, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'games': favourite_games,
        'page_obj': page_obj,
        'len': games_len,
    }

    return render(request, 'user/favourite-games.html', context)


class UserDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    context_object_name = 'user_details'
    model = Profile
    template_name = 'user/details-profile.html'
    # TODO: Remove this before project defense
    # def get_queryset(self):
    #     user = Profile.objects.filter(pk=self.request.user.pk).get()
    #     try:
    #         site_user = UserModel.objects.filter(pk=user.user.pk).get()
    #     except UserModel.DoesNotExist as error:
    #         return redirect('bad request')
    #     return Profile.objects.filter(pk=self.request.user.pk)


class UserEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Profile
    fields = ('avatar', 'name', 'age', 'gender', 'bio')
    template_name = 'user/edit-profile.html'

    # TODO: Delete this before project defense
    # def get_success_url(self):
    #     user = Profile.objects.filter(pk=self.request.user.pk).get()
    #     site_user = UserModel.objects.filter(pk=user.user.pk).get()
    #     result = reverse_lazy('details profile', kwargs={
    #         'slug': site_user.slug,
    #         'pk': site_user.pk,
    #     })
    #
    #     return result
    # TODO: make sure this still works before project defense
    def get_success_url(self):
        return get_redirect_url(Profile, UserModel, self)


class PasswordEditView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = ChangeUserPasswordForm
    template_name = 'user/edit_password.html'

    # TODO: Delete this before project defense
    # def get_success_url(self):
    #     user = Profile.objects.filter(pk=self.request.user.pk).get()
    #     site_user = UserModel.objects.filter(pk=user.user.pk).get()
    #     result = reverse_lazy('details profile', kwargs={
    #         'slug': site_user.slug,
    #         'pk': site_user.pk,
    #     })
    #
    #     return result

    # TODO: make sure this still works before project defense
    def get_success_url(self):
        return get_redirect_url(Profile, UserModel, self)


class EmailEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = UserModel
    fields = ('email',)
    template_name = 'user/edit-email.html'

    # TODO: Delete this before project defense
    # def get_success_url(self):
    #     user = Profile.objects.filter(pk=self.request.user.pk).get()
    #     site_user = UserModel.objects.filter(pk=user.user.pk).get()
    #     result = reverse_lazy('details profile', kwargs={
    #         'slug': site_user.slug,
    #         'pk': site_user.pk,
    #     })
    #
    #     return result

    # TODO: make sure this still works before project defense
    def get_success_url(self):
        return get_redirect_url(Profile, UserModel, self)


class GameCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'game/create-game.html'
    model = Game
    fields = ('title', 'image')
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GameCreateView, self).form_valid(form)


def games_details(request, pk):
    try:
        game = get_game_by_id(Game, pk)
    except Game.DoesNotExist as error:
        return redirect('bad request')

    current_user = request.user

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=game.pk)
    has_commented = get_has_commented(comments, current_user.pk, game)

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    average_rating = get_average_rating(ratings, game)

    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    context = {
        'game': game,
        'user_id': current_user.pk,

        'has_commented': has_commented,
        'game_comments': current_game_comments,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'user_favourite': user_favourite,
    }

    return render(request, 'game/details-game.html', context)


@login_required
def comment_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    average_rating = get_average_rating(ratings, game)

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=game.pk)
    has_commented = get_has_commented(comments, current_user.id, game)

    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    if request.method == 'GET':
        form = GameCommentForm()
    else:
        form = GameCommentForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.game = game
            rating.user = current_user
            rating.save()
            return redirect('details game', game.pk)

    context = {
        'game': game,
        'user': current_user,
        'user_favourite': user_favourite,
        'form': form,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'has_commented': has_commented,
        'game_comments': current_game_comments,
    }

    return render(request, 'game/create-and-edit-comment.html', context)


@login_required
def edit_comment(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    average_rating = get_average_rating(ratings, game)

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=game.pk)
    has_commented = get_has_commented(comments, current_user.id, game)
    comment = get_comment(comments, current_user, game)

    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    if request.method == 'GET':
        form = CommentEditForm(instance=comment)
    else:
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('details game', game_id)

    context = {
        'game': game,
        'user': current_user,
        'user_favourite': user_favourite,
        'form': form,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'has_commented': has_commented,
        'game_comments': current_game_comments,
    }

    return render(request, 'game/create-and-edit-comment.html', context)


@login_required
def delete_comment(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    comments = GameComment.objects.all()
    comment = get_comment(comments, current_user, game)
    comment.delete()

    return redirect('details game', game.pk)


@login_required
def rate_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk
    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    average_rating = get_average_rating(ratings, game)

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=game.pk)
    has_commented = get_has_commented(comments, current_user.id, game)

    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    if request.method == 'GET':
        form = GameRatingForm()
    else:
        form = GameRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.game = game
            rating.user = current_user
            rating.save()
            return redirect('details game', game_id)

    context = {
        'game': game,
        'user': current_user,
        'user_favourite': user_favourite,
        'form': form,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'has_commented': has_commented,
        'game_comments': current_game_comments,
    }

    return render(request, 'game/create-and-edit-rating.html', context)


@login_required
def edit_rating(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    rating = get_current_rating(ratings, current_user, game)
    average_rating = get_average_rating(ratings, game)

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=game.pk)
    has_commented = get_has_commented(comments, current_user.id, game)

    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    if request.method == 'GET':
        form = RatingEditForm(instance=rating)
    else:
        form = RatingEditForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('details game', game_id)

    context = {
        'game': game,
        'user': current_user,
        'user_favourite': user_favourite,
        'form': form,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'has_commented': has_commented,
        'game_comments': current_game_comments,
    }

    return render(request, 'game/create-and-edit-rating.html', context)


@login_required
def favourite_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk
    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    average_rating = get_average_rating(ratings, game)

    comments = GameComment.objects.all()
    current_game_comments = GameComment.objects.filter(game_id=game.pk)
    has_commented = get_has_commented(comments, current_user.id, game)

    if request.method == 'GET':
        form = GameFavouriteForm()
    else:
        form = GameFavouriteForm(request.POST)
        if form.is_valid():
            favourite = form.save(commit=False)
            favourite.game = game
            favourite.user = current_user
            favourite.save()
            return redirect('details game', game_id)

    context = {
        'game': game,
        'user': current_user,
        'user_favourite': user_favourite,
        'form': form,
        'personal_rating': current_user_rating,
        'average': average_rating,
        'has_commented': has_commented,
        'game_comments': current_game_comments,
    }

    return render(request, 'game/create-and-edit-favourite.html', context)


@login_required
def edit_favourite_game(request, pk):
    game = get_game_by_id(Game, pk)
    current_user = request.user
    game_id = game.pk
    favourites = GameFavourite.objects.all()
    user_favourite = get_current_favourite(favourites, current_user.pk, game)

    ratings = GameScore.objects.all()
    current_user_rating = get_rating(ratings, current_user.pk, game)
    average_rating = get_average_rating(ratings, game)

    if request.method == 'GET':
        form = EditFavouriteForm(instance=user_favourite)
    else:
        form = EditFavouriteForm(request.POST, instance=user_favourite)
        if form.is_valid():
            form.save()
            return redirect('details game', game_id)

    context = {
        'game': game,
        'user': current_user,
        'user_favourite': user_favourite,
        'form': form,
        'personal_rating': current_user_rating,
        'average': average_rating,
    }

    return render(request, 'game/create-and-edit-favourite.html', context)
