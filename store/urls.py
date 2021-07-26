from django.urls import path

from store import views


app_name = 'store'

urlpatterns = [
    # path('', views.index, name='index'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.sign_in, name='connexion'),
    path('deconnexion/', views.sign_out, name='sign_out'),

    path('my-order/', views.my_order_view, name='my_order'),
    path('my-profile/', views.my_profile_view, name='my-profile'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('order-details/<int:commande_id>/', views.my_order_view_detail, name='order-details'),

    path('about/', views.about, name='about'),
    path('boutique/<int:category_id>/', views.boutique, name='boutique'),
    path('detail/<int:product_id>/', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),

    path('add-to-cart/<int:product_id>/<int:qty>/', views.add_to_cart, name='add_to_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('clear-item-cart/<str:product_id>', views.clear_item_cart, name='clear_item_cart'),
    path('cart/', views.display_cart, name='display_cart'),

    path('shipping/', views.shipping, name='shipping'),
    # path('add-address/', views.add_address, name='add_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confirmation, name='confirmation'),
    # path('cart/', views.cart, name='cart'),
    # path('mon-compte/', views.compte, name='compte'),
    # path('paiement/', views.paiement, name='paiement'),
]
