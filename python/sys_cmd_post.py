#!/usr/bin/python

import json, requests, signal, subprocess, sys
from creds import POST_URL

def main():

	# Exit cleanly on all interrupts
	signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

	# Prompt user for directions
	ans = raw_input("Do you wish to post the output of a system command to #devel_slack-test [y/n]: ")

	if ans == "y" or "yes":
		# Run a system command and save output into variable
		cmd = raw_input("Enter your command: ").split()
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
		text = proc.stdout.read()
	
		url = POST_URL
		data = {'text': text}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}	
		r = requests.post(url, data=json.dumps(data), headers=headers)
		print r.status_code

	else:
		print "Exiting.."
	

if __name__ == "__main__":
	main()
