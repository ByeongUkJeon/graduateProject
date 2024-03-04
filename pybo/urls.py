from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router=DefaultRouter()
router.register('user',views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.signup),
    path('login/', views.login),
    path('idCheck/', views.idCheck),
    path('nickCheck/', views.nicknameCheck),
    path('addTale/', views.addTale),
    path('requestTTS/', views.requestTTS),
    path('requestTale/', views.requestTale),
    path('requestAudio/', views.requestAudio),
    path('downloadImage/', views.downloadImage),
    path('requestImage/', views.requestImage),
    path('addChild/', views.addChild),
    path('requestHome/', views.requestHome),
    path('requestChildProfile/', views.requestChildProfile),
    path('requestSearch/', views.requestSearch),
    path('requestComment/', views.requestComment),
    path('requestCommentList/', views.requestCommentList),
    path('requestLike/', views.requestLike),
    path('requestRate/', views.requestRate),
    path('requestFavorite/', views.requestFavorite)

]