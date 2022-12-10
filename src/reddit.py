
async def getRedditPosts(sub): # Get hot posts list
	response = await fetch(f'https://www.reddit.com/r/{sub}/hot.json', {
		'headers': {
		'User-Agent': 'data:positronic:v0.0.1',
		},
    })

	data = await response.json()
	posts = []
	
	for i in range(len(data.data.children)):
		try: # Try statements because different post types are formatted differently
			if data.data.children[i]['is_gallery']:
				continue # Galleries don't embed nicely
		except:
			pass

		try: # Video post
			posts.append(data.data.children[i]['data']['secure_media']['reddit_video']['fallback_url'])
			continue
		except:
			pass

		try: # Video post
			posts.append(data.data.children[i]['data']['media']['reddit_video']['fallback_url'])
			continue
		except:
			pass

		try: # Image post
			posts.append(data.data.children[i]['data']['url'])
		except:
			pass

	return posts