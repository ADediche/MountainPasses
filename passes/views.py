import json

from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.parsers import FormParser, MultiPartParser

from .data_manager import PerevalDataManager
from .serializers import PerevalDetailSerializer, SubmitDataSerializer
from .models import Pereval


class SubmitDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            data = json.loads(request.data.get("data", "{}"))
            serializer = SubmitDataSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {"status": 400, "message": serializer.errors, "id": None}, status=http_status.HTTP_400_BAD_REQUEST
                )

            image_files = request.FILES.getlist("images", [])
            images_data = serializer.validated_data.get("pereval", {}).get("images", [])

            if images_data and len(image_files) != len(images_data):
                return Response(
                    {
                        "status": 400,
                        "message": "Количество загруженных файлов не совпадает с количеством заголовков",
                        "id": None,
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
            manager = PerevalDataManager()
            pereval = manager.submit_data(serializer.validated_data, image_files)
            return Response(
                {
                    "status": 200,
                    "message": None,
                    "id": pereval.id
                },
                status=http_status.HTTP_200_OK
            )
        except json.JSONDecodeError:
            return Response(
                {"status": 400, "message": "Некорректный формат JSON в поле data", "id": None},
                status=http_status.HTTP_400_BAD_REQUEST,
            )
        except DatabaseError:
            return Response(
                {
                    "status": 500,
                    "message": "Ошибка подключения к базе данных",
                    "id": None
                },
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except ValueError as e:
            return Response(
                {
                    "status": 400,
                    "message": str(e),
                    "id": None
                },
                status=http_status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id is not None:
            try:
                pereval = Pereval.objects.get(id=id)
                serializer = PerevalDetailSerializer(pereval, context={"request": request})
                return Response(serializer.data, status=http_status.HTTP_200_OK)

            except Pereval.DoesNotExist:
                return Response(
                    {"status": 404, "message": "Перевал не найден", "id": None}, status=http_status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"status": 500, "message": f"Ошибка сервера: {str(e)}", "id": None},
                    status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Обработка GET /submitData/?user__email=<email>
        email = request.query_params.get("user__email")
        if not email:
            return Response({"state": 0, "message": "Email обязателен"}, status=http_status.HTTP_400_BAD_REQUEST)

        try:
            perevals = Pereval.objects.filter(user__email=email)
            serializer = PerevalDetailSerializer(perevals, many=True, context={"request": request})
            return Response(serializer.data, status=http_status.HTTP_200_OK)
        except Exception as e:
            print(f"Ошибка при получении списка перевалов: {str(e)}")
            return Response(
                {"state": 0, "message": f"Ошибка сервера: {str(e)}"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id=None):
        try:
            data = json.loads(request.data.get("data", "{}"))
            serializer = SubmitDataSerializer(data=data)
            if not serializer.is_valid():
                return Response({"state": 0, "message": serializer.errors}, status=http_status.HTTP_400_BAD_REQUEST)

            image_files = request.FILES.getlist("images", [])
            images_data = serializer.validated_data.get("pereval", {}).get("images", [])

            if images_data and not image_files:
                return Response(
                    {"state": 0, "message": "Файлы изображений не переданы"}, status=http_status.HTTP_400_BAD_REQUEST
                )

            if images_data and len(image_files) != len(images_data):
                return Response(
                    {"state": 0, "message": "Количество загруженных файлов не совпадает с количеством заголовков"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            Pereval.objects.get(id=id)

            manager = PerevalDataManager()
            area = manager.create_area(serializer.validated_data["area"])

            manager.update_pereval(
                pereval_id=id, pereval_data=serializer.validated_data["pereval"], area=area, image_files=image_files
            )
            return Response({"state": 1, "message": ""}, status=http_status.HTTP_200_OK)

        except Pereval.DoesNotExist:
            return Response({"state": 0, "message": "Перевал не найден"}, status=http_status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response(
                {"state": 0, "message": "Некорректный формат JSON в поле data"}, status=http_status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response({"state": 0, "message": str(e)}, status=http_status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"state": 0, "message": f"Неизвестная ошибка: {str(e)}"},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
