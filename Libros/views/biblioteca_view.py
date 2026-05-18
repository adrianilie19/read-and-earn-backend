from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Libros.models import Biblioteca
from Libros.serializers import BibliotecaSerializer


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
            return Response({"success": True}, status=status.HTTP_201_CREATED)
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
