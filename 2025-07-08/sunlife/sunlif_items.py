from mongoengine import DynamicDocument, StringField, FloatField, BooleanField
from settings import (
    PARSE_COLLECTION, CRAWLER_COLLECTION,
MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required = True, unique = True)
    product_name = StringField()
    sales_price = FloatField()
    mrp = FloatField()
    discount = StringField()
    instock = BooleanField()


class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required = True, unique = True)

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)