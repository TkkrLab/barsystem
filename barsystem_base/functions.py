from django.template.defaultfilters import floatformat

def money_display(value):
	if value is None:
		return str(None)
	min_digits = 2
	max_digits = 4
	negative = False
	if value < 0:
		value *= -1
		negative = True
	var = floatformat(value, 4)
	if var[-1] == '0': var = var[:-1]
	if var[-1] == '0': var = var[:-1]
	return '{}{}{}'.format('-' if negative else '', '€ ', var)