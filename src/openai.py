async def chatCompletion(prompt):
	headers = {'User-Agent': 'data:positronic:0.0.1', 'content-type': 'application/json', 'Authorization': f'Bearer {OPENAI_KEY}'}

	response = await fetch(f'https://api.openai.com/v1/completions', {'method': 'POST', 'headers': headers, 'body': JSON.stringify({
		'model': "text-davinci-003", # Best model
		'prompt': prompt, # Give it the prompt
		'temperature': 0.9, # Hightly random, more realisticly human
		'max_tokens': 300,
		'top_p': 1,
		'frequency_penalty': 0,
		'presence_penalty': 0.6,
		'stop': ["Human:"], # When it's the user's turn to speak
	})})
	reply = await response.json()
	return reply['choices'][0]['text']

async def generateImage(prompt):
	headers = {'User-Agent': 'data:positronic:0.0.1', 'content-type': 'application/json', 'Authorization': f'Bearer {OPENAI_KEY}'}

	response = await fetch(f'https://api.openai.com/v1/images/generations', {'method': 'POST', 'headers': headers, 'body': JSON.stringify({
		"prompt": prompt,
		"n": 1,
		"size": "1024x1024", # Might as well get best size, it's a $0.004 difference in 256x256 and 1024x1024
		'response_format': 'b64_json' # We want b64 image instead of URL since the OpenAI URL's expire in an hour
	})})							  # AFAIK Discord media doesn't expire at all
	reply = await response.json()
	
	# Try statement since sometimes the data isn't populated because refusal to generate, return False and just assume it's the content policy
	try:
		base64_image = reply['data'][0]['b64_json']
		decoded_image = atob(base64_image) # decoded image data in string format
		image_data = __new__(Uint8Array(len(decoded_image)))
		for i in range(len(decoded_image)):
			image_data[i] = ord(decoded_image[i]) # actual binary data array generation
		return image_data
	except:
		return False