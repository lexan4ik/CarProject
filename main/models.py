from django.db import models


# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    model = models.ForeignKey('Model', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    color = models.ManyToManyField(to='Color')

    def __str__(self):
        return f'{self.model} - {self.brand} - {self.price}'

    # @property
    # def main_image(self):
    #     return self.imagecar_set.select_related().filter(is_main=True).first()
    @property
    def main_image(self):
        # Используем предзагруженные данные, если они есть
        if hasattr(self, 'main_images'):
            return self.main_images[0] if self.main_images else None
        # Фоллбек на обычный запрос, если prefetch не использовался
        return self.imagecar_set.filter(is_main=True).first()

class Color(models.Model):

    color = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.color}'

class Model(models.Model):
    model = models.CharField(max_length=150)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.model}'

class Brand(models.Model):
    brand = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.brand}'

class ImageCar(models.Model):
    image = models.ImageField()
    is_main = models.BooleanField(default=False)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car}'

