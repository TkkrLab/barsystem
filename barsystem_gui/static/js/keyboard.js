// keyboard.js

(function($){

	$.fn.keyboard = function(options)
	{
		var container = this;

		var keyboard = container.find('.keyboard');

		var type = options['type'];
		var output = options['output'];
		if(!output)
		{
			output = container.find('.keyboard-input');
		}
		var has_shift = false;
		var shift_enabled = false;
		var buttons = [];
		var button_map = {};

		if(type == 'numpad')
		{
			buttons = [
				['7', '8', '9', '<-'],
				['4', '5', '6', 'AC'],
				['1', '2', '3'],
				['0', '.', 'clear'],
			]
			keyboard.addClass('numpad');
		}
		else if(type == 'QWERTY')
		{
			has_shift = true;
			buttons = [
				['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[backspace,<-]'],
				['', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
				['', '', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '[ ,space]']
			];
		}
		else if(type == 'qwerty')
		{
			has_shift = true;
			buttons = [
				['1!', '2@', '3#', '4$', '5%', '6^', '7&', '8*', '9(', '0)', '-_', '=+', '[backspace,<-]'],
				['qQ', 'wW', 'eE', 'rR', 'tT', 'yY', 'uU', 'iI', 'oO', 'pP', '[{', ']}', '\\|'],
				['', 'aA', 'sS', 'dD', 'fF', 'gG', 'hH', 'jJ', 'kK', 'lL', ';:', '\'"'],
				['[shift,shift]', 'zZ', 'xX', 'cC', 'vV', 'bB', 'nN', 'mM', ',<', '.>', '/?']
			]
		}

		function button_click()
		{
			var button_id = $(this).val();

			button_id = button_map[button_id];

			if(has_shift)
			{
				if(typeof button_id == 'string' || button_id.length == 2)
				{
					button_id = button_id[shift_enabled ? 1 : 0];
				}
				else if(button_id[0] == '[' && button_id[button_id.length-1] == ']')
				{
					button_id = button_id.substr(1, button_id.length - 2);
					if(button_id.indexOf(',') >= 0)
					{
						button_id = button_id.substr(0, button_id.indexOf(','));
					}
				}
			}

			var type_number = output.attr('type') == 'number';

			var current = output.val();
			if(type_number)
				current = current.toString()

			var new_value = null;
			var append = '';

			if(button_id.match(/^[0-9A-Za-z]$/))
			{
				append = button_id;
			}
			else
			{
				if(button_id == "clear" || button_id == 'AC')
				{
					new_value = '';
				}
				else if(button_id == 'backspace' || button_id == '<-')
				{
					new_value = current.substring(0, current.length - 1);
				}
				else if(button_id == '.')
				{
					if(current.indexOf(button_id) < 0)
					{
						append = button_id;
					}
				}
				else if(has_shift && button_id == 'shift')
				{
					shift_enabled = !shift_enabled;

					$('.keyboard-button', keyboard).each(function()
					{
						var data = $(this).data('button-case');
						if(data)
						{
							$(this).text(data[shift_enabled ? 1 : 0])
						}
					})
				}
				else
				{
					append = button_id;
				}
			}

			if(append.length > 0)
			{
				new_value = current + append;
			}
			if(new_value != null)
			{
				if(type_number)
				{
					new_value = parseFloat(new_value);
				}
				output.val(new_value);
			}

			var maxlength = output.attr('maxlength');
			if(maxlength)
			{
				var current = output.val()
				if(typeof current == 'number')
					current = current.toString();
				if(current.length > maxlength)
					output.val(current.substr(0, maxlength));
			}

			output.focus();
		}

		var button_id = 1;

		$.each(buttons, function(){
			var row = this;
			$.each(row, function(){
				if(this == '')
				{
					var spacer = $('<div>').addClass('spacer');
					keyboard.append(spacer);
					return;
				}
				button_map[button_id] = this;

				var button_val = this;
				var button_text = this;
				var button = $('<button>')
					.addClass('keyboard-button')
					.attr('type', 'button')
					.click(button_click)
					.attr('value', button_id)
					;
				var action = this;
				if(has_shift)
				{
					if(button_val[0] == '[' && button_val[button_val.length-1] == ']')
					{
						if(button_val.indexOf(',') >= 0)
						{
							action2 = button_val.substr(1, button_val.indexOf(',') - 1);
							label = button_val.substring(2 + action2.length, button_val.length - 1);

							button_val = '[' + action2 + ']';
							button_text = label;
						}
						else
						{
							button_text = button_text.substr(1, button_text.length - 2);
						}
					}
					else
					{
						button.data('button-case', [button_text[0], button_text[1]]);
						button_text = button_text[0]
					}
				}
				button
					// .attr('value', button_val)
					.text(button_text);
				keyboard.append(button);

				button_id++;
			})
			keyboard.append('<br />');
		})

		return keyboard;
	}

}(jQuery));
