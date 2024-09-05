from django.core.management.base import BaseCommand
from django_seed import Seed
from accounts.models import CustomUser
from products.models import Product  # Product 모델을 불러옴
import random

class Command(BaseCommand):
    help = 'Seed the database with users and products'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # 유저 시드 생성
        seeder.add_entity(CustomUser, 10, {  # 10명의 유저 생성
            'username': lambda x: seeder.faker.user_name(),
            'email': lambda x: seeder.faker.email(),
            'password': lambda x: 'password123',  # 기본 비밀번호
        })

        # 유저 생성 후 가져옴
        inserted_pks = seeder.execute()
        users = CustomUser.objects.all()

        # 게시글 시드 생성 (20개 게시글)
        seeder.add_entity(Product, 20, {
            'title': lambda x: seeder.faker.sentence(nb_words=6),
            'description': lambda x: seeder.faker.text(),
            'created_by': lambda x: random.choice(users),  # 생성된 유저 중 하나를 작성자로 지정
            'image': None,  # 이미지 필드는 비워 둠
        })

        seeder.execute()

        self.stdout.write(self.style.SUCCESS('Successfully seeded users and products'))
