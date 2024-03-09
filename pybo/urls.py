from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .user import views as user_view
from .comment import views as comment_view
from .tale import views as tale_view
from .like import views as like_view
from .rate import views as rate_view
from .favorite import views as favorite_view
urlpatterns = [
    path('signup/', user_view.signup),
    path('login/', user_view.login),
    path('idCheck/', user_view.idCheck),
    path('nickCheck/', user_view.nicknameCheck),
    path('requestChildProfile/', user_view.requestChildProfile),
    path('addChild/', user_view.addChild),

    path('addTale/', tale_view.addTale),
    path('requestTTS/', tale_view.requestTTS),
    path('requestTale/', tale_view.requestTale),
    path('requestAudio/', tale_view.requestAudio),
    path('requestCheck/', tale_view.requestCheck),
    path('requestImage/', tale_view.requestImage),

    path('requestHome/', views.requestHome),
    path('downloadImage/', views.downloadImage),
    path('requestSearch/', views.requestSearch),

    path('requestComment/', comment_view.requestComment),
    path('requestCommentList/', comment_view.requestCommentList),

    path('requestLike/', like_view.requestLike),

    path('requestRate/', rate_view.requestRate),
    path('requestFavorite/', favorite_view.requestFavorite),


]