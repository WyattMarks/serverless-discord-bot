


async def save(id, value):
	url = f'{UPSTASH_REDIS_URL}/set/{id}/{encodeURIComponent(value)}?_token={UPSTASH_REDIS_TOKEN}' # Save the conversation history
	response = await fetch(url)

	url = f'{UPSTASH_REDIS_URL}/expire/{id}/600?_token={UPSTASH_REDIS_TOKEN}' # Set the expiration time to 600s 
	response = await fetch(url)
	return await response.json()

async def get(id):
	url = f'{UPSTASH_REDIS_URL}/get/{id}?_token={UPSTASH_REDIS_TOKEN}'
	response = await fetch(url)
	value = await response.json()
	return value['result']

async def append(id, value):
	url = f'{UPSTASH_REDIS_URL}/append/{id}/{encodeURIComponent(value)}?_token={UPSTASH_REDIS_TOKEN}' # append
	return await fetch(url)