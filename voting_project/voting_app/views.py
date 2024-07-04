from django.shortcuts import render
from rest_framework import generics, permissions
from .models import PollingUnit, AnnouncedPuResults,Lga,AnnouncedLgaResults
from .serializers import PollingUnitSerializer, AnnouncedPuResultsSerializer,LgaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone


'''
Solution 3
'''

class NewPollingUnitPostResults(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ward_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ward ID'),
                'lga_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Local Government Area ID'),
                'uniquewardid': openapi.Schema(type=openapi.TYPE_INTEGER, description='Unique Ward ID'),
                'polling_unit_number': openapi.Schema(type=openapi.TYPE_STRING, description='Polling unit number'),
                'polling_unit_name': openapi.Schema(type=openapi.TYPE_STRING, description='Polling unit name'),
                'polling_unit_description': openapi.Schema(type=openapi.TYPE_STRING, description='Polling unit description'),
                'lat': openapi.Schema(type=openapi.TYPE_STRING, description='Latitude'),
                'long': openapi.Schema(type=openapi.TYPE_STRING, description='Longitude'),
                'entered_by_user': openapi.Schema(type=openapi.TYPE_STRING, description='Entered by user'),
                'user_ip_address': openapi.Schema(type=openapi.TYPE_STRING, description='User IP address'),
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'party_abbreviation': openapi.Schema(type=openapi.TYPE_STRING, description='Party abbreviation'),
                            'party_score': openapi.Schema(type=openapi.TYPE_INTEGER, description='Party score')
                        }
                    )
                )
            }
        ),
        responses={201: 'Success', 400: 'Bad Request'}
    )
    def post(self, request):
        try:
        # Step 1: Create the new polling unit
            polling_unit_data = {
                'polling_unit_id':1,
                'ward_id': request.data.get('ward_id'),
                'lga_id': request.data.get('lga_id'),
                'uniquewardid': request.data.get('uniquewardid'),
                'polling_unit_number': request.data.get('polling_unit_number'),
                'polling_unit_name': request.data.get('polling_unit_name'),
                'polling_unit_description': request.data.get('polling_unit_description'),
                'lat': request.data.get('lat'),
                'long': request.data.get('long'),
                'entered_by_user': request.data.get('entered_by_user'),
                'user_ip_address': request.data.get('user_ip_address')
            }
            polling_unit_serializer = PollingUnitSerializer(data=polling_unit_data)

            if polling_unit_serializer.is_valid():
                polling_unit = polling_unit_serializer.save()
                # Update the polling unit instance to set the polling_unit_id
                polling_unit.polling_unit_id = polling_unit.uniqueid
                polling_unit.save()

                # Step 2: Store the results using the newly created polling unit's ID
                results = request.data.get('results', [])
                entered_by_user = request.data.get('entered_by_user')
                user_ip_address = request.data.get('user_ip_address')
                date_entered =datetime.now()

                # Save results for each party
                for result in results:
                    AnnouncedPuResults.objects.create(
                        polling_unit_uniqueid=polling_unit.uniqueid,
                        party_abbreviation=result['party_abbreviation'],
                        party_score=result['party_score'],
                        entered_by_user=entered_by_user,
                        date_entered=date_entered,
                        user_ip_address=user_ip_address
                    )

                return Response({'status': 'success', 'message': 'Polling unit and results saved successfully'}, status=200)

            return Response(polling_unit_serializer.errors, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

'''
Solution 2
'''
class LocalGovernmentResult(APIView):
    '''
    This endpoint is designed to get the result of an election in a local governemnt.
    This is designed in such a way that we can get the result of the local government without
    using the AnnouncedLgaResults table. To meet this task we followed the following approach
    Approach:
    filter all polling unit with the given local government id
    we iterate over the polling units to get the unique id of the polling unit
    at each iteration the unique id of the polling unit is used  to get the result of
    the polling unit.
    The result of the polling unit is then aggregated by party using a dictionary

    Assumption made:
    The polling unit id is unique
    The polling unit id is the same as the polling unit unique id
    Announced polling unit result is not filtered by the name of the LGA due to possible Human errors
    '''
    def get(self, request,*args, **kwargs):
        lga_id=kwargs.get('lga_id')
        try:
            # Step 2: Retrieve all polling units under the specified local government
            polling_units = PollingUnit.objects.filter(lga_id=lga_id)
            
            total_results = {}
            

            # Step 3: Retrieve announced results for each polling unit and aggregate by party
            for unit in polling_units:
                announced_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=unit.polling_unit_id)
                
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
        
'''
Solution one
'''

class PollingUnitResultsListAPIView(generics.ListAPIView):
    # This endpoint gives the result of a particular polling unit
    serializer_class = AnnouncedPuResultsSerializer
    def get_queryset(self):
        polling_unit_id = self.kwargs['polling_unit_id']
        return AnnouncedPuResults.objects.filter(polling_unit_uniqueid=polling_unit_id)




class LocalGovernmentListAPIView(generics.ListAPIView):
    # This endpoints gives  all the local government areas details
    queryset = Lga.objects.all()
    serializer_class = LgaSerializer
    permission_classes = [permissions.AllowAny]


class PollingUnitListAPIView(generics.ListAPIView):
    #This endpoint gives  all the polling units 
    queryset = PollingUnit.objects.all()
    serializer_class = PollingUnitSerializer
    permission_classes = [permissions.AllowAny]  

class PollingUnitDetailAPIView(generics.RetrieveAPIView):
    #This endpoint  details of a particular polling unit
    queryset = PollingUnit.objects.all()
    serializer_class = PollingUnitSerializer
    permission_classes = [permissions.AllowAny] 

