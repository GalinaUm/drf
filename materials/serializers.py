from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_with_the_same_course_count = SerializerMethodField()

    def get_lessons_with_the_same_course_count(self, lesson):
        return Lesson.objects.filter(course=lesson).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'lessons_with_the_same_course_count')
