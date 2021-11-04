from django.core.mail import send_mail
from math import radians, cos, sin, asin, sqrt
from PIL import Image, ImageEnhance


def add_watermark(image, opacity=0.5, wm_interval=0):
    '''
    Наложение водяного знака (media/watermark.png)
    на аватар пользователя, регистрирующегося в приложении.
    '''

    image = Image.open(image)
    watermark = Image.open('media/watermark.png')
    assert opacity >= 0 and opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    for y in range(0, image.size[1], watermark.size[1]+wm_interval):
        for x in range(0, image.size[0], watermark.size[0]+wm_interval):
            layer.paste(watermark, (x, y))
    return Image.composite(layer,  image,  layer)


def custom_send_mail(subject, receiver):
    '''
    Отправка уведомления по email, первый параметр - о ком отправляем
    информацию, второй - кому.
    '''
    return send_mail(
        'Вы кому-то понравились!',
        f'Вы понравились {subject.username}! '
        f'Почта участника: {subject.email}',
        'info@dating-service.example',
        [receiver.email],
        fail_silently=False,
    )


def haversine(lon1, lat1, lon2, lat2):
    '''
    Вычисление расстояния большого круга между двумя точками
    на поверхности Земли, координаты которых заданы в виде
    десятичных градусов.
    '''
    # перевод десятичных градусов в радианы
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # формула гаверсинуса
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Радиус Земли 6371 км
    km = '{:.2f}'.format(6371 * c)
    return km
