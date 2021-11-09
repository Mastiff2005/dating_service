from celery import shared_task

from .models import Category
from utils.parser_data import PRODUCT_CATEGORIES
from utils.parsers import main


@shared_task
def parse_products():
    for category in PRODUCT_CATEGORIES.values():
        if not Category.objects.filter(slug=category).exists():
            main(category)
    return
