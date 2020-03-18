from django.conf.urls import url

from rentalhelper.rentals.api import viewsets

urlpatterns = [
        url(
            r'^rentals/$',
            viewsets.RentalViewSet.as_view({'get':'list'}),
            name='rentals'
        ),
]
