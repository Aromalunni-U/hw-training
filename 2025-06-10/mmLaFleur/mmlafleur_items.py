from mongoengine import DynamicDocument, StringField, IntField, FloatField, ListField
from settings import PARSE_COLLECTION, FAILED_COLLECTION

class ProductItem(DynamicDocument):
    meta = {"db_alias": "default", "collection":PARSE_COLLECTION}

    pdp_url = StringField()
    product_name = StringField()
    product_sku = StringField()
    original_price = FloatField()
    sales_price = FloatField()
    category = StringField()
    brand = StringField()
    total_number_of_reviews = IntField()
    
    star_1 = IntField()
    star_2 = IntField()
    star_3 = IntField()
    star_4 = IntField() 
    star_5 = IntField()

    review_text = ListField(StringField())  

class FailedItem(DynamicDocument):
    meta = {"db_alias": "default", "collection":FAILED_COLLECTION}
    url = StringField(required=True)
