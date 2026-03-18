from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube


class LessonSerializer(serializers.ModelSerializer):
    video_url  = serializers.CharField(validators=[validate_youtube], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed =  serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, course):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=course).exists()
        return False


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_with_the_same_course_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    def get_lessons_with_the_same_course_count(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "lessons_with_the_same_course_count",
            "lessons",
        )
