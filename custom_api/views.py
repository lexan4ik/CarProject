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
    cars = Car.objects.all().order_by('id')

    serializer = CarSerializer(cars, many=True, context={'request': request})
    print('request', request.data)
    if request.method == 'POST':

        serializer_car = CarNewValidateSerializer(data=request.data)
        serializer_img = ImageCarSerializer(data=request.data)

        if serializer_car.is_valid():

            if serializer_img.is_valid():
                car = serializer_car.save()
                serializer_img.bulk_create(serializer_img.validated_data,car=car)
                return Response(data={'success': 'Успешно создано!'}, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError({'errors':serializer_img.errors})

        else:
            return Response(data={'errors':serializer_car.errors}, status=status.HTTP_400_BAD_REQUEST)


    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_image(request):

    images = ImageCar.objects.all()

    serializer = ImageCarSerializer(images, many=True, context={'request': request})
    print('Картинки', serializer.data)

    return Response(serializer.data)
