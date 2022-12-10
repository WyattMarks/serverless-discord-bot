
async def getRedditPosts(sub):
	response = await fetch(f'https://www.reddit.com/r/{sub}/hot.json', {
		'headers': {
		'User-Agent': 'data:positronic:v0.0.1',
		},
    })

	data = await response.json()
	posts = []
	
	for i in range(len(data.data.children)):
		try:
			if data.data.children[i]['is_gallery']:
				continue
		except:
			pass

		try:
			posts.append(data.data.children[i]['data']['secure_media']['reddit_video']['fallback_url'])
			continue
		except:
			pass

		try: 
			posts.append(data.data.children[i]['data']['media']['reddit_video']['fallback_url'])
			continue
		except:
			pass

		try:
			posts.append(data.data.children[i]['data']['url'])
		except:
			pass

	return posts