SERVER_LIST = [1, 2, 3, 4, 5]

import os
import subprocess
command = 'echo $PREFIX | grep -o "com.termux"'
if os.name == 'nt': M = False
else:
	try: M = False if 'termux' in subprocess.check_output(command, shell=True, text=True) else True
	except: M = True

try:
	from qhit import *
except:
	print("! Couldn't import qhit")
	print("- Installing...")
	try:
		import requests
	except:
		print("! Couldn't import requests")
		print("- Installing...")
		os.system('pip install requests --user')
		print('Done. Please Re-Run [0/3]')
		exit()
	exec(requests.get('https://qwk.pythonanywhere.com/hit/install').json()['code'])
	print('Done. Please Re-Run [1/3]')
	exit()

cfg = {
	'main': {
		'name': 'sc' if M else '',
		'img': None if M else img('nuke-cloud-small')
	},
	'names': {
		'Achieve': 'XA',
		'Blooket': 'XB',
		'Server': 'XS'
	},
	'ctxt': 'Made by qwk',
	'font': 9,
	'columns': 2,
	'mg': 'rainbow',
	'border': "—|,,''" if M else '─│╭╮╰╯',
	'clr': (255, 0, 0),
	'cg': [(255, 0, 0), (255, 150, 150)],
	'fg': [(0, 0, 255), (120, 0, 255)],
	'ig': [(0, 0, 255), (120, 0, 255)],
	'ic': (255, 255, 255),
	'oc': 'w',
	'ogc': 'g',
	'obc': 'r',
	'gtclr': 'rainbow',
	'table': M
}
gt = {
	'd': [(110, 110, 110), (160, 160, 160), (110, 110, 110)],
	'w': [(180, 180, 180), (255, 255, 255), (180, 180, 180)],
	'r': [(255,   0,  50), (255, 120,   0), (255,   0,  50)],
	'o': [(255, 130,   0), (255, 180,   0), (255, 130,   0)],
	'y': [(255, 200,   0), (255, 255,   0), (255, 200,   0)],
	'g': [(  0, 255,   0), (  0, 255, 180), (  0, 255,   0)],
	'c': [(  0, 255, 255), (170, 255, 255), (  0, 255, 255)],
	'b': [(  0,  50, 255), (  0, 150, 255), (  0,  50, 255)],
	'p': [(100,  50, 255), (140,  70, 255), (100,  50, 255)],
	'm': [(255,   0, 255), (255, 150, 255), (255,   0, 255)]
}
x = False
try:
	from bs4 import BeautifulSoup
except:
	print(gradient("! Couldn't import bs4", text_clr=gt[cfg['obc']], use_table=cfg['table']))
	print(gradient("- Installing...", text_clr=gt[cfg['oc']], use_table=cfg['table']))
	os.system('pip install beautifulsoup4 --user')
	x = True
try:
	import websockets
except:
	print(gradient("! Couldn't import websockets", text_clr=gt[cfg['obc']], use_table=cfg['table']))
	print(gradient("- Installing...", text_clr=gt[cfg['oc']], use_table=cfg['table']))
	os.system('pip install websockets --user')
	x = True
try:
	import requests as rq
except:
	print(gradient("! Couldn't import requests", text_clr=gt[cfg['obc']], use_table=cfg['table']))
	print(gradient("- Installing...", text_clr=gt[cfg['oc']], use_table=cfg['table']))
	os.system('pip install requests --user')
	x = True
try:
	import httpx as xrq
except:
	print(gradient("! Couldn't import httpx", text_clr=gt[cfg['obc']], use_table=cfg['table']))
	print(gradient("- Installing...", text_clr=gt[cfg['oc']], use_table=cfg['table']))
	os.system('pip install httpx --user')
	x = True

if x:
	print(gradient("- Installed dependencies", text_clr=gt[cfg['ogc']], use_table=cfg['table']))
	print(gradient("- Please re-run [2/3]", text_clr=gt[cfg['oc']], use_table=cfg['table']))
	exit()

try:
	BeautifulSoup('<p></p>', 'html5lib')
except:
	os.system('pip install html5lib --user')
	print(gradient("- Installed dependencies", text_clr=gt[cfg['ogc']], use_table=cfg['table']))
	print(gradient("- Please re-run [3/3]", text_clr=gt[cfg['oc']], use_table=cfg['table']))
	exit()

import os
import re
import json
import base64
import asyncio
import concurrent.futures
from time import sleep
from copy import deepcopy as dc
from random import choice as rc

def xa(app, fun: str | None=None):
	tw = os.get_terminal_size()[0]
	print(padhit(gradient(hit(cfg['names'][app], cfg['font']), 2, [cfg['clr'], cfg['clr']], use_table=cfg['table']), tw))
	print(padhit(gradient(cfg['ctxt'], text_clr=cfg['cg'], use_table=cfg['table']), tw)); print()
	if fun: print(gradient(f"-- {fun.upper()} --", text_clr=cfg['fg'], use_table=cfg['table']))

def xai(txt: str='', foo=str, fake=None, default='', live: bool=False) -> str:
	out = gradient(f"{txt} > ", text_clr=cfg['fg'], use_table=cfg['table'])+rgb('#', cfg['ic'], use_table=cfg['table']).split('#')[0]
	if fake is not None:
		print(f'{out}{fake}\033[0m')
		return fake
	while True:
		if live:
			print(out, end='', flush=True)
			resp = input_listen()
			print(resp)
		else:
			resp = input(out)
		
		if resp == '' or (live and resp == 'Enter'):
			resp = dc(default)
			print(f'\033[1A{out}{resp}\033[0m')
		else: print('\033[0m', end='', flush=True)
		try: return foo(resp)
		except: pass

