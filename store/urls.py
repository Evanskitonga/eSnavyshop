# from django.urls import path
# from .views import (
#     RegisterView, UserView,
#     ProductListView, ProductDetailView,
#     CreateOrderView, UserOrdersView
# )

# urlpatterns = [
#     path('register/', RegisterView.as_view()),
#     path('user/', UserView.as_view()),
#     path('products/', ProductListView.as_view()),
#     path('products/<int:pk>/', ProductDetailView.as_view()),
#     path('orders/', CreateOrderView.as_view()),
#     path('my-orders/', UserOrdersView.as_view()),
# ]


from django.urls import path
from .views import place_order
from django.conf import settings
from django.conf.urls.static import static


from .views import (
    RegisterView, LoginView, UserView,
    ProductListView, ProductDetailView,
    CreateOrderView, UserOrdersView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),           # ✅ Add this line
    path('user/', UserView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('orders/', CreateOrderView.as_view()),
    path('my-orders/', UserOrdersView.as_view()),
    path('orders/', place_order),
    path('api/place-order/', place_order),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
