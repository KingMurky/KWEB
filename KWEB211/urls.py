from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('lecturelist', views.lecturelist, name='lecturelist'),
    path('update', views.update, name='update'),
    path('lectureread/lecturewrite/<int:lecture_id>', views.lecturewrite, name='lecturewrite'),
    path('profile', views.profile, name='profile'),
    path('profilechange', views.profilechange, name='profilechange'),
    path('lectureread/<int:lecture_id>', views.lectureread, name='lectureread'),
]