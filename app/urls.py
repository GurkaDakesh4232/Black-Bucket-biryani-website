from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MypasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
from .views import plus_cart
from .views import CheckoutView
from .views import remove_cart,order_success


urlpatterns = [
    path('', views.home),
    path('about/', views.about,name="about"),
    path('contact/', views.contact,name="contact"),
    path("category/<slug:val>", views.category_view.as_view(), name="category"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('address/', views.address,name='address'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(),name='updateAddress'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    
    

    path('pluscart/', plus_cart, name='plus-cart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/',remove_cart, name='remove-cart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('order_success/', order_success, name='order_success'),
    path('', views.home, name='home'),  # Add name='home' to the path





    


    #login authentication
path('registration/', views.customerregistrationView.as_view(), name='customerregistration'),
path('accounts/login/',auth_views.LoginView.as_view(template_name='testapp/login.html', 
         authentication_form=LoginForm),name='login'), 
        
    
path('passwordchange/', 
     auth_views.PasswordChangeView.as_view(
         template_name='testapp/changepassword.html',
         form_class=MyPasswordChangeForm,
         success_url='/passwordchangedone/'),  # Note the fixed success_url parameter
     name='passwordchange'),

path('passwordchangedone/', 
     auth_views.PasswordChangeDoneView.as_view(
         template_name='testapp/passwordchangedone.html'), 
     name='passwordchangedone'),

    # Other URL patterns
path('logout/', 
         auth_views.LogoutView.as_view(next_page='login'), 
         name='logout'),
             


             # Password reset view (with custom form)
path('password-reset/', 
     auth_views.PasswordResetView.as_view(
         template_name='testapp/password_reset.html'),
     name='password_reset'),

# Password reset done view (no form_class, just a template)
path('password-reset/done/', 
     auth_views.PasswordResetDoneView.as_view(
         template_name='testapp/password_reset_done.html'),
     name='password_reset_done'),

# Password reset confirm view (with custom set password form)
path('password-reset-confirm/<uidb64>/<token>/', 
     auth_views.PasswordResetConfirmView.as_view(
         template_name='testapp/password_reset_confirm.html',
         form_class=MySetPasswordForm),
     name='password_reset_confirm'),

# Password reset complete view (no form_class, just a template)
path('password-reset-complete/', 
     auth_views.PasswordResetCompleteView.as_view(
         template_name='testapp/password_reset_complete.html'),
     name='password_reset_complete'),

 path('order_success/', order_success, name='order_success'),            
         
         


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
