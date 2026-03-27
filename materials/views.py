from datetime import timedelta

from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
)
from users.permissions import IsModer, IsOwner

from .tasks import send_course_update_info


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="description from swagger_auto_schema via method_decorator"
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModer]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModer | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [~IsModer | IsOwner]
        return super().get_permissions()

    def perform_update(self, serializer):
        course = self.get_object()
        old_updated_at = course.updated_at

        updated_course = serializer.save()

        if timezone.now() - old_updated_at > timedelta(hours=4):
            send_course_update_info.delay(updated_course.id)

    @action(detail=True, methods=["post"])
    def subscriptions(self, request, pk):
        """Метод только включает/выключает подписку, письма здесь слать не нужно"""
        course = get_object_or_404(Course, id=pk)
        if course.subscription_update.filter(pk=request.user.pk).exists():
            course.subscription_update.remove(request.user)
            message = "Подписка удалена"
        else:
            course.subscription_update.add(request.user)
            message = "Подписка добавлена"

        return Response({"message": message})


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        sub_item = Subscription.objects.filter(user=user, course=course_item)

        if sub_item.exists():
            sub_item.delete()
            message = "Подписка удалена"

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
