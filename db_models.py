from tortoise import Model, fields
from pydantic import BaseModel

from datetime import datetime


class User(Model):
    id = fields.IntField(pk=True, db_index=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    password = fields.CharField(max_length=60, null=False)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow)
    
    
class Business(Model):
    id = fields.IntField(pk=True, db_index=True)
    name = fields.CharField(max_length=20, null=False, unique=True)
    city = fields.CharField(max_length=50, null=False, default="Unspecified")
    region = fields.CharField(max_length=100, null=False,default="Unspecified")
    description = fields.TextField(max_length=300, null=True)
    logo = fields.CharField(max_length=200, null=False, default="business_default.jpg")
    owner = fields.ForeignKeyField('models.User', related_name='business')
    

class Product(Model):
    id = fields.IntField(pk=True, db_index=True)
    name = fields.CharField(max_length=100, null=False, db_index=True)
    category = fields.CharField(max_length=30, null=False, db_index=True)
    original_price = fields.DecimalField(max_digits=12, decimal_places=2)
    new_price = fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = fields.IntField()
    offer_expiration_date = fields.DateField(default=datetime.utcnow)
    product_image = fields.CharField(max_length=200, null=False, default="product_default.jpg")
    business = fields.ForeignKeyField('models.Business', related_name='products')
    