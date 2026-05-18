from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "success": True,
            "data": {
                "nombre": user.nombre,
                "email": user.email,
                "nivel": user.nivel,
                "exp": user.exp,
                "fecha_registro": user.fecha_registro,
            }
        }, status=status.HTTP_200_OK)
