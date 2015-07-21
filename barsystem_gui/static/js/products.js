/*$(function(){
	var keywords = [
		'help', 'ok', 'cancel', 'buy'
	];
	var product_names = [];
	var cmd_options = [];
	$.each(keywords, function(k, value)
	{
		cmd_options.push(value + ' ');
	});
	$.each(products, function(id, product)
	{
		product_names.push(product.name.toLowerCase());
		cmd_options.push(product.name.toLowerCase());
	});

	var cmd_help = function()
	{
		$('#help').modal();
	};
	cmd_help.regex = /^help$/;
	var cmd_ok = function()
	{
		$('#cart [value=ok]').click()
	};
	cmd_ok.regex = /^ok$/;
	var cmd_cancel = function()
	{
		$('#cart [value=cancel]').click();
	};
	cmd_cancel.regex = /^cancel$/;
	var cmd_buy = function()
	{

	};
	cmd_buy.regex = [
		/^buy (-?\d*\.?\d+) (.+)$/,
		/^(-?\d*\.?\d+) (.+)$/,
	];
	cmd_buy.args = { 2: product_names }

	// return;

	var command_list = [
		cmd_help, cmd_ok, cmd_cancel, cmd_buy
	];

	console.debug(cmd_options);

	var c = completely($('#cmdline div')[0], 
	{
		promptInnerHTML : '&gt;&nbsp;', 
	});
	c.options = cmd_options;
	c.onChange = function(text)
	{
		if (text.toLowerCase() != text)
		{
			c.hint.value = text.toLowerCase(); // note should be: cly.setText(text);
			c.input.value =text.toLowerCase();
			return;
		}

		var func = null;
		var match = null;

		$.each(command_list, function()
		{
			var cmd = this;
			var type = Object.prototype.toString.call(this.regex);
			if(type == '[object Array]')
			{
				$.each(this.regex, function()
				{
					match = text.match(this);
					if(match)
					{
						func = this;
						return false; // break;
					}
				});
				if(func) return false; // break
			}
			else
			{
				match = text.match(this.regex);
				if(match)
				{
					func = this;
					return false; // break
				}
			}
		});

		var words = text.split(' ');

		if(func)
		{
			console.debug(func);
			console.debug(match);
			if(func.args)
			{

			}
		}

		if(words.length <= 1)
		{
			c.options = cmd_options;
			c.startFrom = 0;
			c.repaint();
			return;
		}
		else if(words.length == 2)
		{
			var quantity = parseFloat(words[0]);
			if(!isNaN(quantity))
			{
				c.options = product_names;
				c.startFrom = words[0].length + 1;
				c.repaint();
				return;
			}
			if(!$.inArray(words[0], keywords))
			{
				c.options = cmd_options;
				c.startFrom = 0;
				c.repaint();
				return;
			}
			c.options = [];
		}
		else if(words.length == 3)
		{
			c.options = product_names;
			c.startFrom = words[0].length + 1 + words[1].length + 1;
			c.repaint();
			return;
		}
		c.repaint();
	}
	c.onEnter = function(e)
	{
		var text = c.getText();
		var r = process_cmdline(text);
		if(r)
		{
			c.setText('');
		}
		console.debug(text);
		console.debug(r);
		e.stopPropagation();
	};
	c.repaint();
	c.input.focus();
	c.hideDropDown();
});
*/
$(function(){

	// $('body').keydown(function()
	// {
	// 	if($('.modal:visible').length == 0)
	// 		$('#cmdline_text').focus();
	// })

	function find_product(search)
	{
		var matches = [];
		$.each(products, function(id, product)
		{
			var name_lower = product.name.toLowerCase();
			if(name_lower.indexOf(search) >= 0)
			{
				matches.push(id);
			}
		});
		return matches;
	}

	function process_cmdline(command)
	{
		var lower = command.toLowerCase();
		switch(lower)
		{
			case 'help':
				cmd_help.call();
				return true;
			case 'ok':
				cmd_ok.call();
				return true;
			case 'cancel':
				cmd_cancel.call();
				return true;
			default:
				var split = lower.split(' ');
				if($.inArray(split[0], keywords) >= 0)
				{

				}
				else
				{
					var products = find_product(lower);
					if(products.length == 1)
					{
						add_cart(products[0], +1);
						return true;
					}
				}
				if(split.length == 1)
				{
					var products = find_product(split[0]);
					if(products.length == 1)
					{
						add_cart(products[0], +1);
						return true;
					}
				}
				else
				{
					var options = {
						'have_quantity': true
					};
					var start = 0;
					if(split[0] == 'buy')
					{
						options['set_quantity'] = true;
						start++;
					}
					var quantity = parseFloat(split[start]);
					if(quantity >= 0)
					{
						var products = find_product(split.slice(start+1).join(' '));
						if(products.length == 1)
						{
							add_cart(products[0], quantity, options);
							return true;
						}
					}
				}

				break;
		}
	}

	// enable actions for clicking on product / cart item
	$('.product').click(function()
	{
		add_cart($(this).data('product-id'), 1);
	});
	$('#cart-items').on('click', '.product', function()
	{
		add_cart($(this).data('product-id'), -1);
	});


	$('#enter-quantity')
		.on('show.bs.modal', function()
		{
			console.debug('show.bs.modal');
			var product_id = $(this).data('product-id');
			var product = products[product_id];
			$(this)
				.find('.input-unit').text(product.unit).end()
				.find('input[name=value]')
					.val(cart[product_id] && cart[product_id].quantity > 0 ? cart[product_id].quantity : '')
					.end();
		})
		.on('shown.bs.modal', function()
		{
			console.debug('shown.bs.modal');
			var product_id = $(this).data('product-id');
			$(this)
				.find('input[name=value]')
					.focus()
					.setCursor(-1)
					.end();
		})
		// .on('hide.bs.modal', function(e)
		// {
		// 	console.debug('hide.bs.modal');
		// })
		.find('button[name=ok]')
			.click(function()
			{
				var input = $('#enter-quantity input[name=value]');
				var product_id = $('#enter-quantity').data('product-id');
				if(!product_id || product_id.length == 0) return;

				var value = parseFloat(input.val());

				if(isNaN(value))
				{
					if(input.val() === '')
						value = 0;
					else
						return false;
				}

				$('[data-product-id=' + product_id + ']').toggleClass('in-cart', value > 0);

				if(value <= 0)
				{
					delete cart[product_id];
				}
				else
				{
					cart[product_id] = {
						'product_id': product_id,
						'quantity': parseFloat(value)
					}
				}

				$('#enter-quantity').modal('hide');
				update_cart();
			})
			.end()
		.keydown(function(e)
		{
			switch(e.which)
			{
				case 13: // ENTER
					$('#enter-quantity button[name=ok]').click();
					break;
			}
		});

	$('#numpad').keyboard({'type': 'numpad'});
	$('#enter-quantity input[name=value]').setValidation('numeric')

	// $('#keyboard .keyboard').keyboard({'type': 'QWERTY', 'output': $('#keyboard input')});
	// $('#keyboard').show();


	// initial cart update
	update_cart(true);
});


