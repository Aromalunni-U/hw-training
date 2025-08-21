from mongoengine import DynamicDocument, StringField, FloatField, DictField, IntField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY, CRAWLER_COLLECTION
)


class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}

    pdp_url = StringField(required=True, unique=True)
    product_name = StringField()
    review = StringField()
    rating = StringField()
    selling_price = FloatField()
    regular_price = FloatField()
    ingredients = StringField()
    warning = StringField()
    specification = DictField()
    promotion_description = StringField()
    product_description = StringField()
    image = StringField()

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)
    status_code = IntField()


class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)
    product_name = StringField(required = True)
    image = StringField(required = True)
    

class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required = True, unique = True)
    