from mongoengine import DynamicDocument, StringField, FloatField
from settings import (
    PARSE_COLLECTION, CRAWLER_COLLECTION,
    MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY
)

class ProductItem(DynamicDocument):

    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    url = StringField()
    product_name = StringField()
    unique_id = StringField()
    currency = StringField()
    regulat_price =  FloatField()
    product_description = StringField()
    images = StringField()


class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required=True)

class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required=True)

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required=True)
    source = StringField(required=True)