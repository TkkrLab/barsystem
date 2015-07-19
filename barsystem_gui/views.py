from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from barsystem_base.models import Person, Product, Journal

import re
from decimal import Decimal
import json

"""
TODO
cart model:
{
	$product_id: {
		'product_id': $product_id,
		'quantity': $quantity,
		'sender': $sender,
		'recipient': $recipient
	}
}

"""

"""
Flow:
Case: iemand wil iets kopen.
Dat is dan de recipient (de ontvanger van het product).
De sender is standaard "tkkrlab".
Het product gaat dan van sender -> recipient en het bedrag van recipient -> sender.
Als sender "tkkrlab" dan bedrag -> /dev/null
Productvoorraad wordt niet bijgehouden.

Iemand kan ook iets verkopen aan iemand anders.
Dan is de sender een persoon.
Dan gaat product van sender -> recipient, en dan bedrag van recipient -> sender.
"""

class Cart(dict):
	def __init__(self, data=None, person=None):
		if data:
			super().__init__(data)
		self.person = person
		for k in self.keys():
			self[k] = CartItem(self[k])
			self[k].person = self.person

	def js(self):
		return json.dumps(self)

class CartItem(dict):
	def __getattr__(self, key):
		if key in self:
			return self[key]
		raise KeyError

	@property
	def amount(self):
		return self.product.get_price(self.person) * Decimal(self.quantity)

	@property
	def product(self):
		return Product.objects.get(id=self['product_id'])	

	def js(self):
		return json.dumps(self)

def is_bar(request):
	return True
	return request.META.get('REMOTE_ADDR') == '127.0.0.1'

class IndexView(TemplateView):
	template_name = 'barsystem/index.html'

	def post(self, request, *args, **kwargs):
		message = request.POST.get('message')
		m = re.match(r'^i(\d+)b$', message)
		if m:
			button_id = m.groups(1)[0]
			try:
				person = Person.objects.get(active=True, token=button_id)
				request.session['person_id'] = person.id
				if person.special and person.type == 'attendant':
					return HttpResponseRedirect(reverse('people'))
				return HttpResponseRedirect(reverse('products'))
			except Person.DoesNotExist:
				pass
		return HttpResponseRedirect(reverse('index'))

	def get_context_data(self, **kwargs):
		for key in ('person_id', 'cart'):
			if key in self.request.session:
				del self.request.session[key]

		context = super().get_context_data(**kwargs)
		context['wanbetalers'] = Person.objects.filter(amount__lt=0).order_by('amount')[:5]

		context['bar'] = is_bar(self.request)

		return context

class ProductsView(TemplateView):
	template_name = 'barsystem/products.html'

	def post(self, request, *args, **kwargs):
		if request.POST.get('action', None) == 'cancel':
			for key in ('person_id', 'cart'):
				if key in request.session:
					del request.session[key]
			return HttpResponseRedirect(reverse('index'))
		cart = Cart()
		for key, value in request.POST.items():
			m = re.match(r'^products\[(\d+)\]\[quantity\]$', key)
			if m:
				product_id = m.groups(1)[0]
				quantity = value
				cart[product_id] = CartItem(product_id=product_id, quantity=float(quantity), sender=None, recipient=None)
		if len(cart) == 0:
			return HttpResponseRedirect(reverse('products'))
		request.session['cart'] = cart
		return HttpResponseRedirect(reverse('products_confirm'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		person = None
		try:
			person = Person.objects.get(id=self.request.session.get('person_id', None))
		except Person.DoesNotExist:
			pass
		context['person'] = person

		product_list = Product.objects.filter(active=True, special=False)
		paginator = Paginator(product_list, 21**10)

		page = self.request.GET.get('page')
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

		context['products'] = products
		# context['products'] = product_list

		context['special_products'] = Product.objects.filter(active=True, special=True)

		context['cart'] = Cart(self.request.session.get('cart', {}))
		for c in context['cart'].values():
			print(c.js())

		context['bar'] = is_bar(self.request)
		return context

class ProductsGetView(View):
	def post(self, request, *args, **kwargs):
		barcode = request.POST.get('code')
		try:
			product = Product.objects.get(bar_code=barcode)
			return JsonResponse({'product_id': product.id})
		except Product.DoesNotExist:
			return JsonResponse({})
		return JsonResponse({})

class ProductsConfirmView(TemplateView):
	template_name = 'barsystem/products_confirm.html'

	def post(self, request, *args, **kwargs):
		if request.POST.get('action', None) == 'back':
			return HttpResponseRedirect(reverse('products'))

		recipient, balance, balance_limit = self.get_person(request)

		if request.POST.get('action', None) == 'confirm':
			if not self.can_check_out(request):
				return HttpResponseRedirect(reverse('products_confirm'))

			# TEMP DISABLE THIS SHIT
			# return HttpResponseRedirect(reverse('products_confirm'))
			# EOF TEMP
			total = Decimal(0)
			for cart_item in Cart(request.session['cart']).values():
				try:
					product = cart_item.product
					j = Journal()
					j.moment = timezone.now()
					j.sender = cart_item.sender or None #tkkrlab
					j.recipient = cart_item.recipient or recipient
					j.product = product
					j.items = Decimal(cart_item.quantity)
					j.amount = product.get_price(recipient)
					total += j.items * j.amount
					j.save()
				except Product.DoesNotExist:
					pass
			if recipient:
				recipient.amount -= total
				recipient.save()

			for key in ('person_id', 'cart'):
				if key in request.session:
					del request.session[key]

		return HttpResponseRedirect(reverse('index'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		person, balance, balance_limit = self.get_person(self.request)

		context['person'] = person
		context['balance'] = balance
		context['balance_limit'] = balance_limit
		context['cart'] = Cart(self.request.session['cart'], person=person)
		total = Decimal(0)
		for cart_item in context['cart'].values():
			product = cart_item.product
			amount = Decimal(cart_item.quantity) * product.get_price(person)
			total += amount
		context['total'] = total
		context['new_balance'] = balance - total
		context['checkout_permitted'] = self.can_check_out(self.request)
		return context

	def get_person(self, request):
		try:
			person = Person.objects.get(id=request.session.get('person_id', None))
			balance = person.balance
			balance_limit = person.balance_limit
		except Person.DoesNotExist:
			person = None
			balance = Decimal(0)
			balance_limit = None
		return person, balance, balance_limit

	def can_check_out(self, request):
		person, balance, balance_limit = self.get_person(request)
		if balance_limit is None:
			return True
		total = Decimal(0)
		for cart_item in Cart(self.request.session['cart']).values():
			amount = Decimal(cart_item.quantity) * cart_item.product.get_price(person)
			total += amount
		return balance - total >= balance_limit

class PeopleView(TemplateView):
	template_name = 'barsystem/people.html'
	pagination_on = False

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		people_list = Person.objects.filter(active=True)

		context['pagination_on'] = self.pagination_on

		if self.pagination_on:
			paginator = Paginator(people_list, 20)

			page = self.request.GET.get('page')
			try:
				people = paginator.page(page)
			except PageNotAnInteger:
				people = paginator.page(1)
			except EmptyPage:
				people = paginator.page(paginator.num_pages)
		else:
			people = people_list

		context['people'] = people
		return context

class PeopleSetView(View):
	def get(self, request, person_id, *args, **kwargs):
		try:
			person = Person.objects.get(id=person_id)
			request.session['person_id'] = person_id
		except Person.DoesNotExist:
			pass
		return HttpResponseRedirect(reverse('products'))

class AddToCartView(View):
	pass