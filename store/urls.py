from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('all-products/', views.AllProductsView.as_view(), name="category"),
    path('productdetails/<slug:slug>/', views.ProductDetailsView.as_view(), name="productdetails"),
    path('add-to-cart/<int:pro_id>/', views.AddToCartView.as_view(), name="addtocart"),
    path('view-cart/', views.MyCartView.as_view(), name="viewcart"),
    path('manage-cart/<int:cp_id>/', views.ManageCartView.as_view(), name="managecart"),
    path('empty-cart/', views.EmptyCartView.as_view(), name="emptycart"),
    path('checkout/', views.CheckOutView.as_view(), name="checkout"),
    path('register/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('logout/', views.CustomerLogoutView.as_view(), name="customerlogout"),
    path('login/', views.CustomerLoginView.as_view(), name="customerlogin"),
    path('profile/', views.CustomerProfileView.as_view(), name="customerprofile"),
    path('order-detail/<int:pk>/', views.CustomerOrderDetailsView.as_view(), name="customerorderdetails"),
    path('search/', views.Search.as_view(), name="search"),
    

    
    
    
    
    #Admin 
    path('admin-login/', views.AdminLoginView.as_view(), name="adminlogin"),
    path('admin-home/', views.AdminHomeView.as_view(), name="adminhome"),
    path('admin-orderdetails/<int:pk>/', views.AdminOrderDetailsView.as_view(), name="adminorderdetails"),
    path('admin-all-orders/', views.AdminOrderListView.as_view(), name="adminorderlist"),
    path('adminorderstatuschange/<int:pk>/', views.AdminOrderStatuschangeListView.as_view(), name="adminorderstatuschange"),
    path('admin-product-list/', views.AdminProductListView.as_view(), name="adminoproductlist"),
    path('admin-product-create/', views.AdminProductCreateView.as_view(), name="adminoproductcreate"),
    
    
    
    
]


