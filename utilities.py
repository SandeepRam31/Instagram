import instaloader
import os 
from datetime import date 
import shutil
import glob
import time
from instabot import Bot  
import pickle
from fpdf import FPDF  
from mail import send

# ---------------- DATA FOR THE FOLLOW-FOR-FOLLOW FUNCTIONS ------------------ #
HASHTAGS = ['elonmusk']
path_main = os.getcwd()
username = 'cocoa_3103'
password = '''Enter your password here'''

def follow(user_list, USERNAME, PASSWORD):

	for i in range(int(len(user_list)/10)):
		try:
			user_list_small = user_list[:10]
			user_list = user_list[10:]

			with open(f'./follow/{USERNAME}_followlist.txt', 'w') as f:
				for account in user_list_small:
					f.write(account+'\n')

			print('Starting follow round')

			command = f'python ./instagram-followers-bot/main.py -u {username} -p {password} -o follow-list -t ./follow/{username}_followlist.txt'
			os.system(command)

			time.sleep(3000)
			print('sleeping')
		except:
			break



def get_list(HASHTAGS, USERNAME, PASSWORD):
	L = instaloader.Instaloader()
	L.login(USERNAME, PASSWORD)
	count = 0
	FOLLOW = {}

	for HASH in HASHTAGS:
		posts = instaloader.Hashtag.from_name(L.context, HASH).get_posts()
		for post in posts:
			if post.comments >=1:
				for comment in post.get_comments():
					owner = comment.owner.username
					followers = comment.owner.followers
					followees = comment.owner.followees
					if followers/followees <= 4 and followers>100 and followers<2500:
						print(owner)
						if owner not in list(FOLLOW.keys()):
							FOLLOW[comment.owner.username] = 1/float(followers/followees)
						else:
							FOLLOW[comment.owner.username] += 1/float(followers/followees)
						count += 1
						if count%5 == 0:
							print(count)
						if count%20 == 0:
							FOLLOW = dict(sorted(FOLLOW.items(), key=lambda item: item[1]))
							FOLLOW = list(FOLLOW.keys())
							follow(FOLLOW, USERNAME, PASSWORD)
							FOLLOW = {}



def pdf_sender(imagelist, user, body, subject):
	
	images_sent = []

	pdf = FPDF()
	# imagelist is the list with all image filenames
	count = 1

	for image in imagelist:

		pdf.add_page()
		pdf.set_font('Arial', 'B', 16)
		pdf.cell(30, 10, 'post number {num}'.format(num = count))
		pdf.image(image,50,50,150,150)

		root = image.split('_UTC')[0]
		if root not in images_sent:
			images_sent.append(image.split('_UTC')[0])


		if '_UTC_' not in image:
			count += 1

	key_images = [i+1 for i in range(len(images_sent))]
	dic = {'key': key_images, 'path': images_sent}
	os.chdir(path_main)

	with open('current_images.pkl', 'wb') as f:
		pickle.dump(dic, f)

	path = r"pdf_files\{dat}.pdf".format(dat = date.today())
	pdf.output(path, "F")
	send(SUBJECT = subject, SEND = user, body = body, attachments = True)



def post(username, password , img , discription):
	
	if os.path.exists('config'):
		shutil.rmtree('config')

	bot = Bot()
	bot.login(username = username, password = password)
	bot.upload_photo(img, caption = discription)
	try:
		os.rename(img+'.REMOVE_ME', img)
	except:
		pass



def call_pdf(user, body, subject):
	 
	os.chdir(os.path.join(path_main, 'Posts'))
	image_list = []
	for file in glob.glob('*.jpg'):
		image_list.append(file)
		
	pdf_sender(image_list, user, body, subject)



def pretty():

	os.chdir(path_main)
	source = [os.path.join('Posts', i) for i in os.listdir('Posts')]
	destination = "Posts"

	for s in source:

		if '.' not in s:
			files_list = os.listdir(os.path.join(s))
			for file in files_list:
			    shutil.copy(os.path.join(s, file), 'Posts')
			    try:
			    	os.remove(os.path.join(s, file))
			    except:
			    	pass
			try:
				shutil.rmtree(s)
			except:
				pass

	unwanted = ["*_location.txt", "*.xz", "*.json"]
	os.chdir('Posts')
	for ext in unwanted:
		for file in glob.glob(ext):
			os.remove(file)


			
def down(HASHTAG = '#warrenbuffet'):

	 
	L = instaloader.Instaloader()
	L.login('cocoa_3103', 'voldemort')

	username, likes = [], []

	posts = instaloader.Hashtag.from_name(L.context, HASHTAG).get_posts()
	users = {}

	small_posts = []
	metas = []

	for count, post in enumerate(posts):

		users[post.mediaid] = post.likes + post.comments * 4
		metas.append(post.mediaid)
		small_posts.append(post)

		if count == 5:
			break

	count = 0

	if not os.path.exists('./Posts'):
		os.mkdir('./Posts')	

	os.chdir(os.path.join(path_main, 'Posts'))

	for key, value in users.items():
		post = small_posts[metas.index(key)]
		L.download_post(post, target = HASHTAG)
		count += 1 
		if count == 10:
			break

	os.chdir('../')

	pretty()









