from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from Users.serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            errores = []
            for clave, error in serializer.errors.items():
                for err in error:
                    errores.append(str(err))
            return Response({"erroresBackend": errores}, status=status.HTTP_400_BAD_REQUEST)
