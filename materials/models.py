from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )

    picture = models.ImageField(
        upload_to="materials/pictures/courses",
        blank=True,
        null=True,
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание",
    )

    picture = models.ImageField(
        upload_to="materials/pictures/lessons",
        blank=True,
        null=True,
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Курс",
        help_text="Укажите курс",
    )

    video_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео (например, Youtube)",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
