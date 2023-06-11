from tortoise.contrib.pydantic import pydentic_model_creator

from .db_models import User, Business, Product

user_pydentic = pydentic_model_creator(User, name='User', exclude=('is_virified', ))
user_pydenticIn = pydentic_model_creator(User, name='UserIn', exclude_readonly=True)
user_pydenticOut = pydentic_model_creator(User, name='UserOut', exclude=('password', ))

business_pydentic = pydentic_model_creator(Business, name='Business')
business_pydenticIn = pydentic_model_creator(Business, name='BusinessIn', exclude_readonly=True)

product_pydentic = pydentic_model_creator(Product, name='Product')
product_pydenticIn = pydentic_model_creator(Product, name='ProductIn', exclude=('percentage_discount', 'id', ))