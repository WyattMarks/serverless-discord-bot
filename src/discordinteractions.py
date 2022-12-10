class InteractionType:
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

class InteractionResponseType:
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE =  7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9

class InteractionResponseFlags:
    EPHEMERAL = 1 << 6

# For GETs or other plaintext responses
def TextResponse(body, init={}):
	init['headers'] = {
        'content-type': 'text/plain;charset=UTF-8',
	  }
	return __new__(Response(body, init))

# JSON encoded response
def JSONResponse(body, init={}):
	init['headers'] = {
        'content-type': 'application/json;charset=UTF-8',
	  }
	return __new__(Response(JSON.stringify(body), init))

# Return a response formatted to reply in the discord channel
def Reply(message):
	return JSONResponse({'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE, 'data': {'content': message}})

# Return a response formatted to reply in the discord channel
def DeferReply():
	return JSONResponse({'type': InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE, 'data': {'content': ''}})

# Use the javascript library discord-interactions to verify the response
async def verifyKey(request):
    verify = require('discord-interactions').verifyKey
    
    try:
        signature = request.headers.js_get('X-Signature-Ed25519')
        timestamp = request.headers.js_get('X-Signature-Timestamp')
        body = await request.clone().arrayBuffer()

        return verify(body, signature, timestamp, DISCORD_PUB_KEY)
    except:
        return False

async def finishMessage(token, text):
    head = {
        'content-type': 'application/json',
	  }
    response = await fetch(f'https://discord.com/api/webhooks/{DISCORD_APP_ID}/{token}/messages/@original', {'method': 'PATCH', 'headers': head, 'body': JSON.stringify({'type': InteractionResponseType.UPDATE_MESSAGE, 'content': text})})
    return await response.json()