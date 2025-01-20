import json
import requests
import uuid

import bimcloud

def get_resources(client, criterion={}):
	url = client.url + '/management/client/get-resources-by-criterion'
	response = requests.post(url, headers=client.bearer, params={}, json={**criterion})
	return response.json() if response.ok else None

def get_resource_backup_schedules(client, target_id):
	criterion = {
    	"$eq": { "targetResourceId": target_id }
	}
	url = client.url + '/management/client/get-resource-backup-schedules-by-criterion'
	response = requests.post(url, headers=client.bearer, params={}, json={**criterion})
	return response.json() if response.ok else None

def delete_resource_backup_schedule(client, resource_id):
	schedules = get_resource_backup_schedules(client, resource_id)
	url = client.url + '/management/client/delete-resource-backup-schedule'
	for s in schedules:
		response = requests.delete(url, headers=client.bearer, params={'resource-id': s['id']})
		print (f"Delete: {s['id']} {response}")

def insert_resource_backup_schedule(client, target_id, schedule_id, **parameters ):
	payload = {
        "id": schedule_id,
        "$hidden": parameters.get('hidden', False),
        "$visibility": parameters.get('visibility', 'full'),
        "backupType": parameters.get('backup_type', 'pln'),
        "enabled": parameters.get('enabled', True),
        "targetResourceId": target_id,
        "maxBackupCount": parameters.get('max_backup_count', 1),
        "repeatInterval": parameters.get('repeat_interval', 86400),
        "repeatCount": parameters.get('repeat_count', 1),
        "startTime": parameters.get('start_time', 0),
        "endTime": parameters.get('end_time', 0),
        "type": "resourceBackupSchedule",
        "revision": parameters.get('revision', 0)
	}
	url = client.url + '/management/client/insert-resource-backup-schedule'
	response = requests.post(url, headers=client.bearer, params={}, json={**payload})
	print (f"Insert: {target_id} {response}")

def insert(client, resource_id, **parameters):
	type_ids = {
		'pln': 'plnprojectRoot',
		'bimproject': 'bimprojectprojectRoot',
		'bimlibrary': 'bimprojectlibraryRoot'
	}

	for backup, schedule_id in type_ids.items():
		if resource_id != 'projectRoot':
			value = uuid.uuid4().hex

		insert_resource_backup_schedule(
			cloud,
			target_id = resource_id,
			schedule_id = schedule_id,
			backup_type = backup,
			**parameters
		)

def reset(client, resources=[], formats=[]):
	if not resources:
		resources = get_resources(
			cloud,
			{
				'$and': [
					{'$or': [
						{'$eq': {'type': 'projectRoot'}},
						{'$eq': {'type': 'project'}},
						{'$eq': {'type': 'library'}},
						{'$eq': {'type': 'resourceGroup'}},
						]
					},
					{'$ne': {'$loweredName': 'server root'}},
					{'$ne': {'$loweredName': 'unknown projects'}},
					{'$ne': {'$loweredName': 'unknown libraries'}},
					{'$ne': {'$loweredName': 'backups'}},
				]
			}
		)

	for r in resources:
		query = delete_resource_backup_schedule(client, r['id'])

if __name__ == "__main__":

	param = bimcloud.console.get()
	cloud = bimcloud.client.BIMcloud(**vars(param))

	# mass reset all & insert for root
	reset(cloud, [])
	insert(
		cloud,
		'projectRoot',
		enabled = True,
		max_backup_count = 1,
		repeat_count = 1
	)

