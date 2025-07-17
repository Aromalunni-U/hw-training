from mongoengine import DynamicDocument, StringField, FloatField, ListField, DictField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY, CRAWLER_COLLECTION
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}

    pdp_url = StringField(required=True, unique=True)
    product_name = StringField()
    price_was = StringField()
    percentage_discount = StringField()
    selling_price = StringField()
    images = ListField(StringField())
    review = StringField()
    rating = StringField()
    breadcrumb = StringField()
    brand = StringField()
    size = StringField()
    color = StringField()
    material = StringField()
    care_instructions = StringField()
    properties = DictField()


class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)


class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)


class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required = True, unique = True)
    


