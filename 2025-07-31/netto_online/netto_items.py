from mongoengine import DynamicDocument, StringField, FloatField, BooleanField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY, CRAWLER_COLLECTION
)


class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}

    pdp_url = StringField(required=True, unique=True)
    product_name = StringField()
    product_id = StringField()
    currency = StringField()
    selling_price = FloatField()
    price_was = FloatField()
    brand = StringField()
    rating = StringField()
    review = StringField()
    breadcrumb = StringField()
    instock = BooleanField()
    promotion_description = StringField()
    product_description = StringField()
    image = StringField()


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
    
