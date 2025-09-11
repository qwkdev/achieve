import os
import subprocess
import re
import json
import concurrent.futures
import time
import copy
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup

try:
	BeautifulSoup('<p></p>', 'html5lib')
except:
	raise ImportError('Please install html5lib for bs4: `pip install html5lib`')

#! TODO: Add logs to everything
def LOG(text: str | None=None) -> None:
	'''Create a logging function and assign `achieve.LOG` to it.

	OR use the example function by using: `achieve.LOG = achieve.DEFAULT_LOG`
	You can also use `achieve.LOG = achieve.FANCY_LOG` for simple, colorful output.

	### All logs are sent here in this format:
	(in example function)
	1. LOG('Starting task')
	2. First task code...
	3. LOG('Starting second task')
	4. Second task code...
	etc...
	
	:param text: The current task about to be done
	:type text: str (accepts None, but is only used on fancy output)
	'''

	return None

def DEFAULT_LOG(text: str | None=None) -> None:
	'''Default logging function, just outputs (prints) the current tasks and the time.
	
	Use this function by using: `achieve.LOG = achieve.DEFAULT_LOG`'''

	if text is not None:
		print(datetime.now().strftime('[%H:%M:%S]'), text)

_FANCY_LOG_CURRENT_TASK = None
_FANCY_LOG_CURRENT_TASK_START_TIME = 0
def FANCY_LOG(text: str | None=None) -> None:
	'''Fancy logging function, same as the default logging function but with (changing) colors.
	
	Use this function by using: `achieve.LOG = achieve.FANCY_LOG`
	To complete a task (make it go green) without starting another, pass in `None` or a falsy value, (or just leave arguments blank)
	'''

	global _FANCY_LOG_CURRENT_TASK, _FANCY_LOG_CURRENT_TASK_START_TIME
	if _FANCY_LOG_CURRENT_TASK:
		print(f"\033[1A\r\033[32m{datetime.now().strftime('[%H:%M:%S]')} {_FANCY_LOG_CURRENT_TASK}\033[0m \033[30m[{round(time.perf_counter() - _FANCY_LOG_CURRENT_TASK_START_TIME, 3)}s]\033[0m")

	if text:
		print(f"\033[30m{datetime.now().strftime('[%H:%M:%S]')} {text}...\033[0m")
	
	_FANCY_LOG_CURRENT_TASK = text if text else None
	_FANCY_LOG_CURRENT_TASK_START_TIME = time.perf_counter()

def get_schools(teacher_token: str) -> list[str, str, str]:
	'''Gets a list of all schools and their info.

	:param teacher_token: Valid token (sessionid) for a teacher account.
	:type teacher_token: str
	
	:returns: A list of lists with school info. Contains:

		- str: School Name

		- str: Council

		- str: Achieve ID
	:rtype: list of [str, str, str]
	'''
	LOG('Starting')
	with requests.Session() as rqs:
		LOG('Getting or sm idk')
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/school/', cookies={'sessionid': teacher_token})
		soup = BeautifulSoup(rqg.content, 'html.parser')
		LOG('Finishing'); LOG()
		return [[
			i.text.strip().split(' (')[0],
			i.text.strip().split(' (')[1][:-1],
			i['value']
		] for i in soup.select_one('select#school').select('option')]

#####

subjects = {
	'n5': {
		'Accounting': '75',
		'Administration and IT': '19',
		'Applications of Maths': '15',
		'Art and Design': '16',
		'Biology': '6',
		'Business Management': '5',
		'Care': '30',
		'Chemistry': '8',
		'Computer Games Dev': '21',
		'Computing Science': '3',
		'Design and Manufacture': '20',
		'Economics': '82',
		'Engineering Science': '83',
		'English': '7',
		'Esports': '84',
		'French': '67',
		'Geography': '11',
		'German': '86',
		'Graphic Communication': '28',
		'Health & Food Technology': '74',
		'History': '13',
		'Mathematics': '4',
		'Modern Studies': '12',
		'Music': '10',
		'Music Technology': '29',
		'Numeracy': '14',
		'PE': '18',
		'Photography': '66',
		'Physics': '9',
		'Practical Cookery': '33',
		'Practical Woodworking': '78',
		'RMPS': '79',
		'Spanish': '32',
		'Travel & Tourism': '80'
	},
	'h': {
		'Accounting': '75',
		'Administration and IT': '19',
		'Applications of Maths': '15',
		'Art and Design': '16',
		'Biology': '6',
		'Business Management': '5',
		'Chemistry': '8',
		'Computing Science': '3',
		'Design and Manufacture': '20',
		'English': '7',
		'French': '67',
		'Geography': '11',
		'Graphic Communication': '28',
		'Health & Food Technology': '74',
		'History': '13',
		'Human Biology': '17',
		'Mathematics': '4',
		'Modern Studies': '12',
		'Music': '10',
		'Music Technology': '29',
		'PE': '18',
		'Philosophy': '81',
		'Photography': '66',
		'Physics': '9',
		'Politics': '85',
		'Psychology': '31',
		'RMPS': '79',
		'Spanish': '32'
	},
	'ah': {
		'Business Management': '5',
		'Computing Science': '3'
	}
}

def subject(level: str, name: str | None=None) -> list[str, str]:
	...

