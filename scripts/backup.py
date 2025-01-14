import requests
import bimcloud

def get_resources(client, criterion={}):
	url = client.url + '/management/client/get-resources-by-criterion'
	response = requests.post(url, headers=client.bearer, params={}, json={**criterion})
	return response.json() if response.ok else None

if __name__ == "__main__":

	param = bimcloud.console.get()
	cloud = bimcloud.client.BIMcloud(**vars(param))

	projects = get_resources(cloud)
	print (projects)

