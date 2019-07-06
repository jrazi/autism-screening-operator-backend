from django.conf.urls import url,include
from django.urls import path
from website import views
from rest_framework.routers import SimpleRouter
from website.views import obtain_token,verify_token,remove_token

router = SimpleRouter()
router.register('eval/pregame',views.PreGameCommands,'PreGame')
router.register('eval/weel',views.WeelCommands,'Weel')
router.register('eval/parrot',views.ParrotCommands,'Parrot')

urlpatterns = [
    url(r'auth/login', obtain_token),
    url(r'auth/check', verify_token),
    url(r'auth/logout', remove_token),
    path('user/',views.UserProfileList.as_view()),
    url('', include(router.urls))
]
