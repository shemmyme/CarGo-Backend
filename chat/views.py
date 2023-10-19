from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from userside.models import *
from userside.serializers import *
from rest_framework.views import APIView
from .serializer import *
from .models import *
from rest_framework.generics import *


@api_view(["GET"])
def Adminfetch(request):
    try:
        admin = User.objects.get(is_staff=True)
        adminId = admin.id
        print(adminId,'adminnsnsnsnsnsnnnsnsnns............')
        return Response({"admin_id": adminId}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"message": "Admin not found"}, status=status.HTTP_404_NOT_FOUND
        )


class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Messages.objects.filter(
            thread_name=thread_name
        )
        print(queryset,'queryyyysetttt')
        return queryset