from mongoengine import DynamicDocument, StringField, FloatField, DictField, BooleanField
from settings import (
    PARSE_COLLECTION,  CRAWLER_COLLECTION
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required = True, unique = True)
    product_name = StringField()
    product_id = StringField()
    product_color = StringField()
    material = DictField()
    details = StringField()
    specification = DictField()
    price = FloatField()
    price_was = FloatField()
    breadcrumb = StringField()
    stock = BooleanField()
    images = StringField()

class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)