from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from custom_api.serializers import CarSerializer, ImageCarSerializer, CarValidateSerializer, CarNewValidateSerializer
from main.models import Car, ImageCar


# from custom_api.serializers import CarSerializer
#
# class ProductList(generics.ListCreateAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#
# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer

@api_view(['GET', 'POST'])
def get_all_car(request):
    """
    Обработчик для работы с автомобилями.

    Поддерживает методы:
    - GET: Получение списка всех автомобилей
    - POST: Создание нового автомобиля с изображениями

    Примеры запросов:

    1. GET /cars/
    Возвращает:
    [
        {
            "id": 1,
            "name": "Toyota Camry",
            "price": 25000.00,
            "description": "Седан бизнес-класса",
            "model": {
                "id": 1,
                "model": "Camry",
                "brand": {"id": 1, "brand": "Toyota"}
            },
            "color": [{"id": 1, "color": "Черный"}],
            "imagecar_set": [
                {"id": 1, "image": "http://example.com/camry.jpg", "is_main": true}
            ],
            "main_image": {"id": 1, "image": "http://example.com/camry.jpg", "is_main": true}
        }
    ]

    2. POST /cars/
    Параметры формы:
    - name (обязательный): Название автомобиля
    - price (обязательный): Цена (десятичное число)
    - description (обязательный): Описание
    - model (обязательный): ID модели
    - color (обязательный): Список ID цветов
    - is_main_image (опционально): Главное изображение (файл)
    - image (опционально): Дополнительные изображения (список файлов)

    Успешный ответ:
    {"success": "Успешно создано!"}

    Ошибки:
    - 400: Некорректные данные (автомобиль или изображения)
    """
    # Обработка GET-запроса
    if request.method == 'GET':
        cars = Car.objects.all().order_by('id')
        serializer = CarSerializer(cars, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Обработка POST-запроса
    if request.method == 'POST':
        # Валидация данных автомобиля
        car_serializer = CarNewValidateSerializer(data=request.data)
        image_serializer = ImageCarSerializer(data=request.data)

        if not car_serializer.is_valid():
            return Response(
                {'errors': car_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not image_serializer.is_valid():
            return Response(
                {'errors': image_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Сохранение автомобиля и изображений
        try:
            car = car_serializer.save()
            image_serializer.bulk_create(image_serializer.validated_data, car=car)
            return Response(
                {'success': 'Успешно создано!'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Обработка неподдерживаемых методов
    return Response(
        {'error': 'Метод не разрешен'},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(['GET'])
def get_all_image(request):

    images = ImageCar.objects.all()

    serializer = ImageCarSerializer(images, many=True, context={'request': request})
    print('Картинки', serializer.data)

    return Response(serializer.data)

@api_view(['GET'])
def search_cars(request):
    cars = Car.objects.filter(description__icontains=request.query_params.get('brand'))

    serializer = CarSerializer(cars, many=True, context={'request': request})

    print(request.query_params)

    return Response(serializer.data)

