from django.db import models

# Create your models here.

class Car(models.Model):
    model = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'{self.model} - {self.brand} - {self.price}'

class Brand(models.Model):
    brand = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.brand}'

class ImageCar(models.Model):
    image = models.ImageField()
    car = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car}'