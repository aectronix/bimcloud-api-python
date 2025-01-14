import json
import requests

class BIMcloud():

	def __init__(self, manager: str, client: str, user: str, password: str):

		self.url = manager
		self.client = client
		self.user = user
		self.password = password
		self.auth = self.auth() or None
		self.bearer = {'Authorization': f"Bearer {self.auth['access_token']}"}

	def auth(self):
		url = self.url+'/management/client/oauth2/token'
		request = {
			'grant_type': 'password',
			'username': self.user,
			'password': self.password,
			'client_id': self.client
		}
		try:
			response = requests.post(url, data=request, headers={'Content-Type': 'application/x-www-form-urlencoded'})
			response.raise_for_status()
			return response.json() if json else response.content
		except:
			raise