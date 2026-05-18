from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Premios.models import Premio, Canje
from Premios.serializers import PremioSerializer


class PremiosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        premios = Premio.objects.filter(is_active=True)
        data = PremioSerializer(premios, many=True).data
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


class CanjearPremioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, premio_id):
        try:
            premio = Premio.objects.get(id=premio_id, is_active=True)
        except Premio.DoesNotExist:
            return Response({"erroresBackend": ["Premio no encontrado."]}, status=status.HTTP_404_NOT_FOUND)

        if premio.stock <= 0:
            return Response({"erroresBackend": ["Este premio no tiene stock."]}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.exp < premio.coste_exp:
            faltan = premio.coste_exp - request.user.exp
            return Response(
                {"erroresBackend": [f"Te faltan {faltan} EXP para canjear este premio."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.exp -= premio.coste_exp
        request.user.save()

        premio.stock -= 1
        premio.save()

        Canje.objects.create(
            usuario=request.user,
            premio=premio,
            exp_gastada=premio.coste_exp,
        )

        return Response({"success": True, "exp_restante": request.user.exp}, status=status.HTTP_200_OK)