function add_cart(product_id, quantity, options)
{
	if(!options) options = {};
	if(!cart[product_id])
	{
		cart[product_id] = {
			'product_id': product_id,
			'quantity': 0
		};
	}

	var product = products[product_id];
	if(options['set_quantity'])
	{
		cart[product_id].quantity = quantity;
	}
	else if(product.quantity_type == 'enter_numeric')
	{
		if(options['have_quantity'])
		{
			cart[product_id].quantity += quantity;
		}
		else
		{
			var eq = $('#enter-quantity')
				.data('product-id', product_id)
				.modal()
			return;
		}
	}
	else
	{
		cart[product_id].quantity += quantity;
	}

	$('[data-product-id=' + product_id + ']').toggleClass('in-cart', cart[product_id].quantity > 0);
	if(cart[product_id].quantity <= 0)
	{
		delete cart[product_id];
	}
	update_cart();
}

function update_cart(init)
{
	var total = 0;
	var template = $('#templateCartItem').html();
	$('#cart-items').empty();
	if(init) $('#products .product').removeClass('in-cart');
	$.each(cart, function(id, cart_item) {
		if(cart_item.quantity == 0) return true; // continue;
		if(init) $('[data-product-id=' + id + ']').addClass('in-cart');
		var product = products[id];
		var price = product.price;
		var item = template.format(
		{
			'id': product.id,
			'name': product.name,
			'quantity': cart_item.quantity,
			'price': money_format(cart_item.quantity * price),
			'unit': product.unit || 'x'
		});
		total += cart_item.quantity * price;
		$('#cart-items').append(item);
		var row = $(item);
		// if(product.quantity_type == 'enter_numeric')
		// {
		// 	$('#cart_product_' + product.id)
		// 		.find('.updown').hide().end()
		// 		.find('.dialog').css('display', 'inline-block').end()
		// }
	});
	$('#cart-total-price').text(money_format(total));
}