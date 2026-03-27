from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Course


@shared_task
def send_course_update_info(course_id):
    course = Course.objects.get(pk=course_id)
    subscribers_emails = course.subscription_update.values_list("email", flat=True)

    if subscribers_emails:
        send_mail(
            subject=f"Обновление курса {course.name}",
            message=f'Курс "{course.name}" был обновлен. Зайдите посмотреть новые материалы!',
            from_email=EMAIL_HOST_USER,
            recipient_list=list(subscribers_emails),
            fail_silently=False,
        )


# celery -A config worker --loglevel=info -P solo
