user = "dawson_scraper"
pwd = "dawsonscrapes123"
CLIENT_ID = "81Lszn_qxI8t4gitDsB5hA"
SECRET_KEY = "KZXLffRmt_pOnZoisA8pLzE4r3zegQ"
import requests
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
    'grant_type': 'password',
    'username': user,
    'password': pwd
}
headers ={'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

res = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers) # <Response 200> expected
res2 = requests.get('https://oauth.reddit.com/r/dawson/search/?restrict_sr=dawson&q=computer science', headers=headers) # Response 200 but shows html
cs_posts =[]

for i in res2.json()['data']['children']:
    post = {'title': i['data']['title'], 'ups': i['data']['ups'], 'body': i['data']['selftext_html']}
    cs_posts.append(post)
# sorting most popular posts
sorted_cs_posts = sorted(cs_posts, key=lambda value: value['ups'], reverse=True)
for i in sorted_cs_posts:
    print(i)

