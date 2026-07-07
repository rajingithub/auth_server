from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from accounts.models import User
from accounts.dao.user_dao import UserDAO
from utils.logger import logger


class UserCreateViewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField(default=False)

    def validate_username(self, value):
        if UserDAO.get_user_by_username(username=value):
            err_msg = "Username already exists"
            logger.error(f'{err_msg}', extra={"username":value})
            raise serializers.ValidationError("Username already exists.")
        return value



class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserCreateViewSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"serializer error:{serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            user = UserDAO.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                is_staff = validated_data.get('is_staff', False),
                is_active = validated_data.get('is_active', False),
                is_superuser = validated_data.get('is_superuser', False)
            )
            logger.info("user created successfully", extra={"user_id":user.id, "username":user.username, "email":user.email})
            return Response({"msg":"User created succesfully","user_id":user.id})
        except Exception as error:
            logger.error(f"Error:{error}")
            return Response({"error": "Internal Server Error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)







class UserListView(APIView):
    def post(self, request, *args, **kwargs):
        pass
