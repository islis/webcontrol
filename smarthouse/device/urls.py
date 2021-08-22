from django.urls import path
from .views import AddDevice, DeviceView, device_state, DeviceList, DeviceDelete, EditDevice

urlpatterns = [
    path('add/', AddDevice.as_view(), name='add_device'),
    path('<int:pk>/', DeviceView.as_view(), name='device-info'),
    path('set-state/', device_state, name='state'),
    path('device-list/', DeviceList.as_view(), name='device-list'),
    path('<int:pk>/delete/', DeviceDelete.as_view(), name='device-delete'),
    path('<int:pk>/edit/', EditDevice.as_view(), name='device-edit'),
]
