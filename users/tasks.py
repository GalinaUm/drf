from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


@shared_task
def block_inactive_users():
    """
    Проверяет пользователей и блокирует тех, кто не заходил более 30 дней.
    """
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True,
        last_login__isnull=False
    )

    count = inactive_users.count()

    if count > 0:
        inactive_users.update(is_active=False)
        logger.info(f"Заблокировано пользователей: {count}")
    else:
        logger.info("Неактивных пользователей для блокировки не найдено")

    return f"Обработка завершена. Заблокировано: {count}"
