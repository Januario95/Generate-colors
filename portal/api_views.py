from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (
    CollaboratorSerializer,
    ItemToBuySerializer,
    CalculatorSerializer,
    MovieSerializer,
    ResourceSerializer,
    UserProfileSerializer,
    
    UserReadWriteOnlySerializer,
    UserReadOnlySerializer,
    
    AccountSerializer,
    CommentSerializer,
)
from .models import (
    Colaborator, ItemToBuy, Calculator,
    Movie, Resource, UserProfile,
    Account, Comment
)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    

class UserReadWriteViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 
                           'destroy']:
            return UserReadWriteOnlySerializer
        return UserReadOnlySerializer



class MyXMLRenderer1(XMLRenderer):
    root_name_name = 'items'
    item_tag_name = 'items'
    
class MyXMLRenderer2(XMLRenderer):
    root_name_name = 'collaborators'
    item_tag_name = 'collaborators'

class CalculatorView(APIView):
    renderer_classes = [XMLRenderer,]
    
    def get(self, request):
        calcs = Calculator.objects.all()
        calc_serializer = CalculatorSerializer(calcs, many=True)
        return Response(calc_serializer.data)


class CollaboratorView(APIView):
    # renderer_classes = [XMLRenderer,]
    renderer_classes = [MyXMLRenderer2,]
    # permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        collaborators = Colaborator.objects.all()
        colla_serializer = CollaboratorSerializer(collaborators, many=True)
        return Response(colla_serializer.data)
    
class ItemToBuyView(APIView):
    # renderer_classes = [XMLRenderer,]
    renderer_classes = [MyXMLRenderer1,]
    # permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        items = ItemToBuy.objects.all()
        items_serializer = ItemToBuySerializer(items, many=True)
        return Response(items_serializer.data)


class UserProfileViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # permission_classes = [IsAuthenticated,]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class MovieViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # permission_classes = [IsAuthenticated,]
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    
    
class ResourceViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # permission_classes = [IsAuthenticated,]
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()


class CalculatorViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [IsAuthenticated,]
    serializer_class = CalculatorSerializer
    queryset = Calculator.objects.all()


class CollaboratorViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = CollaboratorSerializer
    queryset = Colaborator.objects.all()
    

class ItemToBuyViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = ItemToBuySerializer
    queryset = ItemToBuy.objects.all()
    
    

# '//*[@id="content"]/div[2]/div[4]/pre/span[6]'
# '//*[@id="content"]/div[2]/div[4]/pre/span[9]'

# '//*[@id="content"]/div[2]/div[4]/pre/span[12]'
# '//*[@id="content"]/div[2]/div[4]/pre/span[15]'