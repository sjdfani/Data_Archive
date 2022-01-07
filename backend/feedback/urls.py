from django.urls import path
from .views import CreateFeedback, GetFeedbacks,DeleteFeedback

app_name = "feedback"

urlpatterns = [
    path('create/', CreateFeedback.as_view()),
    path('get-all/', GetFeedbacks.as_view()),
    path('delete/', DeleteFeedback.as_view()),
]
