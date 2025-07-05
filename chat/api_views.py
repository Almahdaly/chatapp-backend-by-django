from rest_framework import generics,permissions
from .models import Message
from .serializers import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    serializer_class=MessageSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MessageDeleteAPIView(generics.DestroyAPIView):
    queryset= Message.objects.all()
    serializer_class=MessageSerializer
    permission_classes=[permissions.IsAuthenticated]

    def delete(self,request,*args, **kwargs):
        instance= self.get_object()
        if instance.user !=request.user:
            return Response({'detail':'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        instance.deleted_at= timezone.now()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)