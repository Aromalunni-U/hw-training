from mongoengine import DynamicDocument, StringField, FloatField, BooleanField
from settings import (
    PARSE_COLLECTION, CRAWLER_COLLECTION,
MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required = True)
    product_name = StringField()
    instock = BooleanField()
    discount = StringField()
    sale_price = FloatField()
    mrp = StringField()

class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)
    product_name = StringField()
    regular_price = FloatField()
    images = StringField()

class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required = True)

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)