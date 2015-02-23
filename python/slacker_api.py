#!/usr/bin/python

'''
This program is a template demonstration of using the slacker
built-in library for python. This program is under development.
-Netuoso

Currently working functions:
-Post chat message to desired channel
-List all files on slack
-Upload files from hard drive to slack
-List all currently created chat rooms
-List all active usernames, their ID and email
-Search all chat messages and get their archive permalink
-Search all files and get their name and download links
'''

import os, requests, signal, sys, time
from slacker import Slacker
from creds import TOKEN

# Assign user based on API credentials created in Slacker dashboard
# Test App - Netuoso - xoxp-2700969653-2751378262-3057670115-99c9f2
slack = Slacker(TOKEN)

print "#" * 50
print "#" * 50
print "Slacker API".rjust(33)
print "-written by Netuoso".rjust(33)
print "#" * 50
print "#" * 50 + "\n"

# Exit cleanly on all interrupts
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

def main():
	ans = raw_input("Please choose an option.\n[chat/users/files/channels/search]: ")
	# Post chat message to given channel
	if ans == "chat":
		channel = raw_input("What channel do you wish to post to?: ")
		if not "#" in channel:
			channel = "#" + channel
		else:
			channel = channel

		message = raw_input("What would you like to post to " + channel + "?: ")
		slack.chat.post_message(channel, message)

	elif ans == "files":
		action = raw_input("What would you like to do? [list/upload]: ")
		if action == "list":
			files = slack.files.list()
			paging_info = files.body['paging']
			files = files.body['files']
			count = paging_info['total']
			print "Displaying %d files: " % count
			time.sleep(1)

			print "#" * 20, "Files", "#" * 20
			for i in files:
				desc = i['name'], i['url'], i['filetype']
				print desc

		elif action == "upload":
			file_dir = raw_input("What is the full location to your file?: ")
			file_exists = os.path.isfile(file_dir)
			if file_exists == True:
				upload = slack.files.upload(file_dir)
				info = upload.body['file']
				desc = info['name'], info['url'], info['filetype']
				print desc
			else:
				print "Could not locate specified file. Exiting.."

	elif ans == "users":
		# Get users list
		users = slack.users.list()
		users = users.body['members']
		for i in users:
			desc = i['profile']
			print i['id'], i['name'], desc['email']

	elif ans == "channels":
		channels = slack.channels.list()
		chat_rooms = channels.body['channels']
		for i in chat_rooms:
			print i['name']

	elif ans == "search":
		action = raw_input("What do you want to search through? [chat/files/both]: ")
		# Procedure for searching the contents of chat
		if action == "chat":
			query = raw_input("Enter search string: ")
			chats = slack.search.messages(query)
			chats = chats.body['messages']
			matches = chats['matches']
			paging_info = chats['paging']
			count = paging_info['total']
			print "Displaying %d messages: " % count
			time.sleep(1)

			print "#" * 20, "Chats", "#" * 20
			for i in matches:
				desc = i['username'] + ":", i['text'], ":", i['permalink']
				print desc
		# Procedure for searching the contents of files
		elif action == "files":
			query = raw_input("Enter search string: ")
			files = slack.search.files(query)
			files = files.body['files']
			matches = files['matches']
			paging_info = files['paging']
			count = paging_info['total']
			print "Displaying %d files: " % count
			time.sleep(1)

			print "#" * 20, "Files", "#" * 20
			for i in matches:
				desc = i['name'], "[" + i["url"] + "]", i["filetype"]
				print desc
		# Procedure for searching the contents of both messages and files
		elif action == "both":
			query = raw_input("Enter search string: ")
			content = slack.search.all(query)
			chats = content.body['messages']
			chat_matches = chats['matches']
			files = content.body['files']
			file_matches = files['matches']
			paging_info_chats = chats['paging']
			paging_info_files = files['paging']
			count_chats = paging_info_chats['total']
			count_files = paging_info_files['total']
			count_total = count_chats + count_files
			print "Displaying %d messages and %d files for a total of %d results." % (count_chats, count_files, count_total)
			time.sleep(1)

			print "#" * 20, "Chats", "#" * 20
			for i in chat_matches:
				desc = i['username'] + ":", i['text'], ":", i['permalink']
				print desc

			print "#" * 20, "Files", "#" * 20
			for i in file_matches:
				desc = i['name'], "[" + i['url'] + "]", i['filetype']
				print desc

		else:
			print "Incorrect option selected. Exiting.."

	else:
		print "Incorrect option selected. Exiting.."

if __name__ == "__main__":
	main()