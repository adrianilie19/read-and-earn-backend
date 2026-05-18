from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Libros.models import Biblioteca
from Libros.serializers import BibliotecaSerializer
from Logros.models import Logro, LogroUsuario


def comprobar_logros_biblioteca(usuario):
    total_libros = Biblioteca.objects.filter(usuario=usuario).count()

    criterios = {
        1: 'Primer libro',
        5: 'Lector habitual',
        10: 'Coleccionista',
    }

    logros_desbloqueados = []
    exp_ganada = 0

    for num_libros, nombre_logro in criterios.items():
        if total_libros >= num_libros:
            try:
                logro = Logro.objects.get(titulo=nombre_logro)
                ya_tiene = LogroUsuario.objects.filter(usuario=usuario, logro=logro).exists()
                if not ya_tiene:
                    LogroUsuario.objects.create(usuario=usuario, logro=logro)
                    usuario.exp += logro.exp
                    exp_ganada += logro.exp
                    logros_desbloqueados.append(nombre_logro)
            except Logro.DoesNotExist:
                pass

    if logros_desbloqueados:
        usuario.nivel = (usuario.exp // 100) + 1
        usuario.save()

    return logros_desbloqueados, exp_ganada


class BibliotecaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        libros = Biblioteca.objects.filter(usuario=request.user)
        data = [
            {
                "id": l.id,
                "gutendex_id": l.gutendex_id,
                "titulo": l.titulo,
                "autor": l.autor,
                "portada_url": l.portada_url,
                "progreso": l.progreso,
                "estado": l.estado,
                "fecha_agregado": l.fecha_agregado,
            }
            for l in libros
        ]
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BibliotecaSerializer(data=request.data)
        if serializer.is_valid():
            ya_existe = Biblioteca.objects.filter(
                usuario=request.user,
                gutendex_id=serializer.validated_data['gutendex_id']
            ).exists()

            if ya_existe:
                return Response(
                    {"erroresBackend": ["Este libro ya está en tu biblioteca."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(usuario=request.user)

            logros_nuevos, exp_ganada = comprobar_logros_biblioteca(request.user)

            return Response({
                "success": True,
                "logros_desbloqueados": logros_nuevos,
                "exp_ganada": exp_ganada,
                "exp": request.user.exp,
                "nivel": request.user.nivel,
            }, status=status.HTTP_201_CREATED)
        else:
            errores = []
            for clave, error in serializer.errors.items():
                for err in error:
                    errores.append(str(err))
            return Response({"erroresBackend": errores}, status=status.HTTP_400_BAD_REQUEST)


class BibliotecaDetalleView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, libro_id):
        try:
            libro = Biblioteca.objects.get(id=libro_id, usuario=request.user)
        except Biblioteca.DoesNotExist:
            return Response({"erroresBackend": ["Libro no encontrado."]}, status=status.HTTP_404_NOT_FOUND)

        progreso = request.data.get('progreso')
        if progreso is None:
            return Response({"erroresBackend": ["Falta el campo progreso."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            progreso = int(progreso)
        except ValueError:
            return Response({"erroresBackend": ["El progreso debe ser un número."]}, status=status.HTTP_400_BAD_REQUEST)

        if progreso < 0 or progreso > 100:
            return Response({"erroresBackend": ["El progreso debe estar entre 0 y 100."]}, status=status.HTTP_400_BAD_REQUEST)

        libro.progreso = progreso

        if progreso == 0:
            libro.estado = "Por comenzar"
        elif progreso == 100:
            libro.estado = "Completado"
        else:
            libro.estado = "En progreso"

        libro.save()
        return Response({"success": True, "progreso": libro.progreso, "estado": libro.estado}, status=status.HTTP_200_OK)

    def delete(self, request, libro_id):
        try:
            libro = Biblioteca.objects.get(id=libro_id, usuario=request.user)
        except Biblioteca.DoesNotExist:
            return Response({"erroresBackend": ["Libro no encontrado."]}, status=status.HTTP_404_NOT_FOUND)

        libro.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)