from mongoengine import DynamicDocument, StringField, FloatField, ListField
from settings import (
    PARSE_COLLECTION, CRAWLER_COLLECTION,
    MONGO_COLLECTION_URL_FAILED
)


class ProductItem(DynamicDocument):

    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    url = StringField()
    product_name = StringField()
    regular_price = FloatField()
    color = ListField()
    sku = StringField()
    size = ListField()
    fabric_type = StringField()
    rating = StringField()
    review = StringField()
    pattern = StringField()
    pocket = StringField()
    clothing_fit = StringField()
    sleeve_type = StringField()
    collar_type = StringField()
    clothing_length = StringField()
    product_description = StringField()
    images = ListField(StringField())

class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required=True)
    product_name = StringField()
    regular_price = FloatField()
    image = StringField()

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required=True)
    source = StringField(required=True)
