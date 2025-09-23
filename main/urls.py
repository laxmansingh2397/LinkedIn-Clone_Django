from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.default, name='default'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('add-experience/', views.add_experience, name="add_experience"),
    # connection actions
    path('connect/send/<int:to_user_id>/', views.send_connection, name='send_connection'),
    path('connect/accept/<int:connection_id>/', views.accept_connection, name='accept_connection'),
    path('connect/reject/<int:connection_id>/', views.reject_connection, name='reject_connection'),
    path('connect/withdraw/<int:connection_id>/', views.withdraw_connection, name='withdraw_connection'),
    path('connect/accept-from/<int:from_user_id>/', views.accept_connection_from, name='accept_connection_from'),
    path('connect/reject-from/<int:from_user_id>/', views.reject_connection_from, name='reject_connection_from'),
    path('connect/withdraw-to/<int:to_user_id>/', views.withdraw_connection_to, name='withdraw_connection_to'),
    path('connections/', views.my_connections, name='connections'),
    path('notification/<int:notif_id>/', views.mark_notification, name='mark_notification'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)