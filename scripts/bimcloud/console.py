import argparse

def get():
	cmd = argparse.ArgumentParser()
	cmd.add_argument('-m', '--manager', required=True, help='URL of the BIMcloud Manager')
	cmd.add_argument('-c', '--client', required=False, help='Client Identification')
	cmd.add_argument('-u', '--user', required=False, help='User Login')
	cmd.add_argument('-p', '--password', required=False, help='User Password')
	return cmd.parse_args()