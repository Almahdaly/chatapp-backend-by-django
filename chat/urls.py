from django.urls import path
from . import views
from . import api_views
app_name='chat'

urlpatterns = [
    path('',views.chat_view, name='chat'),
    path('delete/<int:message_id>/',views.delete_message,name="delete"),

    #api urls
    path('api/message/',api_views.MessageListCreateAPIView.as_view(),name='api-messages'),
    path('api/message/<int:pk>/',api_views.MessageDeleteAPIView.as_view(),name='api-delete-messages'),
]
