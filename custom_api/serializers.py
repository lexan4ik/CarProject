from django.core.validators import FileExtensionValidator
from rest_framework import serializers


from main.models import Car, ImageCar, Model, Color, Brand


# class CarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car
#         fields = '__all__'



class BrandSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    brand = serializers.CharField(max_length=50)
    # image = serializers.ImageField(allow_null=True, allow_empty_file=True)

class ModelSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    model = serializers.CharField(max_length=150)
    brand = BrandSerializer(read_only=True)

class ColorSerializer(serializers.Serializer):

     id = serializers.IntegerField()
     color = serializers.CharField(max_length=50)



# class ImageCarSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ImageCar
#         fields = '__all__'


class ImageCarSerializer(serializers.Serializer):
    """
     Сериализатор для модели ImageCar (Изображения автомобиля).
     Поддерживает массовое создание изображений для автомобиля.

     Поля:
         is_main_image: ImageField - Главное изображение автомобиля (необязательное)
         images: ListField из ImageField - Дополнительные изображения (только для записи)
                Допустимые форматы: jpeg, jpg, png, webp

     Методы:
         create: Создает одно изображение
         bulk_create: Создает несколько изображений для автомобиля
     """
    is_main_image = serializers.ImageField(required=False)
    image = serializers.ListField(
        child=serializers.ImageField(
            validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'webp'])]
        ),
        required=False,
        write_only=True
    )

    def create(self, validated_data):
        """
        Создает одну запись изображения автомобиля.

        Args:
            validated_data: Валидированные данные для создания изображения
        """
        return ImageCar.objects.create(**validated_data)

    def bulk_create(self, images_data, car):
        """
        Массовое создание изображений для автомобиля.

        Args:
            images_data: Словарь с данными изображений:
                        - is_main_image: главное изображение
                        - images: список дополнительных изображений
            car: Экземпляр автомобиля, к которому привязываются изображения
        """
        is_main_image = images_data.get('is_main_image')
        images = images_data.get('image', [])
        print('картинки', images_data)
        # Создаем главное изображение если оно предоставлено
        if is_main_image:
            self.create({'image': is_main_image, 'is_main': True, 'car': car})

        # Создаем дополнительные изображения
        for image in images:
            self.create({'image': image, 'is_main': False, 'car': car})
    #
    # is_main_image = serializers.ImageField()
    # image = serializers.ListField(
    #     child=serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'webp'])]),
    #     required=False,
    #     write_only=True
    # )
    #
    # def create(self, validated_data,**kwargs):
    #
    #     img = ImageCar.objects.create(**kwargs)
    #
    #     return img
    #
    # def bulk_create(self, validated_data, car):
    #     is_main_image = validated_data.pop('is_main_image')
    #     images = validated_data.pop('image', [])
    #
    #     if images:
    #         if is_main_image:
    #             self.create(validated_data=validated_data, is_main=True, car=car, image=is_main_image)
    #         for image in images:
    #             self.create(validated_data=validated_data, image=image, car=car)



class CarSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    model = ModelSerializer()
    color = ColorSerializer(many=True)
    imagecar_set = ImageCarSerializer(many=True)


class CarNewValidateSerializer(serializers.ModelSerializer):

    #imagecar_set = ImageCarSerializer(many=True)
    # is_main_image = serializers.ImageField()
    # image = serializers.ListField(
    #     child=serializers.ImageField(),
    #     required=False,
    #     write_only=True
    # )

    class Meta:
        model = Car

        fields = ['name', 'price', 'description', 'model', 'color']

    def create(self, validated_data):
        print('валид данные', validated_data)
        # is_main_image = validated_data.pop('is_main_image')
        # image = validated_data.pop('image', [])
        # print(image)
        # print(is_main_image)
        colors = validated_data.pop('color')

        car = Car.objects.create(name=validated_data.get('name'),
                                 price=validated_data.get('price'),
                                 description=validated_data.get('description'),
                                 model=validated_data.get('model'),
                                 brand=validated_data.pop('model').brand)

        car.color.set(colors)

        return car








class CarValidateSerializer(serializers.Serializer):

    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    model = serializers.IntegerField()
    color = serializers.ListField(
        child=serializers.IntegerField()
    )
    # main_image_set = serializers.ImageField()
    # imagecar_set = serializers.ImageField()
    #brand = serializers.IntegerField()
    # def validate_brand(self, value):
    #     if not Model.objects.filter(brand__id=value).exists():
    #         raise serializers.ValidationError('Такого бренда не существует')
    #     return Model.objects.filter(brand__id=value).first()


    def validate_model(self, value):
        try:
            return Model.objects.get(id=value)
        except Model.DoesNotExist:
            raise serializers.ValidationError('Такой модели не существует')


    def validate_colors(self, value):
        colors = Color.objects.all().filter(id__in=value).count()
        if colors != len(value):
            raise serializers.ValidationError('Один или несколько цветов не существует.')
        return value

    # def validate_brand(self, value):
    #     if not Brand.objects.filter(id=value).exists():
    #         raise serializers.ValidationError('Такой модели не существует')
    #     return value

    def create(self, validated_data):
        model = validated_data.pop('model')
        colors = validated_data.pop('color')

        car = Car.objects.create(model=model, brand=model.brand, **validated_data)

        car.color.set(colors)

        return car


