from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from shop.models import Perfume, PerfumeImage, Category, Review, Cart, Cartitems
from order.models import Order, OrderItem
from userprofile.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'email', 'phone_number', 'shipping_address', 'billing_address', 'profile_picture']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']  # Include other fields as needed
        extra_kwargs = {'password': {'write_only': True}}  # To hide password when serialized

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'gender', 'slug']


class PerfumeImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = PerfumeImage
            fields = ['id', 'perfume', 'image']


class PerfumeSerializer(serializers.ModelSerializer):
    images = PerfumeImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Perfume # The images, category uploaded_images field was removed in the fields below since it was commented above
        fields = ['id', 'name', 'description', 'price', 'inventory', 'images', 'uploaded_images']
    
    # Serializing the category field to have more context 
    # category = CategorySerializer()
    

    # The method will store the details in the two tables. But how do we write the test to
    # ensure it has stored in the two tables. The listfield we used to create the
    # uploaded_images variable is not supported in HTML browser, we had to make use of
    # postman, maybe that's why its giving issues to test
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images") # Removes the uploaded images from the list of data
        perfume = Perfume.objects.create(**validated_data) #unpacks the validated data

        for image in uploaded_images:
            new_perfume_image = PerfumeImage.objects.create(perfume=perfume, image=image)

        return perfume

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.save()

        if uploaded_images:
            instance.images.all().delete()
            for image in uploaded_images:
                PerfumeImage.objects.create(perfume=instance, image=image)

        return instance


class SimplePerfumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfume
        fields = ['id','name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    perfume = SimplePerfumeSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
            model = Cartitems
            fields = ['id', 'perfume', 'quantity', 'sub_total']

    def total(self,cartitem:Cartitems):
         return cartitem.quantity * cartitem.perfume.price


class AddCartItemSerializer(serializers.ModelSerializer):
    perfume_id = serializers.UUIDField()
    class Meta:
          model = Cartitems
          fields = ['id', 'perfume_id', 'quantity']
    
    def validate_perfume_id(self, value):
        # Methd to check if there's a perfume in the database with the received id
        # Since we cant add a non existent product to cart
         if not Perfume.objects.filter(pk=value).exists():
              raise serializers.ValidationError('There is no perfume associated with the given ID')
         
         return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id'] # This was passed through the cartitemviewset
        perfume_id = self.validated_data['perfume_id']
        quantity = self.validated_data['quantity'] 

        # We want to only save the cart item if it was received from the client, else we create it
        try:
            #  This block will update the item in the cart if it exists already
             cartitem = Cartitems.objects.get(perfume_id=perfume_id, cart_id=cart_id)
             cartitem.quantity += quantity
             cartitem.save()

             self.instance = cartitem
        except:
            #  This block will create the item in the cart if it wasnt there already
            # self.instance = Cartitems.objects.create(perfume_id=perfume_id, cart_id=cart_id, quantity=quantity)
            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance  


class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cartitems
        fields = ['quantity']  
     

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="cart_total")
    
    class Meta:
            model = Cart
            fields = ['id', 'items', 'grand_total']

    def cart_total(self, cart: Cart):
         items = cart.items.all()
         total = sum([item.quantity * item.perfume.price for item in items])
         return total
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
            model = Review
            fields = ['id', 'perfume', 'date_created', 'description', 'customer_name']

    # Overiding the create method for review so as to use the context passed from the view class
    def create(self, validated_data):
        perfume_id = self.context["perfume_id"] # This was passed through the Reviewviewset
        return Review.objects.create(perfume_id = perfume_id, **validated_data)
    


class OrderItemSerializer(serializers.ModelSerializer):
     perfume = SimplePerfumeSerializer()

     class Meta:
          model = OrderItem
          fields = ['id', 'perfume', 'price', 'quantity']



class OrderSerializer(serializers.ModelSerializer):
     items = OrderItemSerializer(many = True)

     class Meta:
          model = Order
          fields = ['id', 'user', 'created_at', 'status', 'items']


class UpdateOrderSerializer(serializers.ModelSerializer):
     class Meta:
          model = Order
          fields = ['status']


class CreateOrderSerilaizer(serializers.Serializer):
     cart_id = serializers.UUIDField()

     def validate_cart_id(self, cart_id):
          if not Cart.objects.filter(pk=cart_id).exists():
               raise serializers.ValidationError("No cart with the given ID was found")
          if Cartitems.objects.filter(cart_id=cart_id).count() == 0:
               raise serializers.ValidationError("The given cart is empty")
          return cart_id

     def save(self, **kwargs):
        #   Wrapping all the code in transaction so they can be excuted at once to avoid
        # inconsistencies in the cases of a failure
          with transaction.atomic():
            cart_id = self.validated_data['cart_id']
        #   print(self.validated_data['cart_id'])
        #   print(self.context['user_id'])

          (user, created) = User.objects.get_or_create(id=self.context['user_id'])
          order = Order.objects.create(user=user)

          cart_items = Cartitems.objects.select_related('perfume').filter(cart_id=cart_id)

          order_items = [
                OrderItem(
                    order = order,
                    perfume = item.perfume,
                    price = item.perfume.price,
                    quantity = item.quantity
                ) for item in cart_items
          ]

          OrderItem.objects.bulk_create(order_items)

        #   Delete the cart after the order has been placed
          Cart.objects.filter(pk=cart_id).delete()

          return order