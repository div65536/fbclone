from .models import FbUser

class UsernameorEmailBackend:


	def authenticate(self,request,username=None,password=None):
		try:
			user = FbUser.objects.get(email=username)
			if user.check_password(password):
				return user
		except FbUser.DoesNotExist:
			try:
				user = FbUser.objects.get(username=username)
				if user.check_password(password):
					return user
			except FbUser.DoesNotExist:
				return None

	def get_user(self,user_id):
		try:
			return FbUser.objects.get(pk=user_id)
		except FbUser.DoesNotExist:
			return None