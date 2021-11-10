from celery import shared_task

from utils.parser_data import PRODUCT_CATEGORIES
from utils.parsers import main


@shared_task
def parse_products():
    for category in PRODUCT_CATEGORIES.keys():
        main(category)
    return
