from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from utils.logger import logger
from utils.pagination import CustomPagination

from accounts.helper.application_view_helper import ApplicationViewHelper


class ApplicationCreateViewSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    redirect_uri = serializers.URLField()
    client_type = serializers.ChoiceField(choices=['confidential', 'public'], default='public')
    grant_type = serializers.ChoiceField(choices=['password', 'client-credentials'], default='password')


class ApplicationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = ApplicationCreateViewSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"serializer error:{serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            application, error = ApplicationViewHelper.create_application(
                application_name=validated_data['name'],
                user_id=request.user.id,
                redirect_uris=validated_data['redirect_uri'],
                client_type=validated_data['client_type'],
                grant_type=validated_data['grant_type']
            )
            if error:
                logger.error(f"Failed to create application:{error}")
                return Response({"error":error}, status=status.HTTP_400_BAD_REQUEST)

            logger.info("application created successfully", extra={"application_id":application["application_id"], "client_id":application["client_id"] })
            return Response({"msg":"Application created succesfully", "data":{"application_id":application["application_id"], "client_id":application["client_id"], "client_secret":application["client_secret"]}})
        except Exception as error:
            logger.error(f"Error:{error}")
            return Response({"error": "Internal Server Error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)