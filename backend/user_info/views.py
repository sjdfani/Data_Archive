from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import UserInfo
from .serializer import UserInfoSerializer


class CreateUser(APIView):

    @staticmethod
    def post(request):
        msg = {"state": None}
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            type_user = serializer.validated_data.get('type')
            if type_user == 'admin':
                username = serializer.validated_data.get('username')
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                User.objects.create_superuser(username=username, email=email, password=password)
            msg["state"] = "done"
            return Response(data=msg, status=201)
        else:
            errors = serializer.errors
            return Response(data=errors, status=400)


class CheckAdmin(APIView):

    @staticmethod
    def get(request):
        msg = {"state": None}
        is_exist_admin = UserInfo.objects.filter(type="admin").exists()
        if is_exist_admin:
            msg["state"] = "is_exist"
            return Response(data=msg, status=200)
        else:
            msg["state"] = "is_not_exist"
            return Response(data=msg, status=200)

    @staticmethod
    def post(request):
        msg = {"state": None}
        data = JSONParser().parse(request)
        username = data['username']
        user = UserInfo.objects.filter(username=username).first()
        if user.type == "admin":
            msg["state"] = "is_admin"
            return Response(msg, status=200)
        else:
            msg["state"] = "is_not_admin"
            return Response(msg, status=400)


class LoginUser(APIView):

    @staticmethod
    def post(request):
        msg = {"message": None, "state": None}
        data = JSONParser().parse(request)
        username = data["username"]
        password = data["password"]
        user_detail = UserInfo.objects.filter(username=username).first()
        if user_detail is None:
            msg["message"] = "username is not exist."
            msg["state"] = "None"
            return Response(data=msg, status=404)
        elif password != user_detail.password:
            msg["message"] = "password is incorrect."
            msg["state"] = "incorrect"
            return Response(data=msg, status=400)
        else:
            msg["message"] = "verified."
            msg["state"] = "correct"
            return Response(data=msg, status=200)


class GetUserInfo(APIView):

    @staticmethod
    def post(request):
        data = JSONParser().parse(request)
        username = data["username"]
        user = UserInfo.objects.filter(username=username).first()
        serializer = UserInfoSerializer(user)
        return Response(data=serializer.data, status=200)


class UpdateUserInfo(APIView):
    @staticmethod
    def patch(request):
        msg = {"message": None, "state": None}
        data = JSONParser().parse(request)
        username = data["username"]
        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")
        user = UserInfo.objects.get(username=username)
        if fullname is not None:
            user.fullname = fullname
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password
        user.save()
        msg["message"] = "Done. Please refresh."
        msg["state"] = "done"
        return Response(data=msg, status=200)


class AllUserInfo(APIView):

    @staticmethod
    def get(request):
        data = UserInfo.objects.all()
        serializer = UserInfoSerializer(data, many=True)
        return Response(serializer.data, status=200)

    @staticmethod
    def delete(request):
        msg = {"message": None}
        data = JSONParser().parse(request)
        user_id = data["id"]
        user_exists = UserInfo.objects.filter(id=user_id).exists()
        if user_exists:
            user = UserInfo.objects.get(id=user_id)
            user.delete()
            msg["message"] = "User has deleted."
            return Response(data=msg, status=200)
        else:
            msg["message"] = f"User with id={user_id} has not exists."
            return Response(data=msg, status=400)
