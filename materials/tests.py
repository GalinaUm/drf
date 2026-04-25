from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@sky.pro", password="0987654321admin"
        )
        self.course = Course.objects.create(name="История", owner=self.user)
        self.lesson = Lesson.objects.create(name="Киевская Русь", course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("name"),
            self.course.name,
        )

    def test_course_create(self):
        url = reverse("materials:courses-list")
        data = {"name": "Физика"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {"name": "Физика"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("name"),
            "Физика",
        )

    def test_course_delete(self):
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Course.objects.all().count(), 0)

    # def test_course_list(self):
    #     url = reverse("materials:courses-list")
    #     response = self.client.get(url)
    #     data = response.json()
    #     result = {
    #         "count": 1,
    #         "next": None,
    #         "previous": None,
    #         "results": [
    #             {
    #                 "id": self.course.pk,
    #                 "is_subscribed": False,
    #                 "name": "История",
    #                 "picture": None,
    #                 "description": None,
    #                 "owner": self.user.pk,
    #             },
    #         ],
    #     }
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)

    def test_course_list(self):
        url = reverse("materials:courses-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем структуру пагинации
        self.assertEqual(data["count"], 1)

        # Проверяем данные конкретного курса внутри списка
        course_data = data["results"][0]
        self.assertEqual(course_data["name"], "История")
        self.assertEqual(course_data["id"], self.course.pk)
        self.assertEqual(course_data["owner"], self.user.pk)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@sky.pro", password="0987654321admin"
        )
        self.course = Course.objects.create(name="История", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Киевская Русь", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("name"),
            self.lesson.name,
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "Электролиз",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "Электролиз"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("name"),
            "Электролиз",
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Lesson.objects.all().count(), 0)

    # def test_lesson_list(self):
    #     url = reverse("materials:lesson_list")
    #     response = self.client.get(url)
    #     data = response.json()
    #     print(data)
    #     result = {
    #         "count": 1,
    #         "next": None,
    #         "previous": None,
    #         "results": [
    #             {
    #                 "id": 9,
    #                 "video_url": None,
    #                 "name": self.lesson.name,
    #                 "description": None,
    #                 "picture": None,
    #                 "course": self.course.pk,
    #                 "owner": self.user.pk,
    #             },
    #         ],
    #     }
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Берем первый урок из результатов
        lesson_data = data["results"][0]

        self.assertEqual(lesson_data["name"], self.lesson.name)
        self.assertEqual(
            lesson_data["id"], self.lesson.pk
        )  # используем pk вместо цифры 9
        self.assertEqual(lesson_data["course"], self.course.pk)
