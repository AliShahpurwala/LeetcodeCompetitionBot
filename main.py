from discord.ext import commands
import uuid
import os
import json
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gClient = gspread.authorize(credentials)
sheet = gClient.open("Hacktober Leetcode Points").get_worksheet(1)


API_KEY = ''
ENDPOINT = 'https://eastus.api.cognitive.microsoft.com/vision/v1.0/ocr'
DIR = '.'


def handler():
    text = []
    pathToImage = './image.jpg'
    results = get_text(pathToImage)
    text = parse_text(results)
    return text

def parse_text(results):
    text = []
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text.append(word['text'])
    return text  

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': 'en',
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results


def awardPoints(authorName, challengeNumber):
	try:
		sheetRow = sheet.find(authorName).row
	except:
		print("Unable to locate said author")
		return 0


	try:
		sheetCol = sheet.find("Challenge " + str(challengeNumber)).col
	except:
		print("Unable to locate said challenge")
		return -1
	
	sheet.update_cell(int(sheetRow), int(sheetCol), 1)
	return 1


client = commands.Bot(command_prefix="-")





@client.event
async def on_ready():
	print("Bot is now live!")




@client.command()
async def leetCodeSubmission(context):
	try:
		challengeNum = int(context.message.content.split(' ')[1])
	except:
		await context.send("I couldn't find a valid question number. Could you try that again please?")
		return None
	try:
		url = context.message.attachments[0].url
	except:
		print("No image found")
		await context.send("Have you attached an image? I can't seem to find one")
	else:
		await context.message.attachments[0].save('image.jpg')
		await context.send("Hey! We got your image, this will just take a minute :)")
		imageText = handler()
		submissionAuthor = context.message.author.name
		if 'Success' in imageText:
			responseCode = awardPoints(submissionAuthor, challengeNum)
			if responseCode == 0:
				await context.send("I couldn't find your username in the database. Could you contact one of the moderators?")
			elif responseCode == -1:
				await context.send("You haven't entered a valid question number :(")
			elif responseCode == 1:
				await context.send("Woohoo! Your submission has been accepted and you've been awarded a point!") 
		else:
			await context.send("Hmm you didn't seem to get this one :(")
		# await context.send(imageText)
		os.system("rm image.jpg")






client.run('')