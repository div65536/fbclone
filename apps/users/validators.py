from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.validators import ASCIIUsernameValidator


def usernameoremailvalidator(value):
	try:
		validate_email(value)
	except ValidationError:
		try:
			ASCIIUsernameValidator(value)
		except ValidationError:
			raise ValidationError("Please enter a valid username or a valid email")
