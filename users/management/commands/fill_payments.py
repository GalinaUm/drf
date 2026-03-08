from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        Payment.objects.all().delete()

        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('В базе нет ни одного пользователя'))
            return

        if course:
            Payment.objects.create(user=user, course=course, amount=15000.00, payment_method='transfer')
            self.stdout.write(self.style.SUCCESS(f'Платеж за курс "{course.name}" создан'))
        else:
            self.stdout.write(self.style.WARNING('Предупреждение: Курсы не найдены, платеж не создан'))

        if lesson:
            Payment.objects.create(
                user=user,
                paid_lesson=lesson,
                amount=1500.00,
                payment_method='cash'
            )
            self.stdout.write(self.style.SUCCESS(f'Платеж за урок "{lesson.name}" создан'))
        else:
            self.stdout.write(self.style.WARNING('Предупреждение: Уроки не найдены, платеж не создан'))


