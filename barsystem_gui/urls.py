from django.conf.urls import patterns, include, url

from barsystem_gui import views

urlpatterns = [
	url(r'^people/$', views.PeopleView.as_view(), name='people'),
	url(r'^people/set/(?P<person_id>\d+)/$', views.PeopleSetView.as_view(), name='people_set'),
	url(r'^cart/add/', views.AddToCartView.as_view(), name='add_to_cart'),
	url(r'^products/$', views.ProductsView.as_view(), name='products'),
	url(r'^products/get/$', views.ProductsGetView.as_view(), name='products_get'),
	url(r'^products/confirm/$', views.ProductsConfirmView.as_view(), name='products_confirm'),
	url(r'^create_account/$', views.CreateAccountView.as_view(), name='create_account'),
	url(r'^delete_account/$', views.DeleteAccountView.as_view(), name='delete_account'),
	url(r'^$', views.IndexView.as_view(), name='index'),
]