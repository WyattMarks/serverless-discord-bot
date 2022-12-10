async def chatCompletion(prompt):
	headers = {'User-Agent': 'data:positronic:0.0.1', 'content-type': 'application/json', 'Authorization': f'Bearer {OPENAI_KEY}'}

	response = await fetch(f'https://api.openai.com/v1/completions', {'method': 'POST', 'headers': headers, 'body': JSON.stringify({
		'model': "text-davinci-003",
		'prompt': prompt,
		'temperature': 0.9,
		'max_tokens': 150,
		'top_p': 1,
		'frequency_penalty': 0,
		'presence_penalty': 0.6,
		'stop': ["Human:"],
	})})
	reply = await response.json()
	return reply['choices'][0]['text']
