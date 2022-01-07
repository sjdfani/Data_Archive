from django.urls import path
from .views import CreateUser, CheckAdmin, LoginUser, GetUserInfo, UpdateUserInfo, AllUserInfo

app_name = 'user_info'

urlpatterns = [
    path('create/', CreateUser.as_view()),
    path('check-admin/', CheckAdmin.as_view()),
    path('login/', LoginUser.as_view()),
    path('get-user-info/', GetUserInfo.as_view()),
    path('update-user/', UpdateUserInfo.as_view()),
    path('all-del-user/', AllUserInfo.as_view()),
]
