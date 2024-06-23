from django.urls import path
from . import views

urlpatterns = [
    path('local_governments/results/<str:lga_id>', views.LocalGovernmentResult.as_view(), name='local_government_results'),
    path('local_governments/', views.LocalGovernmentListAPIView.as_view(), name='local_governments'),
    path('polling_units/', views.PollingUnitListAPIView.as_view(), name='polling_units'),
    path('polling_units/<int:pk>/', views.PollingUnitDetailAPIView.as_view(), name='polling_unit_detail'),
    path('polling_units/<int:polling_unit_id>/results/', views.PollingUnitResultsListAPIView.as_view(), name='polling_unit_results'),
]
