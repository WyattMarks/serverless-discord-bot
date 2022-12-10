from src.discordinteractions import InteractionType, InteractionResponseType, TextResponse, JSONResponse, Reply, verifyKey
from src.commands import GLOBAL_COMMANDS

async def handleRequest(event):
	request = event.request
	
	# Discord always sends a POST with json in the payload
	if request.method == "POST":
		# Discord requires you to correctly verify the key, they apparently will send 
		# packets with an incorrect signature to catch you. They definitely do when you change the endpoint.
		if not await verifyKey(request):
			return TextResponse('Incorect Signature!', {'status': 401})

		message = await request.json()

		# Ping is only used when changing the endpoint
		if message['type'] == InteractionType.PING:
			return JSONResponse({'type': InteractionResponseType.PONG})

		# All commands come through as this
		if message['type'] == InteractionType.APPLICATION_COMMAND:
			for i in range(len(GLOBAL_COMMANDS)):
				cmd = GLOBAL_COMMANDS[i]
				if message.data['name'] == cmd.name:
					return cmd.handle(message, event)
				

			return Reply('Sorry, not implemented yet!')

			
		else:
			# Some unimplemented message type
			print(f'Unknown Type {message.type}')
			return JSONResponse({ 'error': f'Unknown Type {message.type}' }, {'status': 400})
	else:
		# Must be someone manually visiting the endpoint
		return TextResponse('Hello from Data!')

addEventListener('fetch', (lambda event: event.respondWith(handleRequest(event))))