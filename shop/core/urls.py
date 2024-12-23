from django.urls import path
from . import views


app_name = 'core'


urlpatterns = [
    path('', views.index, name='home'),
    path('about/',views.about, name='about'),
    path('product/<str:slug>/', views.product_detail, name='product_detail'),
    path('products/suggestions/', views.suggestions_proudcts, name='sugg_product'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:slug>/', views.category_detail, name='category_detail'),

    # Registrations section
    path('register/signup/', views.signup, name='signup'),
    path('register/login', views.login, name='login'),
    path('register/logout/', views.logout_user, name='logout'),
    path('register/why_logout/', views.why_logout, name='why_logout'),
    path('register/change_password/', views.change_password, name='change_password'),

    # Profile section
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='profile_edit')
]