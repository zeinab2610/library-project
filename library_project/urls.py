from django.contrib import admin
from django.urls import path
from books import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home, name="home-page"),
    path('login/', views.login_page, name='login-page'),
    path('user_login', views.login_user, name='login-user'),
    path('home', views.home, name='home-page'),
    path('logout', views.logout_user, name='logout'),

    path('category', views.category, name='category-page'),
    path('create_category', views.create_category, name='create-category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit-category'),
    path('view_category/<int:pk>', views.view_category, name='view-category-pk'),
    path('save_category', views.save_category, name='save-category'),
    path('delete_category/<int:pk>', views.delete_category, name='delete-category'),

    path('books/', views.books, name='book-page'),
    path('create_book', views.create_book, name='create-book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit-book'),
    path('view_book/<int:pk>', views.view_book, name='view-book-pk'),
    path('save_book', views.save_book, name='save-book'),
    path('delete_book/<int:pk>', views.delete_book, name='delete-book'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
