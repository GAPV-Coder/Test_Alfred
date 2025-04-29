from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from delivery.models import Address, Driver, Service
from delivery.services.service_manager import ServiceManager
from .serializers import AddressSerializer, DriverSerializer, ServiceSerializer

class AddressViewSet(viewsets.ModelViewSet):
    """
    View to manage addresses (CRUD).
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
class DriverViewSet(viewsets.ModelViewSet):
    """
    View to manage drivers (CRUD).
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
class ServiceRequestView(APIView):
    """
    View to request a new service.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        address_data = request.data.get('pickup_address')
        if not address_data:
            return Response({'error': 'The pick-up address is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        address_serializer = AddressSerializer(data=address_data)
        if not address_serializer.is_valid():
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        address = Address.objects.create(**address_serializer.validated_data)
        service, error = ServiceManager.create_service(address)
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ServiceCompleteView(APIView):
    """
    View to mark a service as completed.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({"error": f"Service with id {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if service.status == 'COMPLETED':
            return Response({'error': 'Service is already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        
        service.status = 'COMPLETED'
        if service.driver:
            service.driver.is_available = True
            service.driver.save()
        service.save()
        
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)