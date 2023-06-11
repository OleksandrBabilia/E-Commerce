from tortoise.contrib.pydantic import pydantic_model_creator

from db_models import User, Business, Product

user_pydentic = pydantic_model_creator(User, name='User', exclude=('is_virified', 'join_date'))
user_pydenticIn = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
user_pydenticOut = pydantic_model_creator(User, name='UserOut', exclude=('password', ))

business_pydentic = pydantic_model_creator(Business, name='Business')
business_pydenticIn = pydantic_model_creator(Business, name='BusinessIn', exclude_readonly=True)

product_pydentic = pydantic_model_creator(Product, name='Product')
product_pydenticIn = pydantic_model_creator(Product, name='ProductIn', exclude=('percentage_discount', 'id', ))