import json
import requests

import bimcloud

def get_resource_backup_schedules(client, target_id):
	criterion = {
    	"$eq": { "targetResourceId": target_id }
	}
	url = client.url + '/management/client/get-resource-backup-schedules-by-criterion'
	response = requests.post(url, headers=client.bearer, params={}, json={**criterion})
	return response.json() if response.ok else None

def update_resource_backup_schedule(client, target_id):
	payload = {
        "id": "bimprojectprojectRoot",
        "$hidden": False,
        "$visibility": "full",
        "backupType": "bimproject",
        "enabled": True,
        "targetResourceId": target_id,
        "maxBackupCount": 7,
        "repeatInterval": 14400,
        "repeatCount": 0,
        "startTime": 0,
        "endTime": 0,
        "type": "resourceBackupSchedule",
        "revision": 0
	}
	url = client.url + '/management/client/update-resource-backup-schedule'
	response = requests.put(url, headers=client.bearer, params={}, json={**payload})
	return response

if __name__ == "__main__":

	param = bimcloud.console.get()
	cloud = bimcloud.client.BIMcloud(**vars(param))

	# schedules = get_resource_backup_schedules(cloud, '3DC3CD2A-3BE1-47A8-930E-093C60C1E871')
	upd = update_resource_backup_schedule(cloud, '74db6a15-a64e-4f81-836f-2c58499b48da')
	print (upd)
	# print(json.dumps(schedules, indent = 4))

