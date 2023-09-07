from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from userprofile.models import UserProfile
from shop.models import Category, Perfume, Cart, Cartitems, Review
from .serializers import UserProfileSerializer, UserSerializer, CategorySerializer, PerfumeSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer


# Importing searchfilter orderingfilter to implement search and sorting
from rest_framework.filters import SearchFilter, OrderingFilter
# Import for pagination
from rest_framework.pagination import PageNumberPagination
# Importing product filters from the filters.py file
from api.filters import PerfumeFilter

# Create your views here.
class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.auth.delete()
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
    # Instantiate the category object from models
    
    queryset = Category.objects.all()
    # Serialize the category object so we can render its data in a json format
    serializer_class = CategorySerializer


class PerfumesViewSet(ModelViewSet):
    queryset = Perfume.objects.all()
    serializer_class = PerfumeSerializer

    # Implementing filter and search
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PerfumeFilter
    # pagination_class = PageNumberPagination # Global pagination setting was activated, hence; we don't need again at the view level
    search_fields = ['name', 'description']
    ordering_fields = ['price']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    # queryset = Cartitems.objects.all()  #Need to apply some logic so we use get_queryset method instead
    # serializer_class = CartItemSerializer
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
         return {'cart_id': self.kwargs['cart_pk']}  # Here we're retrieving the id of the
    # particular cart and passing it to the serializer, so we can use it to add items to the cart


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all() # fetched all reviews despite the product
    serializer_class = ReviewSerializer

    # Fetches reviews based on a particular product
    def get_queryset(self):
        return Review.objects.filter(perfume_id=self.kwargs['perfume_pk']) 

    def get_serializer_context(self):
        return {"perfume_id": self.kwargs["perfume_pk"]}  # Retrieving the id of the particular
    # perfume and passing it to the serializer, so we can add the review to that particular perfume


# @api_view()
# def category_list(request):
#     # Instantiate the category object from models
#     queryset = Category.objects.all()
#     # Serialize the category object so we can render its data in a json format
#     serializer = CategorySerializer(queryset, many=True)
#     # Retrieve all the details in the serializer
#     data = serializer.data
#     return Response(data)
    
    
# @api_view()
# def category_detail(request, id):
#     # Instantiate the category object from models
#     category = get_object_or_404(Category, pk=id) # This does the work of the try except block in
#                                                   #ensuring a gentle display in the case where
#                                                   #the category is not found
#     # Serialize the category object so we can render its data in a json format
#     serializer = CategorySerializer(category)
#     # Retrieve all the details in the serializer
#     data = serializer.data
#     return Response(data)


