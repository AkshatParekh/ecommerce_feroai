from django.urls import path

from feroai_store.views import CustomerListCreateView, CustomerRetrieveUpdateView, ProductListCreateView, OrderListCreateView, \
    RetrieveUpdateView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:id>/', CustomerRetrieveUpdateView.as_view(), name='customer-retrieve-update'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:id>/', RetrieveUpdateView.as_view(), name='order-retrieve-update'),
]
