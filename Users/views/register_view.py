from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from Users.serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"success": True}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errores = []
            for clave, error in serializer.errors.items():
                for err in error:
                    errores.append(str(err))
            return Response({"erroresBackend": errores}, status=status.HTTP_400_BAD_REQUEST)
