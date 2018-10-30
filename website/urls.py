from django.conf.urls import url,include
from website import views
from rest_framework.routers import SimpleRouter
from website.authentication import obtain_token,verify_token,remove_token

router = SimpleRouter()
router.register('user',views.UserProfile,'User')
router.register('command',views.Commands,'Command')


urlpatterns = [
    url(r'login/', obtain_token),
    url(r'^verify_token/', verify_token),
    url(r'^logout/', remove_token),
    url('^', include(router.urls))
]

