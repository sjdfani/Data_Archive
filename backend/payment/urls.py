from django.urls import path
from .views import CreatePayment, GetAllPayment, GetByUsernamePayment,Delete_Data

app_name = "payment"

urlpatterns = [
    path('create/', CreatePayment.as_view()),
    path('get-all-payment/', GetAllPayment.as_view()),
    path('get-by-username/', GetByUsernamePayment.as_view()),
    path('delete-data/', Delete_Data.as_view()),
]
