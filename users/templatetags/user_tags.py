from django import template

from allauth.account.admin import EmailAddress

register = template.Library()

#@register.filter("user_email_verify")
@register.inclusion_tag('users/include/tag/user_email_verify.html')
def user_email_verify(value):
    
	result = EmailAddress.objects.filter(user=value, verified=True).exists()
    
	return { 'result' : result }