def get_school_code(teacher_token: str, school_id: str | int) -> str:
	with requests.Session() as rqs:
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/school/', cookies={'sessionid': teacher_token})
		
		soup = BeautifulSoup(rqg.content, 'html.parser')
		csrf = rqg.cookies.get('csrftoken')
		csrfmw = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')
		
		rqg = rqs.post(
			'https://achieve.hashtag-learning.co.uk/update-teacher-school/',
			headers={'Referer': 'https://achieve.hashtag-learning.co.uk/school/'},
			data={'csrfmiddlewaretoken': csrfmw, 'school': str(school_id)},
			cookies={'csrftoken': csrf, 'sessionid': teacher_token}
		)
		if not rqg.ok: raise ValueError("Couldn't get join code")

		return rqg.json()['school_code']

def create_account(email: str, password: str, school_code: str, first_name: str='\u2800', last_name: str='\u2800', subjects: list[list[str | int, str | int]] | None=None) -> None:
	with requests.Session() as rqs:
		LOG('Getting sign up csrf token')
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/accounts/signup-l/')
		soup = BeautifulSoup(rqg.content, 'html.parser')
		try: csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except: raise ValueError("Couldn't get csrf")

		LOG('Signing up')
		signup = rqs.post('https://achieve.hashtag-learning.co.uk/accounts/signup-l/', data={
			'csrfmiddlewaretoken': csrf, 'email': email, 'password1': password, 'password2': password
		}, cookies={
			'csrftoken': rqg.cookies['csrftoken']
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
			"Cookie": f"csrftoken={rqg.cookies['csrftoken']}",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i"
		})
		if not signup.ok: raise ValueError("Couldn't sign up")

		LOG('Getting naming csrf token')
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/base/learner-school-account/')
		soup = BeautifulSoup(rqg.content, 'html.parser')
		try: csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except: raise ValueError("Couldn't get csrf")

		LOG('Naming')
		setname = rqs.post('https://achieve.hashtag-learning.co.uk/base/learner-school-account/', data={
			'csrfmiddlewaretoken': csrf, 'first_name': first_name, 'last_name': last_name, 'save-learner-details': 'Save'
		}, cookies={
			'csrftoken': rqg.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
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
			"Cookie": f"csrftoken={rqg.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
		if not setname.ok: raise ValueError("Couldn't name")

		LOG('Getting school joiner csrf token')
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/base/learner-school-account/')
		soup = BeautifulSoup(rqg.content, 'html.parser')
		try: csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')
		except: raise ValueError("Couldn't get csrf")

		LOG('Checking school code')
		checksc = rqs.post('https://achieve.hashtag-learning.co.uk/base/check-school-class-code/', data={
			'typed_code': school_code,
			'csrfmiddlewaretoken': csrf
		}, cookies={
			'csrftoken': rqg.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
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
			"Cookie": f"csrftoken={rqg.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
		})
		if checksc.json()['is_valid']:
			LOG(f'Found school: "{checksc.json()["name"]}"')
		else:
			raise ValueError(f"Couldn't find school ({school_code})")

		LOG('Joining school')
		joinschool = rqs.post('https://achieve.hashtag-learning.co.uk/base/learner-school-details/', data={
			'csrfmiddlewaretoken': csrf,
			'school_code_field': school_code,
			'save-learner-school': 'Save',
		}, cookies={
			'csrftoken': rqg.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
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
			"Cookie": f"csrftoken={rqg.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
			"Upgrade-Insecure-Requests": "1",
			"Sec-Fetch-Dest": "document",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-User": "?1",
			"Priority": "u=0, i",
		})
		if not joinschool.ok: raise ValueError("Couldn't join school")

		LOG('Getting subjects csrf token')
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/course/learner-courses-at-startup/')
		soup = BeautifulSoup(rqg.content, 'html.parser')
		try: csrf = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')
		except: raise ValueError("Couldn't get csrf")
		
		LOG('Getting subjects')

		# , i.select_one('span').text.strip()
		if subjects == None:
			selected_subjects = [[i.get('id').split('-')[0], i.get('id').split('-')[1]] for i in [*list(soup.select('div#n5-subjects button')), *list(soup.select('div#h-subjects button')), *list(soup.select('div#ah-subjects button'))]]
			# LOG(); print(selected_subjects)
		else:
			selected_subjects = [[str(i[0]), str(i[1])] for i in subjects]
		
		LOG('Adding subjects')
		for level, sid in selected_subjects:
			addsub = rqs.post('https://achieve.hashtag-learning.co.uk/course/save-course-selected/', data={
				'is_selected': 'true',
				'level_pk': level,
				'subject_pk': sid,
				'csrfmiddlewaretoken': csrf
			}, cookies={
				'csrftoken': rqg.cookies['csrftoken'], 'sessionid': rqs.cookies.get_dict()['sessionid']
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
				"Cookie": f"csrftoken={rqg.cookies['csrftoken']}; sessionid={rqs.cookies.get_dict()['sessionid']}",
				"Sec-Fetch-Dest": "empty",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Site": "same-origin",
				"Priority": "u=0",
			})

		LOG('Finishing')
		rqs.get('https://achieve.hashtag-learning.co.uk/')

	LOG()

def create_session(email: str, password: str) -> str:
	with requests.session() as rqs:
		rqg = rqs.get('https://achieve.hashtag-learning.co.uk/accounts/login/')
		soup = BeautifulSoup(rqg.content, 'html.parser')
		csrf = soup.find_all('input', attrs={'name': 'csrfmiddlewaretoken'})[0].get('value')

		token = rqs.post('https://achieve.hashtag-learning.co.uk/accounts/login/', data={
			'csrfmiddlewaretoken': csrf, 'login': email, 'password': password
		}, cookies={
			'csrftoken': rqg.cookies['csrftoken']
		}, headers={
			"Origin": "https://achieve.hashtag-learning.co.uk",
		})
	return token.cookies['sessionid']


