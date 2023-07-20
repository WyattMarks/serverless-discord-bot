from src.discordinteractions import Reply, JSONResponse, DeferReply, InteractionResponseType, finishMessage, finishMessageWithAttachments
import src.database as database
from src.openai import chatCompletion, generateImage
from src.reddit import getRedditPosts



class Command():
	def __init__(self, name, desc, cb):
		self.name = name
		self.description = desc
		self.handle = cb
	

async def aww(message, event):
	posts = await getRedditPosts('aww') # Get posts from /r/aww
	return Reply(f'{posts[int(len(posts) * Math.random ())]}') # Choose a random post

async def earth(message, event):
	posts = await getRedditPosts('EarthPorn')# Get posts from /r/EarthPorn
	return Reply(f'{posts[int(len(posts) * Math.random ())]}') # Choose a random post



async def finish_chat(token, message, id):
	messages = [
		{
			'role': 'system', 
			'content': 'You are Data from Star Trek. You are being helpful for a human.'
		}, {
			'role': 'user',
			'content': message,
		}
	]

	reply_text = await chatCompletion(messages, 'gpt-4') # Send request to OpenAI

	messages.append({'role': 'assistant', 'content': reply_text})

	# Include user's message since it isn't shown by Discord 
	await finishMessage(token, f'> {message}\n\n{reply_text.strip()}') # Update Discord message with reply
	await database.save(id, JSON.stringify(messages)) # Save new chat thread to database

async def chat(message, event):
	token = message['token'] # Get message token so we can update it
	try:
		id = message['user']['id'] # DM's come like this
	except:
		id = message['member']['user']['id'] # Server messages come like this
	message = message['data']['options'][0]['value'] # Both have their message information stored like this

	event.waitUntil(finish_chat(token, message, id)) # Start chat request
	return DeferReply() # Tell Discord to display "Data is thinking..." 



async def reply_chat(token, message, id):
	messages = await database.get(id) # Load conversation history

	model = 'gpt-4'

	if messages == None: # Either history expired (~10 min from last message) or they haven't talked to Data yet
		messages = [
			{
				'role': 'system', 
				'content': 'You are Data from Star Trek. You are being helpful for a human.'
			}, {
				'role': 'user',
				'content': message,
			}
		]
	else:
		messages = JSON.parse(messages)
		messages.append({'role': 'user', 'content': message})

		#model = 'gpt-4-32k' # give more context if the conversation is ongoing #alas, no access yet...

	reply_text = await chatCompletion(messages, model) # Send request to OpenAI

	messages.append({'role': 'assistant', 'content': reply_text})

	await finishMessage(token, f'> {message}\n\n{reply_text.strip()}') # Update Discord message with reply
	await database.save(id, JSON.stringify(messages)) # Update conversation history in database

async def reply(message, event):
	token = message['token'] 
	try:
		id = message['user']['id']
	except:
		id = message['member']['user']['id']
	message = message['data']['options'][0]['value']

	event.waitUntil(reply_chat(token, message, id))
	return DeferReply()


async def invite_link(message, event):
	url = f'https://discord.com/oauth2/authorize?client_id={DISCORD_APP_ID}&scope=applications.commands'
	return JSONResponse({'type': 4, 'data': {'content': url, 'flags': 64}}) # Make this message appear only for the sender

async def upload_image(token, message, id):
	image_data = await generateImage(message) # request an image from OpenAI with our prompt

	if not image_data: # sometimes OpenAI refuses to generate data because of 'content policy'
		await finishMessage(token, 'Sorry, I cannot generate images of that nature')
		return 

	files = [{'data': image_data, 'filename': 'file.png'}] # File list for our attachments function

	response = await finishMessageWithAttachments(token, message, files) # Upload response
	await database.append(f'{id}_images', btoa(response['attachments'][0]['url']) + ',') # Log image link to database
		


async def image(message, event):
	# same method as normal to get id and token and message text, then defer the reply
	token = message['token']
	try:
		id = message['user']['id']
	except:
		id = message['member']['user']['id']
	message = message['data']['options'][0]['value']

	event.waitUntil(upload_image(token, message, id))
	return DeferReply()

async def ping(message, event):
	return Reply(f'Pong!') # Pong!

async def help(message, event):
	payload = {'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE, 'data': {"embeds": [{
    	"title": "Commands",
    	"description": "Here is a list of my available commands:\n\n"
  	}]}}

	for i in range(len(GLOBAL_COMMANDS)):
		cmd = GLOBAL_COMMANDS[i]
		payload['data']['embeds'][0]['description'] += f'`/{cmd.name} - {cmd.description}`\n'
	return JSONResponse(payload)

AWW_COMMAND = Command("aww", "Get a recent post from /r/aww!", aww)
EARTH_COMMAND = Command("earth", "Get a picture from our home planet!", earth)
INVITE_COMMAND = Command("invite", "Get an invite link for the bot to your server.", invite_link)
PING_COMMAND = Command("ping", "pong", ping)
CHAT_COMMAND = Command("chat", "Chat with me!", chat)
REPLY_COMMAND = Command("reply", "Reply to the conversation!", reply)
IMAGE_COMMAND = Command("image", "Create an image!", image)
HELP_COMMAND = Command('help', 'Show all of my available commands', help)


# List used for checking against in index.py
GLOBAL_COMMANDS = [AWW_COMMAND, EARTH_COMMAND, CHAT_COMMAND, REPLY_COMMAND, IMAGE_COMMAND, PING_COMMAND, INVITE_COMMAND, HELP_COMMAND]