from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListAPIView
from .serializer import FeedbackSerializer
from .models import Feedback


class CreateFeedback(APIView):

    @staticmethod
    def post(request):
        msg = {"state": None}
        data = JSONParser().parse(request)
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            msg["state"] = "done"
            return Response(data=msg, status=201)
        else:
            errors = serializer.errors
            return Response(data=errors, status=400)


class DeleteFeedback(APIView):

    @staticmethod
    def delete(request):
        msg = {"message": None, "state": None}
        data = JSONParser().parse(request)
        feedback_id = data["id"]
        feedback = Feedback.objects.filter(id=feedback_id).exists()
        if not feedback:
            msg["message"] = f"This id({feedback_id}) is not exist."
            msg["state"] = "not_found"
            return Response(data=msg, status=200)
        else:
            feedback = Feedback.objects.filter(id=feedback_id).first()
            feedback.delete()
            msg["message"] = f"Feedback has deleted."
            msg["state"] = "done"
            return Response(data=msg, status=400)


class GetFeedbacks(ListAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
