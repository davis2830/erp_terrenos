from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/", views.TokenRefreshApiView.as_view(), name="token_refresh"),
    path("me/", views.ProfileView.as_view(), name="profile"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("users/", views.UserListCreateView.as_view(), name="user_list_create"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
]
