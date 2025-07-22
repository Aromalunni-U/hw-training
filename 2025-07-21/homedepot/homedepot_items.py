from mongoengine import DynamicDocument, StringField, FloatField, ListField, DictField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, CRAWLER_COLLECTION
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required = True, unique = True)
    product_name = StringField()
    brand = StringField()
    breadcrumb = StringField()
    retail_limit = StringField()
    currency = StringField()
    selling_price = FloatField()
    price_was = FloatField()
    images = ListField()
    rating = StringField()
    review = StringField()
    product_description = StringField()
    product_details = DictField()

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)

class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)