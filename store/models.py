from PIL import Image
from django.db import models

from accounts.models import User, StoreUser, WareHouseUser


class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


class BaseStore(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class WareHouse(BaseStore):
    user = models.OneToOneField(WareHouseUser, on_delete=models.CASCADE, related_name='ware_house')
    logo = models.ImageField(upload_to='logos')

    def save(self, *args, **kwargs):
        super(WareHouse, self).save(*args, **kwargs)
        img = Image.open(self.logo.path)

        if img.height > 100 or img.width > 100:
            size = (100, 100)
            img.thumbnail(size)
            img.save(self.logo.path)


class Store(BaseStore):
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, related_name='store')


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    short_description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products')
    price = models.DecimalField(max_digits=19, decimal_places=2)
    ware_house = models.ForeignKey(WareHouse, on_delete=models.CASCADE)


class Order(models.Model):
    customer = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()


class Subscription(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='subscriptions')
    ware_house = models.ForeignKey(WareHouse, on_delete=models.CASCADE, related_name='subscribers')
    is_approved = models.BooleanField(default=False)
