from mongoengine import DynamicDocument, StringField, FloatField, DictField, BooleanField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, CRAWLER_COLLECTION
)



class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required=True, unique=True)
    product_name = StringField()
    selling_price = FloatField()
    sku = StringField()
    part = StringField()
    breadcrumb = StringField()
    rating = StringField()
    review = StringField()
    product_description = StringField()
    container_size = StringField()
    instock = BooleanField()
    image = StringField()
    specification = DictField()
    
    

class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)
    product_name = StringField()
    sku = StringField()
    part = StringField()
    cross_reference = StringField()
    matched = StringField()



class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)