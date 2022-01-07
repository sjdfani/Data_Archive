from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import ListAPIView
from .serializer import PaymentSerializer
from .models import Payment


class CreatePayment(APIView):

    @staticmethod
    def post(request):
        msg = {"message": None, "state": None}
        data = JSONParser().parse(request)
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            msg["message"] = "Add has successful."
            msg["state"] = "done"
            return Response(data=msg, status=201)
        else:
            errors = serializer.errors
            return Response(data=errors, status=400)


class GetAllPayment(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class GetByUsernamePayment(APIView):
    @staticmethod
    def get(request):
        data = JSONParser().parse(request)
        username = data['username']
        payment_data = Payment.objects.filter(username=username)
        serializer = PaymentSerializer(payment_data, many=True)
        return Response(serializer.data, status=200)


class Delete_Data(APIView):

    @staticmethod
    def delete(request):
        msg = {"message": None}
        data = JSONParser().parse(request)
        data_id = data['id']
        payment_obj_exist = Payment.objects.filter(id=data_id).exists()
        if payment_obj_exist:
            payment_obj = Payment.objects.filter(id=data_id)
            payment_obj.delete()
            msg["message"] = f"Data has deleted."
            return Response(data=msg, status=200)
        else:
            msg["message"] = f"{data_id} is not exists."
            return Response(data=msg, status=400)
