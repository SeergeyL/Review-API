from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api import views

urlpatterns = [

    # Titles
    path('titles/', views.Titles.as_view()),
    path('titles/<int:pk>/', views.TitleDetail.as_view()),

    # Genres
    path('genres/', views.Genres.as_view()),
    path('genres/<str:slug>/', views.GenreDetail.as_view()),

    # Categories
    path('categories/', views.Categories.as_view()),
    path('categories/<str:slug>/', views.CategoryDetail.as_view()),

    # Reviews
    path('titles/<int:title_id>/reviews/', views.Reviews.as_view()),
    path('titles/<int:title_id>/reviews/<int:review_id/>', views.Reviews.as_view()),

    # Comments
    path('titles/<int:title_id>/reviews/<int:review_id>/comments',
         views.Comments.as_view()),
    path('titles/<int:title_id>/reviews/<int:review_id>/comments/<int:comment_id>/',
         views.CommentDetail.as_view()),

    # Auth
    path('auth/email/', views.email_auth, name='email_auth'),
    path('auth/token/', views.user_auth, name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('users/', views.Users.as_view()),
    path('users/me/', views.UserProfile.as_view()),
    path('users/<str:email>/', views.UserDetail.as_view()),
]
