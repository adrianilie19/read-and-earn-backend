from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Logros.models import Logro, LogroUsuario


class LogrosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        todos = Logro.objects.all()
        ids_completados = LogroUsuario.objects.filter(
            usuario=request.user
        ).values_list('logro_id', flat=True)

        data = [
            {
                "id": logro.id,
                "titulo": logro.titulo,
                "descripcion": logro.descripcion,
                "exp": logro.exp,
                "icono": logro.icono,
                "completado": logro.id in ids_completados,
            }
            for logro in todos
        ]

        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


class DesbloquearLogroView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, logro_id):
        try:
            logro = Logro.objects.get(id=logro_id)
        except Logro.DoesNotExist:
            return Response({"erroresBackend": ["El logro no existe."]}, status=status.HTTP_404_NOT_FOUND)

        ya_tiene = LogroUsuario.objects.filter(usuario=request.user, logro=logro).exists()
        if ya_tiene:
            return Response({"erroresBackend": ["Ya tienes este logro."]}, status=status.HTTP_400_BAD_REQUEST)

        LogroUsuario.objects.create(usuario=request.user, logro=logro)

        request.user.exp += logro.exp
        request.user.nivel = (request.user.exp // 100) + 1
        request.user.save()

        return Response({"success": True, "exp_ganada": logro.exp}, status=status.HTTP_200_OK)
