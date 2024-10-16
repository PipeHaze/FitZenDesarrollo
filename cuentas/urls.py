from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import (UserLoginForm, PwdResetForm, PwdResetConfirmForm)
from django.views.generic import TemplateView

app_name = 'cuentas'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/cuentas/login/'),name='logout'),
    path('registro/', views.registro_usuarios, name='registro'),
    path('activate/<slug:uidb64>/<slug:token>',views.account_activate, name='activate'),
    #cambio de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/user/password_reset_form.html",
                                                                 success_url='password_reset_email_confirm',
                                                                 email_template_name='account/user/password_reset_email.html',
                                                                 form_class=PwdResetForm), name='recuperaclave'),
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='account/user/password_reset_confirm.html',
                                                                                               success_url='/cuentas/password_reset_complete/', #no se como pero poniendole /cuentas funciono.
                                                                                               form_class=PwdResetConfirmForm), name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/user/reset_status.html"),name='password_reset_done'),
    path('password_reset_complete/',
         TemplateView.as_view(template_name="account/user/reset_status.html"), name='password_reset_complete'),
    #dashboard de usuarios     
    path("dashboard/", views.dashboard, name="dashboard"),
    path("acciones_usuario/", views.acciones_usuario, name="acciones_usuario"),
    path("editar_detalles/", views.editar_detalles, name="editar_detalles"),
    path('perfil/borrar/usuario/',views.borrar_usuarios, name='borrar_usuarios'),
    path('perfil/confirmar_eliminacion/', TemplateView.as_view(template_name="account/user/confirma_eliminacion.html"), name='confirma_eliminacion'),
    path('pedidos_de_tu_usuario/',views.ver_pedidos_usuarios, name="pedidos_del_usuario")
]