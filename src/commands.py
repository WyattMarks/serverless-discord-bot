from src.discordinteractions import Reply, JSONResponse, DeferReply, InteractionResponseType, finishMessage
import src.database as database
from src.openai import chatCompletion
from src.reddit import getRedditPosts



class Command():
	def __init__(self, name, desc, cb):
		self.name = name
		self.description = desc
		self.handle = cb
	

async def aww(message, event):
	posts = await getRedditPosts('aww')
	return Reply(f'{posts[int(len(posts) * Math.random ())]}')

async def earth(message, event):
	posts = await getRedditPosts('EarthPorn')
	return Reply(f'{posts[int(len(posts) * Math.random ())]}')



async def finish_chat(token, message, id):
	prompt = f"The following is a conversation with Data from Star Trek. Data is being very helpful.\n\nHuman: {message}\nData:"
	reply_text = await chatCompletion(prompt)

	await finishMessage(token, f'> {message}\n\n{reply_text.strip()}')
	await database.save(id, prompt + reply_text + '\nHuman:')

async def chat(message, event):
	token = message['token']
	try:
		id = message['user']['id']
	except:
		id = message['member']['user']['id']
	message = message['data']['options'][0]['value']

	event.waitUntil(finish_chat(token, message, id))
	return DeferReply()



async def reply_chat(token, message, id):
	prompt = await database.get(id)

	if prompt == None:
		f"The following is a conversation with Data from Star Trek. Data is being very helpful.\n\nHuman: {message}\nData:"
	else:
		prompt = f'{prompt} {message}\nData:'

	reply_text = await chatCompletion(prompt)

	await finishMessage(token, f'> {message}\n\n{reply_text.strip()}')
	await database.save(id, prompt + reply_text + '\nHuman')

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
	return JSONResponse({'type': 4, 'data': {'content': url, 'flags': 64}})

async def ping(message, event):
	return Reply(f'Pong!')


AWW_COMMAND = Command("aww", "Get a recent post from /r/aww!", aww)
EARTH_COMMAND = Command("earth", "Get a picture from our home planet!", earth)
INVITE_COMMAND = Command("invite", "Get an invite link for the bot to your server.", invite_link)
PING_COMMAND = Command("ping", "pong", ping)
CHAT_COMMAND = Command("chat", "Chat with me!", chat)
REPLY_COMMAND = Command("reply", "Reply to the conversation!", reply)

GLOBAL_COMMANDS = [AWW_COMMAND, INVITE_COMMAND, PING_COMMAND, EARTH_COMMAND, CHAT_COMMAND, REPLY_COMMAND]