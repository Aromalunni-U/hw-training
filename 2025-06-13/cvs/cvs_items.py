from mongoengine import DynamicDocument, StringField, ListField, IntField, FloatField
from settings import PARSE_COLLECTION, MONGO_COLLECTION_URL_FAILED


class ProductItem(DynamicDocument):

    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField()
    product_name = StringField()
    original_price = FloatField()
    selling_price = FloatField()
    grammage_quantity = FloatField()
    grammage_unit = StringField()
    currency = StringField()
    unique_id = StringField()
    breadcrumb = StringField()
    brand = StringField()
    rating = FloatField()
    review = IntField()
    ingredients = StringField()
    warnings = StringField()
    feeding_recommendation = StringField()
    promotion_description = StringField()
    product_description = StringField()
    product_specifications = StringField()
    images = ListField(StringField())

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_URL_FAILED}
    url = StringField(required=True)
