from django.shortcuts import render
from rest_framework import generics, permissions
from .models import PollingUnit, AnnouncedPuResults,Lga,AnnouncedLgaResults
from .serializers import PollingUnitSerializer, AnnouncedPuResultsSerializer,LgaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class AnnouncedLocalGovernmentResult(APIView):
    def get(request):
        result=AnnouncedLgaResults.objects.filter(lga_name="Ethiope West")
        return Response(result)
        

class LocalGovernmentResult(APIView):
    def get(self, request,*args, **kwargs):
        lga_id=kwargs.get('lga_id')
        try:
            # Step 2: Retrieve all polling units under the specified local government
            polling_units = PollingUnit.objects.filter(lga_id=lga_id)
            
            total_results = {}

            # Step 3: Retrieve announced results for each polling unit and aggregate by party
            for unit in polling_units:
                announced_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=unit.uniqueid)
                
                for result in announced_results:
                    party_abbreviation = result.party_abbreviation
                    party_score = result.party_score
                    
                    if party_abbreviation in total_results:
                        total_results[party_abbreviation] += party_score
                    else:
                        total_results[party_abbreviation] = party_score

            # Step 4: Return aggregated results
            return Response(total_results)

        except Exception as e:
            return Response({'error': str(e)}, status=500)



class LocalGovernmentListAPIView(generics.ListAPIView):
    queryset = Lga.objects.all()
    serializer_class = LgaSerializer
    permission_classes = [permissions.AllowAny]


class PollingUnitListAPIView(generics.ListAPIView):
    queryset = PollingUnit.objects.all()
    serializer_class = PollingUnitSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class PollingUnitDetailAPIView(generics.RetrieveAPIView):
    queryset = PollingUnit.objects.all()
    serializer_class = PollingUnitSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

class PollingUnitResultsListAPIView(generics.ListAPIView):
    serializer_class = AnnouncedPuResultsSerializer

    def get_queryset(self):
        polling_unit_id = self.kwargs['polling_unit_id']
        return AnnouncedPuResults.objects.filter(polling_unit_uniqueid=polling_unit_id)