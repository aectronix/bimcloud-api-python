import json
import requests

import bimcloud

def get_file(client, uri):
	response = requests.post(uri, headers=client.bearer, params={}, json={})
	return response.content

if __name__ == "__main__":

	param = bimcloud.console.get()
	cloud = bimcloud.client.BIMcloud(**vars(param))

	export = get_file(cloud, 'copy_generated_uri')

	with open("save_path_local", "wb") as file:
		file.write(export)