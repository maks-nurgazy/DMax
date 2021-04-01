from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField()
    is_ware_house = models.BooleanField(default=True)


class WareHouseManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_ware_house=True)


class WareHouseUser(User):
    objects = WareHouseManager()

    class Meta:
        proxy = True


class StoreManager(Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_ware_house=False)


class StoreUser(User):
    objects = StoreManager()

    class Meta:
        proxy = True
