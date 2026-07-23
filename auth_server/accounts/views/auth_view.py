from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from accounts.enums import GrantType
from utils.logger import logger
from accounts.helper.auth_view_helper import AuthViewHelper
# Create your views here.


class AuthViewSerializer(serializers.Serializer):
    grant_type = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    client_id = serializers.CharField(required=True, allow_blank=False, allow_null=False)

class ClientCredentialsGrantTypeSerializer(serializers.Serializer):
    client_id = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    client_secret = serializers.CharField(required=True, allow_blank=False, allow_null=False)

class PasswordGrantTypeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class AuthView(APIView):
    authentication_classes = []
    
    def post(self, request):
        request_data = request.data
        try:
            serializer = AuthViewSerializer(data = request_data)
            if not serializer.is_valid():
                logger.error(f"serializer error:{serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            client_id = request_data['client_id']
            grant_type = request_data['grant_type']
            """
                Think of a "Grant Type" as the method or the type of credentials the client provides to prove who they are. 
                our single endpoint checks the incoming request parameter called grant_type and instantly knows whether a human or a machine is trying to log in
            """
            if grant_type.lower() == GrantType.CLIENT_CREDENTIALS.lower():
                client_credentials_grant_type_serializer = ClientCredentialsGrantTypeSerializer(data = request_data)
                if not client_credentials_grant_type_serializer.is_valid():
                    logger.error(f"serializer error:{client_credentials_grant_type_serializer.errors}")
                    return Response(client_credentials_grant_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif grant_type.lower() == GrantType.PASSWORD.lower():
                password_grant_type_serializer = PasswordGrantTypeSerializer(data=request_data)
                if not password_grant_type_serializer.is_valid():
                    logger.error(f"serializer errors:{password_grant_type_serializer.errors}")
                    return Response(password_grant_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                username = password_grant_type_serializer.validated_data['username']
                password = password_grant_type_serializer.validated_data['password']
                access_token_details, error = AuthViewHelper.authenticate_user(user_identifier=username, password=password, client_id = client_id)
                if error:
                    return Response({"error":"Authentication Failed"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response(access_token_details, status = status.HTTP_200_OK)    
        except Exception as error:
            logger.error(f"Error:{error}")
            return Response({"error": "Internal Server Error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)