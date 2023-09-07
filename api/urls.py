from django.urls import path, include, re_path
from . import views
from pprint import pprint
# Importing router for the modelviewset
# from rest_framework.routers import DefaultRouter
# We now make use of the router that comes nested router, no more the one from restframework above
from rest_framework_nested import routers

# router = DefaultRouter()
# The lines below registers the parent routers
router = routers.DefaultRouter()

router.register(r'profile', views.UserProfileViewSet)
router.register(r'users', views.UserViewSet)
router.register('categories', views.CategoryViewSet) #the name of the endpoint here shouldnt have a forward slash (!categories/)
router.register('perfumes', views.PerfumesViewSet)
router.register('carts', views.CartViewSet)

pprint(router.urls) #Printing the url patterns on the terminal to check whats expectected

# The lines below registers the child routers

# Notice that we pass three arguments which are the parent router (router), the parent
# prefix (perfumes), and the lookup parameter (lookup="perfume")
perfume_router = routers.NestedDefaultRouter(router, "perfumes", lookup="perfume")
perfume_router.register("reviews", views.ReviewViewSet, basename="perfume-reviews")


# cart child router
cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", views.CartItemViewSet, basename="cart-items")

# urlpatterns = router.urls  #Does the same thing as below

urlpatterns = [
    path("", include(router.urls)),
    path("", include(perfume_router.urls)), # Gives access to the perfume child router and the reviews resource
    path("", include(cart_router.urls)),   # Gives access to the cart child
    # path('categories/', views.category_list),
    # path('category_detail/<int:id>/', views.category_detail),
    # path('categories/<str:pk>', views.ApiCategory.as_view())
    
]