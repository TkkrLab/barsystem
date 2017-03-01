from django.template.defaultfilters import floatformat
from django.core.mail import send_mail
from django.conf import settings


def money_display(value):
    if value is None:
        return str(None)
    negative = False
    if value < 0:
        value *= -1
        negative = True
    # Make sure precision is 4 digits, but strip up to 2 trailing zeroes.
    var = floatformat(value, 4)
    if var[-1] == '0':
        var = var[:-1]
    if var[-1] == '0':
        var = var[:-1]
    return '{}{}{}'.format('-' if negative else '', '€ ', var)


EMAIL_OVERDRAWN_SUBJECT = 'Barsystem: {nickname} is over spending limit!'
EMAIL_OVERDRAWN_BODY = """
Dear treasurer,

{nickname} spent {transaction_amount} today.
They currently have a balance of {balance}.
Please tell them they are a bad person.

Thank you,

Your friendly neighbourhood barsystem.

"""


def send_overdrawn_mail(naughty_person, transaction_amount):
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_TARGET:
        # logging.warning('Unable to send email')
        return
    # person_name = '{} ({} {})'.format(naughty_person.nick_name, naughty_person.first_name, naughty_person.last_name)
    values = {
        'nickname': naughty_person.nick_name,
        'transaction_amount': money_display(transaction_amount),
        'balance': money_display(naughty_person.amount),
    }
    subject = EMAIL_OVERDRAWN_SUBJECT.format(**values)
    message = EMAIL_OVERDRAWN_BODY.format(**values)
    send_mail(subject, message, settings.EMAIL_HOST_USER, settings.EMAIL_TARGET, fail_silently=True)
