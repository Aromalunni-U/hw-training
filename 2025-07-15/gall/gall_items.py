from mongoengine import DynamicDocument, StringField, FloatField, BooleanField
from settings import (
    PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED, MONGO_COLLECTION_CATEGORY, CRAWLER_COLLECTION
)

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField(required = True, unique = True)
    product_name = StringField()
    regular_price = FloatField()
    price_was = FloatField()
    percentage_discount = StringField()
    product_description = StringField()
    breadcrumb = StringField()
    rating = StringField()
    review = StringField()
    image = StringField()
    alchole_percentage = StringField()
    ingredient = StringField()
    allergens = StringField()
    alchol_by_volume = StringField()
    instock = BooleanField()
    nutritions = StringField()

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required = True)
    source = StringField(required = True)


class ProductUrlItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": CRAWLER_COLLECTION}
    url = StringField(required = True, unique = True)
    product_name = StringField()
    regular_price = FloatField()
    alchole_by_volume = StringField()
    image = StringField()

    
class CategoryItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    url = StringField(required = True, unique = True)
    


