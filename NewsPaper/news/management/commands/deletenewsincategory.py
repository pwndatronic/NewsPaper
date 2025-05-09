from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = "Удаляем все новости заданной категории."

    def add_arguments(self, parser):
        parser.add_argument('--category', type=str)

    def handle(self, *args, **options):
        category = options['category']
        answer = input(f"Хотите удалить все посты в категории {category}? Y/n\n")

        if answer != 'Y':
            self.stdout.write(self.style.ERROR('Галя, отмена.'))
            return
        try:
            category_to_delete = Category.objects.get(category_name=category)
            Post.objects.filter(categories=category_to_delete).delete()
            self.stdout.write(self.style.SUCCESS(f'Посты из категории {category} удалены.'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категории {category} не существует.'))



