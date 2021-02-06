from mail import read_email_from_gmail, send 
from utilities import down, call_pdf, pretty, post
import os
import shutil 
from datetime import date
import pickle
import glob
import time
from multiprocessing import Process

def one_pass(USERNAME, PASSWORD, USER_EMAIL, HASHTAGS):

	admin = 'pyproject101@gmail.com'
	user = USER_EMAIL
	path_main = os.getcwd()

	# if os.path.exists('./Posts'):
	# 	try:
	# 		os.remove('./Posts')
	# 	except:
	# 		shutil.rmtree('./Posts')
	# 	os.mkdir('./Posts')
	# else:
	# 	os.mkdir('./Posts')

	# ---------- GET POSTS FROM IG ----------------- #

	# for hashtag in HASHTAGS:
	# 	os.chdir(path_main)
	# 	down(hashtag)

	os.chdir(path_main)
	if not os.path.exists('./pdf_files'):
		os.mkdir('./pdf_files')

	print('Ready to make pdf')

	sub = f'Money._.Makerz confirmation {date.today()}'
	body = 'Please reply with the post number for tomorrow. Reference the attachment(s)'

	call_pdf(user, body, sub)

	# ------------- AFTER THE POST NUMBER HAS ARRIVED -------------- #
	print('started')
	with open('current_images.pkl', 'rb') as f:
		image_keys = pickle.load(f)

	cont = True

	while cont:
	
		content = read_email_from_gmail(sender = user, subject = sub).split('\n')[0]

		try:
				content = int(content.split('\n')[0].strip())
				print('Post number: ',content)
				if content not in image_keys['key']:
					print("WRONG POST NUMBER")
				else:
					cont = False

		except:
				print('INVALID POST NUMBER \nREPLY AGAIN.')
				time.sleep(10)
		
		

	final_images = []
	os.chdir(path_main)
	imes = os.listdir(os.path.join(os.getcwd(), 'Posts'))

	image_path = image_keys['path'][content-1]

	for x in imes:
		if image_path in str(x) and '.jpg' in str(x):
			final_images.append(x)

	if 'next_post' not in os.listdir(os.getcwd()):
		os.mkdir('next_post')

	for image_root in final_images:
		shutil.copy(os.path.join('./Posts', image_root),'next_post')

	# --- continue from here
	desc = str(open(os.path.join('Posts', image_path + '_UTC' + '.txt'), 'r', encoding = 'utf-8').read())

	new = ''
	for i in desc:
		if ord(i) <= 127 and ord(i) >= 32:
			new += (i)

	f = 'description of the original post: \n' + new + '\n\nReply with the your description.'

	today = date.today()
	sub = f'Money._.Makerz discription {today}'

	send(sub, user, f, False)

	cont = True

	while cont:
		try:
			sub_desc = f'Money._.Makerz discription {date.today()}'
			mail = read_email_from_gmail(sender = user, subject = sub_desc)
			content = ''.join(mail.split('>')[0].split('\n')[:-1]).replace('\r', ' ').replace('  ', '\n')

			if len(content) != 0:
				cont = False
		except:
			pass

	os.chdir('next_post')

	img = []

	for file in glob.glob("*.jpg"):
		img.append(os.path.join(os.getcwd(), file))

	try:
		os.chdir('../')
		shutil.rmtree('./config')
	except:
		pass

	post( USERNAME, PASSWORD, img[0], content)

	shutil.rmtree('./next_post')

def execute():
	users = os.listdir('./accounts')

	for account in users:
		with open(os.path.join('./accounts',account), 'r') as f:
			var = f.read().split('\n')

		USERNAME, PASSWORD, USER_EMAIL, HASHTAGS = var
		HASHTAGS = HASHTAGS.replace(' ', '').split(',')

		SJ = 'follow'
		try:
			content = read_email_from_gmail(sender = USER_EMAIL, subject = SJ).split('\n')[0]
			if content == 'Yes':
				p1 = Process(get_list(HASHTAGS, USERNAME, PASSWORD))
				p2 = Process(one_pass(USERNAME, PASSWORD, USER_EMAIL, HASHTAGS))
				p1.start()
				p2.start()
				p1.join()
				p2.join()
		except:
			one_pass(USERNAME, PASSWORD, USER_EMAIL, HASHTAGS)
# exit()
execute()
