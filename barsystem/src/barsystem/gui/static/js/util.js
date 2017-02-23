String.prototype.format = function() {
	var args = arguments[0];
	return this.replace(/{([A-Za-z0-9_\\-]+)}/g, function(match, number)
	{
		return typeof args[number] != 'undefined'
		? args[number]
		: match
		;
	});
};

function round(val, max)
{
	var multiplier = Math.pow(10, max);
	return Math.round(val * multiplier) / multiplier;
}

var currency = {
	"prefix": "€",
	"postfix": "",
};

function float_to_string(val) {
	var result = val.toFixed(2);
	var full = val + '';
	if(full.length > result.length)
	{
		result = round(val, 4) + '';
	}

	return result.replace(/\./, ',');
}

function money_format(val)
{
	var negative = false;
	if(val < 0)
	{
		val *= -1;
		negative = true;
	}
	var str = currency.prefix + float_to_string(val) + currency.postfix;
	if(negative) str = '-' + str;
	return str;
}

(function($) {
	$.fn.setCursor = function(position)
	{
		if(position < 0)
		{
			position = this.val().length + 1 + position;
		}
		this[0].selectionStart = position;
		return this;
	};
}(jQuery));

(function($) {
	function numeric_validate(evt)
	{
		var self = $(evt.delegateTarget);

		// ignore keys with modifiers
		if(evt.metaKey || evt.shiftKey || evt.ctrlKey || evt.altKey) return;

		var prevent = true;
		if(evt.key.match(/^[0-9]$/) || evt.key.length > 1)
		{
			prevent = false;
		}

		if(evt.key.match(/^[\.,]$/))
		{
			if(self.val().indexOf('.') < 0)
			{
				if(evt.key == ',')
				{
					prevent = true;
					self.val(self.val()+'.');
				}
				else
				{
					prevent = false;
				}
			}
		}

		if(prevent)
		{
			evt.preventDefault();
		}
	}

	$.fn.setValidation = function(type)
	{
		var self = this;
		if(type == 'numeric')
		{
			this.keypress(numeric_validate);
		}
		return self;
	};
}(jQuery));

var Barlink = (function(){
	var socket = null;
	var connect_errors = 0;

	function Barlink(options)
	{
		this.options = options;

		this.socket = null;
		this.connect_errors = 0;

		var self = this;

		this.connect = function()
		{
			socket = new WebSocket('ws://localhost:1234/ws/' + self.options.path);
			socket.onopen = function(evt)
			{
				self.connect_errors = 0;
				$('#connection').removeClass('fail').addClass('ok');
				if(self.options.onopen)
				{
					self.options.onopen(evt);
				}
			}
			socket.onclose = function(evt)
			{
				$('#connection').removeClass('ok').addClass('fail');
				self.connect_errors++;
				if(self.connect_errors < 5)
				{
					setTimeout(self.reconnect, 1000);
				}
				if(self.options.onclose)
				{
					self.options.onclose(evt);
				}
			}
			socket.onmessage = function(evt)
			{
				if(self.options.onmessage)
				{
					self.options.onmessage(evt.data)
				}
			}
			socket.onerror = function(evt)
			{
				if(self.options.onerror)
				{
					self.options.onerror(evt);
				}
			}
		}
		this.reconnect = function()
		{
			self.connect();
		}
		this.send = function(data)
		{
			if(socket)
			{
				socket.send(JSON.stringify(data))
			}
		}
		this.close = function()
		{
			if(socket)
			{
				socket.close()
			}
		}
	}

	return Barlink;
})();