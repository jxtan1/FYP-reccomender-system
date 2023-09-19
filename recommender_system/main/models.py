from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    product_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200) # I need to set max_length
    sold_count = models.IntegerField() #product_owner = models.ForeignKey(User, on_delete=models.CASCADE, default = 1, to_field='id')
    #description = models.TextField()

    def __str__(self):
        return str(self.product_id) + '\n' + self.name + '\n' + self.price + '\n' + self.sold_count


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
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, default=1, to_field='product_id')
    comment = models.TextField()



from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=gender_choices)

    # Add related_name to avoid clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