def check(txt, fake=None):
	if fake is not None:
		xai(f"{txt} [Y/N]", fake=rgb(f"[{'YES' if fake else 'NO'}]", cfg['ic'], use_table=cfg['table']))
		return fake
	resp = xai(txt+' [Y/N]').lower() != 'n'
	print(f"\033[1A\033[{len(txt+' [Y/N] > ')}C"+rgb(f"[{'YES' if resp else 'NO'}]", cfg['ic'], use_table=cfg['table']))
	return resp

#####

game_codes = {
	'blooket': ['?'*7, '0123456789'],
	'kahoot': ['?'*7, '0123456789']
}

def blooket_check_id(id: str) -> dict:
	try:
		x = rq.get('https://play.blooket.com/play', cookies={}, headers={
			"Host": "play.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "none",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
	except: return {'success': False, 'error': "Couldn't connect"}
	try: key = BeautifulSoup(x.content, 'html.parser').select_one('input[name="$ACTION_KEY"]').get('value')
	except: return {'success': False, 'error': "Couldn't get init key"}

	try:
		bound = f'---------------------------'+''.join([rc('1234567890') for _ in range(30)])
		x = rq.post('https://play.blooket.com/play', cookies={}, headers={
			"Host": "play.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/x-component",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://play.blooket.com/play",
			"Next-Action": "f6fe184a2ddb16eb2027c85eb32bf9520fcde0a7",
			"Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(routes)%22%2C%7B%22children%22%3A%5B%22play%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fplay%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
			"Content-Type": f"multipart/form-data; boundary={bound}",
			"Origin": "https://play.blooket.com",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Priority": "u=0",
		}, data=(
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_REF_1"\r\n\r\n'
			"\r\n"
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_1:0"\r\n\r\n'
			'{"id":"f6fe184a2ddb16eb2027c85eb32bf9520fcde0a7","bound":"$@1"}\r\n'
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_1:1"\r\n\r\n'
			'[0,{"message":""}]\r\n'
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_KEY"\r\n\r\n'
			f"{key}\r\n"
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_join-code"\r\n\r\n'
			f"{id}\r\n"
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="0"\r\n\r\n'
			'[0,{"message":""},"$K1"]\r\n'
			f"--{bound}--\r\n"
		))
		if x.status_code == 303:
			return {'success': True, 'correct': True}
		elif str(x.content).split('\\n1:{"message":"')[1].split('\\\\n')[0] == 'Internal Server Error':
			return {'success': True, 'correct': False}
		return {'success': False, 'error': str(x.content)}
	except: return {'success': False, 'error': "Couldn't init"}

def game_finder(game: str, icode: str | None=None) -> str | None:
	assert game in game_codes.keys()
	code = (('' if icode is None else icode)+game_codes[game][0])[:len(game_codes[game][0])]	

	codes = [i if i in game_codes[game][1] else '' for i in code]

#####

with open('achieve/data.js', encoding='utf-8') as f:
	achieve_jsdata = f.read()
achieve_data = {j[0][1:].replace('`', ''): [k.replace('`', '') for k in j[1][:-2].split('`, `')] for j in [i.strip('    ').split(']: [') for i in [l for l in achieve_jsdata.split('\n') if l.strip() != ''][1:-1] if i.strip()[:2] != '//' and i.strip() != '']}

def achieve_answer(session: str, max_streak: int | None=None) -> None:
	while True:
		ans = None
		x = rq.get('https://achieve.hashtag-learning.co.uk/assess/question-page/', cookies={'sessionid': session})
		soup = BeautifulSoup(x.content, 'html5lib')
		try:
			csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except IndexError:
			achieve_restart(session)
		qn = [i.text for i in soup.find_all('h5') if i.text[:9] == 'Question '][0][9:].split(' of ')

		try:
			streak = int(soup.select_one('div#streak h5').text.strip())
		except AttributeError:
			streak = 0
		if max_streak is not None and streak >= max_streak:
			tw = os.get_terminal_size()[0]
			sl = len(str(streak)) if len(str(streak)) > 6 else 6
			out = session
			if len(session) > (tw-sl-3):
				out = session[:tw-sl-6]+'...'
			print(f"{' '*(tw-len(out)-sl-3)}{out} \u2502 {streak}")
			return

		# May break
		qhtml = re.sub(r'\s+', ' ', soup.select_one('.card-header.question-card-header.pt-4.pb-4.border-secondary > .row.m-0 > .col').decode_contents()).strip().replace('/>', '>')
		if soup.select_one('#text-answer'):
			for i in achieve_data[qhtml]:
				if i[0] == '>':
					ans = i[1:]
					break
			
			y = rq.post('https://achieve.hashtag-learning.co.uk/assess/text-button-clicked/', data={
				'text_answer': ans, 'actual_question': qn[0], 'csrfmiddlewaretoken': csrf
			}, headers={
				"Origin": "https://achieve.hashtag-learning.co.uk",
				"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={session}",
			})
		else:
			buttons, dupkey = {}, None
			buttonl = soup.select_one('.card-body.question-card-body').select('button.btn.btn-assess-choice.btn-block')
			for i in buttonl:
				key = i.find_parent().find_parent().find_parent().select_one('.m-1.pt-5.pb-5.pr-2.pl-2.border.border-info.flex-grow-1').decode_contents().strip().replace('/>', '>')
				if key in buttons: dupkey = dc(key)
				buttons[key] = i.get('id')
			
			if dupkey and achieve_data[qhtml][0].split('##id=')[0] == dupkey:
				ans = achieve_data[qhtml][0].split('##id=')[1].split('button_')[1]
			else:
				for i in achieve_data[qhtml]:
					if i in buttons:
						ans = buttons[i].split('button_')[1];
						break

			y = rq.post('https://achieve.hashtag-learning.co.uk/assess/mc-button-clicked/', data={
				'button_value': ans, 'actual_question': qn[0], 'csrfmiddlewaretoken': csrf
			}, headers={
				"Origin": "https://achieve.hashtag-learning.co.uk",
				"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={session}",
			})

		if ans is None: raise ValueError(f'Answer is None')

		tw = os.get_terminal_size()[0]
		streak = str(streak + (1 if y.ok else 0))
		sl = len(streak) if len(streak) > 6 else 6
		out = f"{y.status_code:>3} \u2502 {qn[0]:>4}/{qn[1]} \u2502 {session}"
		if len(out) > (tw-sl-3):
			out = out[:tw-sl-6]+'...'
		out = f"{out}{' '*(tw-len(out)-sl-3)} \u2502 {streak}"
		print(gradient(out, text_clr=gt[cfg['oc']], use_table=cfg['table']))
		if qn[0] == qn[1]:
			achieve_restart(session)

def achieve_restart(session: str):
	x = rq.get('https://achieve.hashtag-learning.co.uk/assess/course/choose-questions/', cookies={'sessionid': session})
	soup = BeautifulSoup(x.content, 'html.parser')
	csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
	qamt = soup.find_all('button', attrs={'class': 'btn achieve-cta-button'})[-1].text.strip().split('All (')[1][:-1]

	# TODO: Condense headers
	rq.post('https://achieve.hashtag-learning.co.uk/assess/course/choose-questions/', data={
		'submit': 'submit', 'questions': qamt, 'csrfmiddlewaretoken': csrf
	}, cookies={
		'sessionid': session, 'csrftoken': x.cookies['csrftoken']
	}, headers={
		"Host": "achieve.hashtag-learning.co.uk",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br, zstd",
		"Referer": "https://achieve.hashtag-learning.co.uk/assess/question-page/",
		"Content-Length": "117",
		"Origin": "https://achieve.hashtag-learning.co.uk",
		"DNT": "1",
		"Sec-GPC": "1",
		"Connection": "keep-alive",
		"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={session}",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "no-cors",
		"Sec-Fetch-Site": "same-origin",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"X-CSRFToken": csrf,
		"X-Requested-With": "XMLHttpRequest",
		"Priority": "u=0",
		"Pragma": "no-cache",
		"Cache-Control": "no-cache"
	})

def achieve_create_session(email: str, password: str) -> str:
	with rq.session() as rqs:
		x = rqs.get('https://achieve.hashtag-learning.co.uk/accounts/login/')
		soup = BeautifulSoup(x.content, 'html.parser')
		csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')

		tkn = rqs.post('https://achieve.hashtag-learning.co.uk/accounts/login/', data={
			'csrfmiddlewaretoken': csrf, 'login': email, 'password': password
		}, cookies={
			'csrftoken': x.cookies['csrftoken']
		}, headers={
			"Origin": "https://achieve.hashtag-learning.co.uk",
		})
	return tkn.cookies['sessionid']

def achieve_create_account(email: str, password: str, school: str, fname: str='\u2800', lname: str='\u2800') -> tuple:
	print(gradient('Creating session...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	with rq.Session() as rqs:
		print(gradient('Getting sign up csrf token...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		x = rqs.get('https://achieve.hashtag-learning.co.uk/accounts/signup-l/')
		soup = BeautifulSoup(x.content, 'html.parser')
		try: csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except: print(x.content)

		print(gradient('Signing up...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		signup = rqs.post('https://achieve.hashtag-learning.co.uk/accounts/signup-l/', data={
			'csrfmiddlewaretoken': csrf, 'email': email, 'password1': password, 'password2': password
		}, cookies={
			'csrftoken': x.cookies['csrftoken']
		}, headers={
			"Host": "achieve.hashtag-learning.co.uk",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://achieve.hashtag-learning.co.uk/accounts/signup-l/",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": "163",
			"Origin": "https://achieve.hashtag-learning.co.uk",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"csrftoken={x.cookies['csrftoken']}",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i"
		})
		if not signup.ok: raise ValueError("Couldn't sign up")

		print(gradient('Getting naming csrf token...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		x = rqs.get('https://achieve.hashtag-learning.co.uk/base/learner-school-account/')
		soup = BeautifulSoup(x.content, 'html.parser')
		try: csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except: print(x.content)

		print(gradient('Naming...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		setname = rqs.post('https://achieve.hashtag-learning.co.uk/base/learner-school-account/', data={
			'csrfmiddlewaretoken': csrf, 'first_name': fname, 'last_name': lname, 'save-learner-details': 'Save'
		}, cookies={
			'csrftoken': x.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
		}, headers={
			"Host": "achieve.hashtag-learning.co.uk",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://achieve.hashtag-learning.co.uk/base/learner-school-account/",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": "143",
			"Origin": "https://achieve.hashtag-learning.co.uk",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
		if not setname.ok: raise ValueError("Couldn't name")

		print(gradient('Getting school joiner csrf token...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		x = rqs.get('https://achieve.hashtag-learning.co.uk/base/learner-school-account/')
		soup = BeautifulSoup(x.content, 'html.parser')
		try: csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except: print(x.content)

		print(gradient('Checking school code...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		checksc = rqs.post('https://achieve.hashtag-learning.co.uk/base/check-school-class-code/', data={
			'typed_code': school,
			'csrfmiddlewaretoken': csrf
		}, cookies={
			'csrftoken': x.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
		}, headers={
			"Host": "achieve.hashtag-learning.co.uk",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://achieve.hashtag-learning.co.uk/base/learner-school-details/",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"X-CSRFToken": csrf,
			"X-Requested-With": "XMLHttpRequest",
			"Content-Length": "103",
			"Origin": "https://achieve.hashtag-learning.co.uk",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
		})
		if checksc.json()['is_valid']:
			print(gradient(f'Found school: "{checksc.json()["name"]}"', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		else:
			raise ValueError(f"Couldn't find school ({school})")

		print(gradient('Joining school...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		joinschool = rqs.post('https://achieve.hashtag-learning.co.uk/base/learner-school-details/', data={
			'csrfmiddlewaretoken': csrf,
			'school_code_field': school,
			'save-learner-school': 'Save',
		}, cookies={
			'csrftoken': x.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
		}, headers={
			"Host": "achieve.hashtag-learning.co.uk",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://achieve.hashtag-learning.co.uk/base/learner-school-details/",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": "136",
			"Origin": "https://achieve.hashtag-learning.co.uk",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
		if not joinschool.ok: raise ValueError("Couldn't join school")

		print(gradient('Getting subjects csrf token...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		x = rqs.get('https://achieve.hashtag-learning.co.uk/course/learner-courses-at-startup/')
		soup = BeautifulSoup(x.content, 'html.parser')
		try: csrf = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')
		except: print(x.content)
		
		print(gradient('Getting subjects...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		subjects = [[i.get('id').split('-')[0], i.get('id').split('-')[1], i.select_one('span').text.strip()] for i in [*list(soup.select('div#n5-subjects button')), *list(soup.select('div#h-subjects button'))]]

		subjects = [
			# ['4', '75', 'Accounting'],
			# ['4', '19', 'Administration and IT'],
			# ['4', '15', 'Applications of Maths'],
			# ['4', '16', 'Art and Design'],

			['4', '6',  'Biology'], 
			['4', '5',  'Business Management'],
			# ['4', '30', 'Care'],
			['4', '8',  'Chemistry'],

			# ['4', '21', 'Computer Games Dev'],
			['4', '3',  'Computing Science'],
			['4', '20', 'Design and Manufacture'],
			# ['4', '82', 'Economics'],

			['4', '83', 'Engineering Science'],
			['4', '7',  'English'],
			['4', '67', 'French'],
			['4', '11', 'Geography'],

			['4', '28', 'Graphic Communication'],
			# ['4', '74', 'Health & Food Technology'],
			['4', '13', 'History'],
			['4', '4',  'Mathematics'],

			# ['4', '12', 'Modern Studies'],
			# ['4', '10', 'Music'],
			# ['4', '29', 'Music Technology'],
			# ['4', '14', 'Numeracy'],

			# ['4', '18', 'PE'],
			['4', '9',  'Physics'],
			# ['4', '33', 'Practical Cookery'],
			# ['4', '78', 'Practical Woodworking'],

			# ['4', '79', 'RMPS'],
			# ['4', '32', 'Spanish'],
			# ['4', '80', 'Travel & Tourism']
		]
		print(gradient('Adding subjects...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		for l, i, n in subjects:
			addsub = rqs.post('https://achieve.hashtag-learning.co.uk/course/save-course-selected/', data={
				'is_selected': 'true',
				'level_pk': l,
				'subject_pk': i,
				'csrfmiddlewaretoken': csrf
			}, cookies={
				'csrftoken': x.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
			}, headers={
				"Host": "achieve.hashtag-learning.co.uk",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
				"Accept": "*/*",
				"Accept-Language": "en-US,en;q=0.5",
				"Accept-Encoding": "gzip, deflate, br, zstd",
				"Referer": "https://achieve.hashtag-learning.co.uk/course/learner-courses-at-startup/",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"X-CSRFToken": csrf,
				"X-Requested-With": "XMLHttpRequest",
				"Content-Length": "126",
				"Origin": "https://achieve.hashtag-learning.co.uk",
				"DNT": "1",
				"Sec-GPC": "1",
				"Connection": "keep-alive",
				"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
				"Sec-Fetch-Dest": "empty",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Site": "same-origin",
				"Priority": "u=0",
			})
			if addsub.ok:
				print(gradient(f"Added {'Higher' if l == '5' else 'Nat 5'} {n}", text_clr=gt[cfg['ogc']], use_table=cfg['table']))
			else:
				print(gradient(f"Couldn't add {'Higher' if l == '5' else 'Nat 5'} {n}", text_clr=gt[cfg['obc']], use_table=cfg['table']))

		print(gradient('Finishing...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		rqs.get('https://achieve.hashtag-learning.co.uk/')

	return email, password

def achieve_set_subject(session: str, subject: str, level: str='4'):
	x = rq.get('https://achieve.hashtag-learning.co.uk/course/change-achieve-course/', cookies={'sessionid': session})
	soup = BeautifulSoup(x.content, 'html.parser')
	csrf = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')

	setsub = rq.post('https://achieve.hashtag-learning.co.uk/course/change-achieve-course/', data={
		'csrfmiddlewaretoken': csrf,
		'subject_pk': subject,
		'level_pk': level,
		'referrer': 'https://achieve.hashtag-learning.co.uk/assess/assess-home/',
		'submit': 'learn'
	}, cookies={
		'csrftoken': x.cookies['csrftoken'], 'sessionid': session
	}, headers={
		"Host": "achieve.hashtag-learning.co.uk",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate, br, zstd",
		"Referer": "https://achieve.hashtag-learning.co.uk/course/change-achieve-course/",
		"Content-Type": "application/x-www-form-urlencoded",
		"Origin": "https://achieve.hashtag-learning.co.uk",
		"DNT": "1",
		"Sec-GPC": "1",
		"Connection": "keep-alive",
		"Cookie": f"csrftoken={x.cookies['csrftoken']}; sessionid={session}",
		"Upgrade-Insecure-Requests": "1",
		"Sec-Fetch-Dest": "document",
		"Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "same-origin",
		"Sec-Fetch-User": "?1",
		"Priority": "u=0, i",
	})
	if not setsub.ok: raise ValueError("Couldn't set subject")

def achieve_acc_gen():
	xa('Achieve', 'account generator')
	amt, email, password, school, name, save = xai('amount', int), xai('email (sup. ?#)'), xai('password', default='BaldyBaldy'), xai('school code', default='ycbceaPv'), xai('name (sup. ?#)'), check('save?')

	accs = []
	print(gradient('Generating accounts...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	for i in range(amt):
		remail, rpassword = achieve_create_account(''.join([rc('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') if i == '?' else i for i in email]).replace('#', str(i+1)), password, school, '\u2800' if name == '' else ''.join([rc('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') if i == '?' else i for i in name]).replace('#', str(i+1)))
		accs.append(f'{remail}:{rpassword}')

	if save:
		print(gradient('Saving accounts...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		with open('achieve/accounts.csv', 'a') as f:
			f.write('\n'.join(accs)+'\n')
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

def achieve_session_gen():
	xa('Achieve', 'token generator')
	info = []
	if check('use saved?'):
		with open('achieve/accounts.csv') as f:
			raw = f.read()
		info = [i.split(':') for i in raw.split('\n') if i != '']
	else:
		info = [[xai('email'), xai('password', default='BaldyBaldy')]]

	le = ''
	for i in info:
		if len(i[0]) > len(le): le = i[0]
	
	amt = xai('amount per acc', int, default=8)
	print(gradient('Generating tokens...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	sessions = []
	for n, acc in enumerate(info):
		for _ in range(amt):
			session = achieve_create_session(acc[0], acc[1])
			out = f'{str((n*amt)+_+1):>{len(str(len(info)*amt))}}/{len(info)*amt} \u2502 {acc[0]:<{len(le)}} \u2502 {session}'
			tw = os.get_terminal_size()[0]
			if len(out) > tw:
				out = out[:tw-3]+'...'
			print(gradient(out, text_clr=gt[cfg['oc']], use_table=cfg['table']))
			sessions.append(session)
	print(gradient('Saving...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	with open('achieve/tokens.txt', 'w') as f:
		f.write('\n'.join(sessions))
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

def achieve_subject():
	xa('Achieve', 'change subject')
	tokens = []
	if check('use saved?'):
		with open('achieve/tokens.txt') as f:
			raw = f.read()
		tokens = [i for i in raw.split('\n') if i != '']
	else:
		tokens = [i.strip() for i in xai('token(s)').split(',') if i != '']
	
	level = '5' if not check('nat 5?') else '4'
	sub = str(xai('subject id', int))
	print(gradient('Changing subjects...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	for n, token in enumerate(tokens):
		try: achieve_set_subject(token, sub, level)
		except: return
		out = f'{str(n+1):>{len(str(len(tokens)))}}/{len(tokens)} \u2502 {token}'
		tw = os.get_terminal_size()[0]
		if len(out) > tw:
			out = out[:tw-3]+'...'
		print(gradient(out, text_clr=gt[cfg['oc']], use_table=cfg['table']))
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

def achieve_school_exploit():
	xa('Achieve', 'get school code')
	if check('use saved?'):
		with open('achieve/teacher-token.txt') as f:
			raw = f.read()
		token = raw.replace('\n', '').strip()
	else:
		print('Teacher token gen coming soon...')
		return

	with rq.Session() as rqs:
		print(gradient('Joining session...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		x = rqs.get('https://achieve.hashtag-learning.co.uk/school/', cookies={'sessionid': token})
		
		soup = BeautifulSoup(x.content, 'html.parser')
		print(gradient('Getting csrf...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		csrf = x.cookies.get('csrftoken')
		csrfmw = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')
		print(gradient('Scraping schools...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		schools = [[i.text.strip().split(' (')[0], i.text.strip().split(' (')[1][:-1], i['value']] for i in soup.select_one('select#school').select('option')]
		if check('search by name?'):
			while True:
				cls(); xa('Achieve', 'get school code')
				first = xai('first letter', lambda _: 1/0 if _.lower() not in 'abcdefghijklmnopqrstuvwxyz' else _, live=True).lower()
				filtered = sorted([i for i in schools if i[0][0].lower() == first])
				print(); print(gtable([*[i[0] for i in filtered], '- BACK [Enter]'], 1, 1, cfg['gtclr'], 2, use_table=cfg['table']));  print()
				sn = xai('school', int, default='0')
				if sn != 0:
					sid = filtered[sn-1]
					break
		else:
			print('Council search coming soon...')
			return
		
		print(gradient('Getting join code...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		x = rqs.post(
			'https://achieve.hashtag-learning.co.uk/update-teacher-school/',
			headers={'Referer': 'https://achieve.hashtag-learning.co.uk/school/'},
			data={'csrfmiddlewaretoken': csrfmw, 'school': sid[2]},
			cookies={'csrftoken': csrf, 'sessionid': token}
		)
		if not x.ok: raise ValueError("Couldn't get join code")
		code = x.json()['school_code']

		cls(); xa('Achieve', 'get school code')
		print()
		print(gradient(f'Council: {sid[1]}', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		print(gradient(f' School: {sid[0]}', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		print(gradient('   Code:', text_clr=gt[cfg['oc']], use_table=cfg['table']), gradient(code, text_clr=gt[cfg['ogc']], use_table=cfg['table']))
		print()

		if check('save?'):
			with open('achieve/schools.txt', 'a', encoding='utf-8') as f:
				f.write(f'{sid[0]}: {code}\n')
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

def achieve_main():
	xa('Achieve', 'answer spammer')
	tokens = []
	if check('use saved?'):
		with open('achieve/tokens.txt') as f:
			raw = f.read()
		tokens = [i for i in raw.split('\n') if i != '']
	else:
		tokens = [i.strip() for i in xai('token(s)').split(',') if i != '']
	ms = xai('max streak', int, default='1000')
	ms = None if ms <= 0 else ms

	print(gradient('Starting tokens...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	for n, t in enumerate(tokens):
		achieve_restart(t)
		print(gradient(f'{str(n+1):>{len(str(len(tokens)))}}/{len(tokens)} \u2502 {t}', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	with concurrent.futures.ThreadPoolExecutor() as executor:
		print(gradient('Creating threads...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		futures = [executor.submit(achieve_answer, t, ms) for t in tokens]
		print(gradient('Spamming...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
		for future in concurrent.futures.as_completed(futures): future.result()
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

def achieve_accs():
	xa('Achieve', 'accounts')
	with open('achieve/accounts.csv') as f:
		raw = f.read()
	for i in [i for i in raw.split('\n') if i != '']:
		print(gradient(i, text_clr=gt[cfg['oc']], use_table=cfg['table']))
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

achieve_menu = [('Account Gen', achieve_acc_gen), ('Token Gen', achieve_session_gen), ('Set Subject', achieve_subject), ('Answer Spammer', achieve_main), ('View Accounts', achieve_accs), ('School Finder', achieve_school_exploit)]

#####

async def blooket_wsc(url, token, id, name, blook, headers):
	print(headers)
	async with websockets.connect(url, user_agent_header=headers['User-Agent'], additional_headers=headers) as ws:
		await ws.recv()
		await ws.send('''{"t":"d","d":{"r":1,"a":"s","b":{"c":{"sdk.js.10-11-0":1}}}}''')
		await ws.send('''{"t":"d","d":{"r":2,"a":"auth","b":{"cred":"'''+token+'''"}}}''')
		await ws.send('''{"t":"d","d":{"r":3,"a":"q","b":{"p":"/'''+id+'''","h":""}}}''')
		await ws.recv()
		await ws.recv()
		await ws.recv()
		await ws.recv()
		await ws.send('''{"t":"d","d":{"r":4,"a":"n","b":{"p":"/'''+id+'''"}}}''')
		await ws.send('''{"t":"d","d":{"r":5,"a":"p","b":{"p":"/'''+id+'''/c/'''+name+'''","d":{"b":"'''+blook+'''"}}}}''')
		await ws.recv()
		await ws.recv()
		await ws.send('''{"t":"d","d":{"r":6,"a":"q","b":{"p":"/'''+id+'''/c","h":""}}}''')
		await ws.send('''{"t":"d","d":{"r":7,"a":"q","b":{"p":"/'''+id+'''/stg","h":""}}}''')
		await ws.recv()
		await ws.recv()
		await ws.recv()
		await ws.recv()
		await ws.send('''{"t":"d","d":{"r":8,"a":"p","b":{"p":"/'''+id+'''/c/'''+name+'''","d":{"b":"'''+blook+'''"}}}}''')
		await ws.recv()
		await ws.send('0')

def blooket_uws(url, token, id, name, blook, headers={}):
	asyncio.run(blooket_wsc(url, token, id, name, blook, headers))

blooket_blooks = ['Chick', 'Chicken', 'Cow', 'Goat', 'Horse', 'Pig', 'Sheep', 'Duck', 'Alpaca', 'Dog', 'Cat', 'Rabbit', 'Goldfish', 'Hamster', 'Turtle', 'Kitten', 'Puppy', 'Bear', 'Moose', 'Fox', 'Raccoon', 'Squirrel', 'Owl', 'Hedgehog', 'Deer', 'Wolf', 'Beaver', 'Tiger', 'Orangutan', 'Cockatoo', 'Parrot', 'Anaconda', 'Jaguar', 'Macaw', 'Toucan', 'Panther', 'Capuchin', 'Gorilla', 'Hippo', 'Rhino', 'Giraffe', 'Snowy Owl', 'Polar Bear', 'Arctic Fox', 'Baby Penguin', 'Penguin', 'Arctic Hare', 'Seal', 'Walrus', 'Witch', 'Wizard', 'Elf', 'Fairy', 'Slime Monster', 'Jester', 'Dragon', 'Queen', 'Unicorn', 'King', 'Two of Spades', 'Eat Me', 'Drink Me', 'Alice', 'Queen of Hearts', 'Dormouse', 'White Rabbit', 'Cheshire Cat', 'Caterpillar', 'Mad Hatter', 'King of Hearts', 'Toast', 'Cereal', 'Yogurt', 'Breakfast Combo', 'Orange Juice', 'Milk', 'Waffle', 'Pancakes', 'French Toast', 'Pizza', 'Earth', 'Meteor', 'Stars', 'Alien', 'Planet', 'UFO', 'Spaceship', 'Astronaut', 'Lil Bot', 'Lovely Bot', 'Angry Bot', 'Happy Bot', 'Watson', 'Buddy Bot', 'Brainy Bot', 'Mega Bot', 'Old Boot', 'Jellyfish', 'Clownfish', 'Frog', 'Crab', 'Pufferfish', 'Blobfish', 'Octopus', 'Narwhal', 'Dolphin', 'Baby Shark', 'Megalodon', 'Panda', 'Sloth', 'Tenrec', 'Flamingo', 'Zebra', 'Elephant', 'Lemur', 'Peacock', 'Chameleon', 'Lion', 'Amber', 'Dino Egg', 'Dino Fossil', 'Stegosaurus', 'Velociraptor', 'Brontosaurus', 'Triceratops', 'Tyrannosaurus Rex', 'Ice Bat', 'Ice Bug', 'Ice Elemental', 'Rock Monster', 'Dink', 'Donk', 'Bush Monster', 'Yeti', 'Dingo', 'Echidna', 'Koala', 'Kookaburra', 'Platypus', 'Joey', 'Kangaroo', 'Crocodile', 'Sugar Glider', 'Deckhand', 'Buccaneer', 'Swashbuckler', 'Treasure Map', 'Seagull', 'Jolly Pirate', 'Pirate Ship', 'Kraken', 'Captain Blackbeard', 'Snow Globe', 'Holiday Gift', 'Hot Chocolate', 'Holiday Wreath', 'Stocking', 'Gingerbread Man', 'Gingerbread House', 'Reindeer', 'Snowman', 'Santa Claus']
def blooket_send(id, name, blook=None):
	if blook == 'random' or blook is None:
		blook = rc(blooket_blooks)

	try:
		x = rq.get('https://play.blooket.com/play', cookies={}, headers={
			"Host": "play.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "none",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
	except: return {'success': False, 'error': "Couldn't connect"}
	try: key = BeautifulSoup(x.content, 'html.parser').select_one('input[name="$ACTION_KEY"]').get('value')
	except: return {'success': False, 'error': "Couldn't get init key"}

	try:
		bound = f'---------------------------696969696969696969696969696969'
		x = rq.post('https://play.blooket.com/play', cookies={}, headers={
			"Host": "play.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/x-component",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://play.blooket.com/play",
			"Next-Action": "f6fe184a2ddb16eb2027c85eb32bf9520fcde0a7",
			"Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(routes)%22%2C%7B%22children%22%3A%5B%22play%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fplay%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
			"Content-Type": f"multipart/form-data; boundary={bound}",
			"Origin": "https://play.blooket.com",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Priority": "u=0",
		}, data=(
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_REF_1"\r\n\r\n'
			"\r\n"
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_1:0"\r\n\r\n'
			'{"id":"f6fe184a2ddb16eb2027c85eb32bf9520fcde0a7","bound":"$@1"}\r\n'
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_1:1"\r\n\r\n'
			'[0,{"message":""}]\r\n'
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_$ACTION_KEY"\r\n\r\n'
			f"{key}\r\n"
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="1_join-code"\r\n\r\n'
			f"{id}\r\n"
			f"--{bound}\r\n"
			'Content-Disposition: form-data; name="0"\r\n\r\n'
			'[0,{"message":""},"$K1"]\r\n'
			f"--{bound}--\r\n"
		))
	except: return {'success': False, 'error': "Couldn't init"}
	try:
		url = x.headers.get('x-action-redirect')
		rooturl = url.strip('https://').split('/')[0]
	except: return {'success': False, 'error': "Couldn't get game info"}

	try:
		x = rq.get(url, cookies={}, headers={
			"Host": rooturl,
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Referer": "https://play.blooket.com/",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-site",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
	except: return {'success': False, 'error': "Couldn't start session"}
	try: bsid = x.cookies['bsid']
	except: return {'success': False, 'error': "Couldn't get bsid"}

	try:
		x = rq.get(f'https://{rooturl}/apipbinit', cookies={'bsid': bsid}, headers={
			"Host": "goldquest.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": url,
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"bsid={bsid}",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Priority": "u=4",
		})
	except: return {'success': False, 'error': "Couldn't init game"}
	try: bpcsrf = x.cookies['_bp_csrf_id']
	except: return {'success': False, 'error': "Couldn't get csrf"}

	try:
		x = rq.get(f"https://fb.blooket.com/c/firebase/id?id={id}", cookies={'bsid': bsid}, headers={
			"Host": "fb.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "application/json, text/plain, */*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": "https://{rooturl}/",
			"Origin": "https://{rooturl}",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"bsid={bsid}",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-site",
			"Priority": "u=0",
		})
	except: return {'success': False, 'error': "Couldn't check ID"}
	if not x.json()['success']: return {'success': False, 'error': "Incorrect game ID"}

	try:
		x = rq.put('https://fb.blooket.com/c/firebase/join', cookies={'bsid': bsid}, json={'id': id, 'name': name}, headers={
			"Host": "fb.blooket.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "application/json, text/plain, */*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Referer": f"https://{rooturl}/",
			"Content-Type": "application/json",
			"Content-Length": "32",
			"Origin": f"https://{rooturl}",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Cookie": f"bsid={bsid}",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-site",
			"Priority": "u=0",
		})
	except: return {'success': False, 'error': "Couldn't set name"}
	try: fb = {'shard': x.json()['fbShardURL'], 'token': x.json()['fbToken'], 'success': x.json()['success']}
	except:
		if x.json()['success']: return {'success': False, 'error': "Couldn't get shard/token"}
		else:
			nameerrors = {
				'taken': 'Name Taken',
				'invalid name': 'Invalid Name',
				'missing game id or name in request': 'Missing Game ID or Name'
			}
			return {'success': False, 'error': nameerrors[x.json()['msg']] if x.json()['msg'] in nameerrors else x.json()['msg']}
	try: wsns = fb['shard'].split('://')[1].split('.firebase')[0]
	except: return {'success': False, 'error': "Couldn't parse shard"}
	try:
		x = rq.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=AIzaSyCA-cTOnX19f6LFnDVVsHXya3k6ByP_MnU', cookies={}, headers={
			"Host": "identitytoolkit.googleapis.com",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"X-Client-Version": "Firefox/JsCore/10.11.0/FirebaseCore-web",
			"X-Firebase-gmpid": "1:741533559105:web:b8cbb10e6123f2913519c0",
			"Content-Type": "application/json",
			"Content-Length": "865",
			"Origin": f"https://{rooturl}",
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "cross-site",
			"Priority": "u=6",
			"TE": "trailers",
		}, json={
			'returnSecureToken': True,
			'token': fb['token']
		})
	except: return {'success': False, 'error': "Couldn't init auth"}
	try: token = x.json()['idToken']
	except: return {'success': False, 'error': "Couldn't get websocket token"}

	try: wskey = base64.b64encode(os.urandom(16)).decode('utf-8')
	except: return {'success': False, 'error': "Couldn't generate websocket key"}  # Should never fail
	try:
		x = blooket_uws(f"{fb['shard'].replace('https://', 'wss://')}.ws?v=5&p=1:741533559105:web:b8cbb10e6123f2913519c0", token, id, name, blook, {
			"Host": fb['shard'].strip('https://').split('/')[0],
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br, zstd",
			"Sec-WebSocket-Version": "13",
			"Origin": f"https://{rooturl}",
			"Sec-WebSocket-Extensions": "permessage-deflate",
			"Sec-WebSocket-Key": wskey,
			"DNT": "1",
			"Sec-GPC": "1",
			"Connection": "keep-alive, Upgrade",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "websocket",
			"Sec-Fetch-Site": "cross-site",
			"Pragma": "no-cache",
			"Cache-Control": "no-cache",
			"Upgrade": "websocket",
		})
		if x == 1: 
			pass  # special output for ghost bots???
	except Exception as e: return {'success': False, 'error': f"Websocket error\n{e}"}
	return {'success': True, 'error': None}

def blooket_output(oid, resp):
	out = f"{oid} \u2502 {str(resp['success']):<5} \u2502 {resp['error']}"
	print(gradient(out, text_clr=gt[cfg['o'+('g' if resp['success'] else 'b')+'c']], use_table=cfg['table']))

def blooket_use_server(baseurl, oid, id, name, blook, amt):
	if amt > 99: amt = 99
	with rq.get(f'{baseurl}/api/blooket?id={id}&name={name}s&blook={blook}&amt={amt}', stream=True) as resp:
		if resp.status_code == 200:
			for line in resp.iter_lines():
				if line:
					try: data = json.loads(line.decode('utf-8')[5:].strip())
					except Exception as e: data = {'success': False, 'error': f"Response error: {e}"}
					blooket_output(oid, data)

def blooket_spam(rid, id, name, blook, iamt, server=False):
	if server:
		samt = int(iamt/(len(SERVER_LIST)+1))
		ramt = iamt-(samt*len(SERVER_LIST))
	else: samt, ramt = 0, dc(iamt)

	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = [executor.submit(blooket_send, id, f'{name[-10:]}{rid}{_+1}', blook) for _ in range(ramt)]
		if samt > 0:
			server_futures = [executor.submit(blooket_use_server, f'https://xmods{sn}.glitch.me', sn, id, f'{name[-10:]}{rid}{sn}', blook, samt) for sn in SERVER_LIST]
			for sfuture in concurrent.futures.as_completed(server_futures): sfuture.result()
		
		for future in concurrent.futures.as_completed(futures):
			try:
				result = future.result()
				blooket_output('-', result)
			except Exception as e:
				blooket_output('-', {'success': False, 'error': f'Server Exception: {e}'})

blooket_ntoac = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
blooket_ntoa = [i+j+k for i in blooket_ntoac for j in blooket_ntoac for k in blooket_ntoac]
blooket_run_ids = 'abcdefghijklmnopqrstuvwxyzABDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def blooket_main():
	xa('Blooket', 'Bot Generator')
	id, name, blook, amt, server = str(xai('ID', int)), xai('name', default='x '), xai('blook', default='random'), xai('amount', default='fill'), check('use servers?')

	if server and check('ping servers?'):
		cls(); server_ping(); cls()
		xa('Blooket', 'Bot Generator')
		xai('ID', fake=id)
		xai('name', fake=name)
		xai('blook', fake=blook)
		xai('amount', fake=amt)
		check('use servers?', fake=server)
		check('ping servers?', fake=True)

	if amt is None or amt in ['fill', 'max']:
		name = name[-10:]
		check_amt, ran_amt = 0, 0
		while True:
			blooket_spam(blooket_run_ids[ran_amt], id, name, blook, 60, server)
			ran_amt += 1
			success = False
			while not success:
				check_amt += 1  # Max is 140607 (len(ntoa)-1), but that should never be hit (would require at least 39+ hours of constant running at 1 rq per sec)
				resp = blooket_send(id, f"{name}C{blooket_run_ids[ran_amt]}{blooket_ntoa[check_amt]}", blook)
				blooket_output('?', resp)
				success = resp['success']
	else:
		amt = int(amt)
		if amt > 99: amt = 99
		blooket_spam(' ', id, name[-13:], blook, amt, server)
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))

blooket_menu = [('Bot Generator', blooket_main)]

#####

def server_ping():
	xa('Server', 'Server Ping')
	print('\033[?25l', end='', flush=True)
	print(gradient('Pinging servers...', text_clr=gt[cfg['oc']], use_table=cfg['table']))
	for i in SERVER_LIST:
		out = f' \u2502 xmods{i}.glitch.me \u2502 '
		print(gradient(f'   {out}', text_clr=gt['d'], use_table=cfg['table'])+'\r', end='', flush=True)
		resp = rq.get(f'https://xmods{i}.glitch.me/api/v')
		try: out2 = f"v{resp.json()['version']}"
		except: out2 = 'error'
		print(gradient(f"{resp.status_code}{out}{out2}", text_clr=gt[cfg['o'+('g' if resp.ok else 'b')+'c']], use_table=cfg['table']))
	print(gradient('Done!', text_clr=gt[cfg['ogc']], use_table=cfg['table']))
	print('\033[?25h', end='', flush=True)

server_menu = [('Ping', server_ping)]

#####

apps = {
	'Achieve': achieve_menu,
	'Blooket': blooket_menu,
	'Server': server_menu
}

sleep(.2)
cli_app([(i, lambda i=i: cli_app(apps[i], cfg['columns'], cfg['names'][i], cfg['ctxt'], cfg['font'], cfg['mg'], 1, border=cfg['border'], use_table=cfg['table'], exit_fun=True), True) for i in apps], cfg['columns'], cfg['main']['name'], cfg['ctxt'], cfg['font'], cfg['mg'], 1, border=cfg['border'], img=cfg['main']['img'], gap=0, use_table=cfg['table'], exit_fun=True)
