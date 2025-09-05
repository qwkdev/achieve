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
def FANCY_LOG(text: str | None=None) -> None:
	'''Fancy logging function, same as the default logging function but with (changing) colors.
	
	Use this function by using: `achieve.LOG = achieve.FANCY_LOG`
	To complete a task (make it go green) without starting another, pass in `None` or a falsy value, (or just leave arguments blank)
	'''

	global _FANCY_LOG_CURRENT_TASK
	if _FANCY_LOG_CURRENT_TASK:
		print(f"\033[1A\r\033[32m{datetime.now().strftime('[%H:%M:%S]')} {_FANCY_LOG_CURRENT_TASK}   \033[0m")

	if text:
		print(f"\033[30m{datetime.now().strftime('[%H:%M:%S]')} {text}...\033[0m")
	
	_FANCY_LOG_CURRENT_TASK = text if text else None

# '''Gets a list of all schools and their info.
#
# :param teacher_token: Valid token (sessionid) for a teacher account.
# :type teacher_token: str
#
# :returns: A list of lists with school info. Contains:
#
# 	- str: School Name
#
# 	- str: Council
#
# 	- str: Achieve ID
# :rtype: list of [str, str, str]
# '''

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


		