from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('search/', views.search, name='search'),
    path('khabar/<int:khabar_id>/', views.khabar_show, name='khabar_show'),
    path('khabar/<int:khabar_id>/like/', views.khabar_like, name='khabar_like'),
    path('khabar/<int:khabar_id>/comment/', views.add_comment, name='add_comment'),
    path('khabar/<int:khabar_id>/delete/', views.delete_khabar, name='delete_khabar'),
    path('khabar/<int:khabar_id>/edit/', views.edit_khabar, name='edit_khabar'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('generate-ai-content/', views.generate_ai_content, name='generate_ai_content'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
]
