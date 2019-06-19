from rest_framework import viewsets
from parking.models import CarParks
from parking.serializers import CarParkSerializer

class CarParkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows list of car parks with paging of 20 per page.
    Can be filtered by any field in the features JSON object.
    """

    queryset = CarParks.objects.filter()
    serializer_class = CarParkSerializer

    def get_queryset(self):
        queryset = CarParks.objects.filter()
        for query, value in self.request.query_params.items():
            if query != "offset" and query != "limit":          
                ## I'd double check any security implications for using this
                ## technique to filter before putting this in to production.
                filter = 'features__' + query
                feature_bool = False
                if value.lower() == "true":
                    feature_bool = True
                queryset = queryset.filter(**{ filter: feature_bool })
        return queryset