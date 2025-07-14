from mongoengine import DynamicDocument, StringField, FloatField, ListField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY, CRAWLER_COLLECTION
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required = True, unique = True)
    product_name = StringField()
    regular_price = FloatField()
    brand = StringField()
    net_quantity = StringField()
    country_of_origin = StringField()
    description = StringField()
    care_instructions = StringField()
    material_composition = StringField()
    clothing_fit = StringField()
    images = ListField()
    color = ListField()
    product_breadcrumb = StringField()
    sku = StringField()
    size = ListField()
   

class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)
    product_name = StringField()
    brand = StringField()
    selling_price = FloatField()

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)


class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required = True, unique = True)
    