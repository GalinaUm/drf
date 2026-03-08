from django.urls import path
from users.apps import UsersConfig
from users.views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView, PaymentListAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user_list"),
    path("create/", UserCreateAPIView.as_view(), name="user_create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_get"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
]
