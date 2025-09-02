from mongoengine import DynamicDocument, StringField, FloatField, IntField, ListField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY, CRAWLER_COLLECTION
)


class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}

    pdp_url = StringField(required=True, unique=True)
    prices = FloatField()
    product_id = IntField()
    product_description = StringField()
    color = ListField()
    product_type = StringField()

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)


class ProductDataItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    product_id = IntField(required = True, unique = True)
    category_id = IntField(required = True)
    


class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    category_id = IntField(required = True, unique = True)
    category_name = StringField()
    
    
