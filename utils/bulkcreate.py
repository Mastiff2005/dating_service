import random
from users.models import User

User.objects.bulk_create([User(
    username='VasyOK',
    gender=random.choice('MF'),
    latitude=random.uniform(0.0, 90.0),
    longitude=(random.uniform(-180.0, 180.0))
) for index in range(100)])
