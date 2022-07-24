from django.urls import path
from Home import views
from django.conf import settings
from django.conf.urls.static import static
from .middlewares.auth import  auth_middleware
from .views import  *

urlpatterns = [
    path('', views.home ,name="home"),
    path('productpage', productpage, name='productpage'),
    path('store', store , name='store'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('delete_cart/<int:id>',delete_cart,name='delete_cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('categorie', views.categorie,name="categorie"),
    path('login', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout', views.logout , name='logout'),
    path('edit/<int:id>', views.edit ,name="edit"),
    path('contact', views.contact, name='contact'),
    path("search/", views.SearchView, name="search"),
    path("searchresult/", views.searchresult, name="searchresult"),
    path('blog/', views.showblog, name='blog'),
    path('<int:id>', views.blog_detail, name='blog_detail'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('admindashboard', views.admin_dashboard_view, name='admindashboard'),
    path('view-customer', views.view_customer, name='view-customer'),
    path('view-blog', views.view_blog, name='view-blog'),
    path('blogform', views.blogform, name="blogform"),
    path('edit_blog/<int:p_id>', views.edit_blog,name='edit_blog'),
    path('update_blog/<int:p_id>', views.update_blog,name='update_blog'),
    path('delete_blog/<int:p_id>', views.delete_blog,name='delete_blog'),
    path('productform', views.productform, name="productform"),
    path('view-product', views.view_product, name='view-product'),
    path('view-comment', views.view_comment, name='view-comment'),
    path('view-review', views.view_review, name='view-review'),
    path('edit_product/<int:p_id>', views.edit_product,name='edit_product'),
    path('delete_product/<int:p_id>', views.delete_product,name='delete_product'),
    path('update_product/<int:p_id>', views.update_product,name='update_product'),
    path('delete_customer/<int:p_id>', views.delete_customer,name='delete_customer'),
    path('verify_payment', views.verify_payment, name='verify_payment'),
    path('creator/', views.creator, name='creator'),
    path('logincreator', views.logincreator, name='/logincreator'),
    path('creatordashboard', views.creatordashboard, name='/creatordashboard'),
    path('logoutcreator', views.logoutcreator , name='logoutcreator'),
    path('creatorprofile', views.creatorprofile , name='creatorprofile'),
    path('adminlogin', views.adminlogin , name='adminlogin'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)