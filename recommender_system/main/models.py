from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    productId = models.IntegerField()
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.productId + '\n' + self.name + '\n' + self.description


class Review(models.Model):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ] 
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()

# need to migrate