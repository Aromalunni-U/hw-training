from mongoengine import DynamicDocument, StringField, FloatField, ListField
from settings import (
    PARSE_COLLECTION, CRAWLER_COLLECTION,
    MONGO_COLLECTION_URL_FAILED
)


class ProductItem(DynamicDocument):

    meta = {"db_alias": "default", "collection": PARSE_COLLECTION}
    pdp_url = StringField()
    product_name = StringField()
    regular_price = FloatField()
    art_number = StringField()
    material_composition = StringField()
    clothing_length = StringField()
    clothing_fit = StringField()
    country_of_origin = StringField()
    neck_style = StringField()
    style = StringField()
    care_instruction = StringField()
    color = StringField()
    sleeve_length_style = StringField()
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