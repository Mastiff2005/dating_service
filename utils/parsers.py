import logging
import requests
import urllib.request
from urllib.parse import urlencode
from bs4 import BeautifulSoup

import products

from .parser_data import PRODUCT_CATEGORIES
from products.models import Category, Product

URL = 'https://www.citilink.ru/catalog/'
PARAMS = {}


def get_products(category):
    # Создаем пустой список для найденных продуктов
    result_block = []
    # Находим категорию в словаре по названию
    try:
        category = PRODUCT_CATEGORIES[category]
    except KeyError:
        logging.error('Категории нет в списке!')
    # Находим количество страниц
    url = URL + category + '/?' + urlencode(PARAMS)
    try:
        response = urllib.request.urlopen(url).read().decode('utf-8')
    except requests.exceptions.ConnectTimeout as e:
        logging.error('Время ожидания истекло')
        raise e
    soup = BeautifulSoup(response, features='lxml')
    block = soup.find(
        'div', {'class': 'Subcategory__count js--Subcategory__count'}
    )
    if block is None:
        pages_number = 1
    else:
        block_text = block.text
        products_found = [int(s) for s in block_text.split() if s.isdigit()][0]
        pages_number = (products_found // 48) + 1
    # Перебираем страницы выдачи результатов поиска
    for page_number in range(1, pages_number + 1):
        PARAMS.update({'p': page_number})
        url = URL + category + '/?' + urlencode(PARAMS)
        try:
            response = urllib.request.urlopen(url).read().decode('utf-8')
        except requests.exceptions.ConnectTimeout as e:
            logging.error('Время ожидания истекло')
            raise e
        soup = BeautifulSoup(response, features='lxml')
        # Находим все карточки товаров на данной странице
        block = str(soup.find_all(
            'div', {
                'class': 'product_data__gtm-js product_data__pageevents-js '
                         'ProductCardHorizontal js--ProductCardInListing '
                         'js--ProductCardInWishlist'
            }
        ))
        parsed_block = parse_products(category, product_cards=block)

        # Добавляем товары в базу
        p_category = Category.objects.get_or_create(slug=category)[0]
        for product in parsed_block:
            item = Product.objects.get_or_create(
                name=product['name'],
                category=p_category,
                price=product['price'],
                image_url=product['image']
            )[0]
            item.save()

        # Добавляем в общий список
        result_block += parsed_block
    return result_block


def parse_products(category, product_cards=None):
    soup = BeautifulSoup(product_cards, features='lxml')
    block = soup.find_all(
        'div', {
            'class': 'product_data__gtm-js product_data__pageevents-js '
                     'ProductCardHorizontal js--ProductCardInListing '
                     'js--ProductCardInWishlist'
        }
    )
    # Создаем пустой список товаров
    products_list = []
    for card in block:
        # Создаем словарь для каждого товара
        product = {}

        # Категория
        product['category'] = category

        # Название
        product_name_div = card.find(
            'div', {'class': 'ProductCardHorizontal__header-block'}
        )
        name = product_name_div.find('a').text
        product['name'] = ' '.join(name.replace('\n', ' ').split())

        # Цена
        product_price_div = card.find(
            'div', {'class': 'ProductCardHorizontal__price-block'}
        )
        if product_price_div is None:
            product['price'] = float(0)
        else:
            price = product_price_div.find(
                'span', {
                    'class': 'ProductCardHorizontal__price_current-price '
                             'js--ProductCardHorizontal__price_current-price'
                }
            ).text
            product['price'] = float(price.strip().replace(' ', ''))

        # Картинка
        product_image_div = card.find(
            'div', {'class': 'ProductCardHorizontal__image-block'}
        )
        image = product_image_div.find('img')['src']
        product['image'] = image

        # Собираем карточки продуктов в список
        products_list.append(product)
    return products_list


def main(category):
    get_products(category)
