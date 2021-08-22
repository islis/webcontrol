from django.urls import path
from .views import AddRoom, RoomView, RoomUpdate, RoomDelete

app_name = 'room'

urlpatterns = [
    path('add/', AddRoom.as_view(), name='add_room'),
    path('<int:pk>/', RoomView.as_view(), name='detail_room'),
    path('<int:pk>/edit/', RoomUpdate.as_view(), name='edit_room'),
    path('<int:pk>/delete/', RoomDelete.as_view(), name='delete_room'),
]