QHIT_CLR_ESC = '\uABCD'

import json
import os
from functools import lru_cache
from time import sleep
from threading import Thread
from copy import deepcopy as dc
import re
with open('qhit_data.json', encoding='utf-8') as f:
	qhitdata = json.load(f)
with open('qhit_img_data.json', encoding='utf-8') as f:
	qhitimgdata = json.load(f)

qhit_clr_table = [  # all ansi ESC[(3/4)8;5;#m colours
	[0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0], [0, 0, 128], [128, 0, 128], [0, 128, 128], [192, 192, 192], [128, 128, 128], [255, 0, 0], [0, 255, 0], [255, 255, 0], [0, 0, 255], [255, 0, 255], [0, 255, 255], [255, 255, 255],
	[0, 0, 0], [0, 0, 95], [0, 0, 135], [0, 0, 175], [0, 0, 215], [0, 0, 255], [0, 95, 0], [0, 95, 95], [0, 95, 135], [0, 95, 175], [0, 95, 215], [0, 95, 255], [0, 135, 0], [0, 135, 95], [0, 135, 135], [0, 135, 175], [0, 135, 215], [0, 135, 255], [0, 175, 0], [0, 175, 95], [0, 175, 135], [0, 175, 175], [0, 175, 215], [0, 175, 255], [0, 215, 0], [0, 215, 95], [0, 215, 135], [0, 215, 175], [0, 215, 215], [0, 215, 255], [0, 255, 0], [0, 255, 95], [0, 255, 135], [0, 255, 175], [0, 255, 215], [0, 255, 255], [95, 0, 0], [95, 0, 95], [95, 0, 135], [95, 0, 175], [95, 0, 215], [95, 0, 255], [95, 95, 0], [95, 95, 95], [95, 95, 135], [95, 95, 175], [95, 95, 215], [95, 95, 255], [95, 135, 0], [95, 135, 95], [95, 135, 135], [95, 135, 175], [95, 135, 215], [95, 135, 255], [95, 175, 0], [95, 175, 95], [95, 175, 135], [95, 175, 175], [95, 175, 215], [95, 175, 255], [95, 215, 0], [95, 215, 95], [95, 215, 135], [95, 215, 175], [95, 215, 215], [95, 215, 255], [95, 255, 0], [95, 255, 95], [95, 255, 135], [95, 255, 175], [95, 255, 215], [95, 255, 255], [135, 0, 0], [135, 0, 95], [135, 0, 135], [135, 0, 175], [135, 0, 215], [135, 0, 255], [135, 95, 0], [135, 95, 95], [135, 95, 135], [135, 95, 175], [135, 95, 215], [135, 95, 255], [135, 135, 0], [135, 135, 95], [135, 135, 135], [135, 135, 175], [135, 135, 215], [135, 135, 255], [135, 175, 0], [135, 175, 95], [135, 175, 135], [135, 175, 175], [135, 175, 215], [135, 175, 255], [135, 215, 0], [135, 215, 95], [135, 215, 135], [135, 215, 175], [135, 215, 215], [135, 215, 255], [135, 255, 0], [135, 255, 95], [135, 255, 135], [135, 255, 175], [135, 255, 215], [135, 255, 255], [175, 0, 0], [175, 0, 95], [175, 0, 135], [175, 0, 175], [175, 0, 215], [175, 0, 255], [175, 95, 0], [175, 95, 95], [175, 95, 135], [175, 95, 175], [175, 95, 215], [175, 95, 255], [175, 135, 0], [175, 135, 95], [175, 135, 135], [175, 135, 175], [175, 135, 215], [175, 135, 255], [175, 175, 0], [175, 175, 95], [175, 175, 135], [175, 175, 175], [175, 175, 215], [175, 175, 255], [175, 215, 0], [175, 215, 95], [175, 215, 135], [175, 215, 175], [175, 215, 215], [175, 215, 255], [175, 255, 0], [175, 255, 95], [175, 255, 135], [175, 255, 175], [175, 255, 215], [175, 255, 255], [215, 0, 0], [215, 0, 95], [215, 0, 135], [215, 0, 175], [215, 0, 215], [215, 0, 255], [215, 95, 0], [215, 95, 95], [215, 95, 135], [215, 95, 175], [215, 95, 215], [215, 95, 255], [215, 135, 0], [215, 135, 95], [215, 135, 135], [215, 135, 175], [215, 135, 215], [215, 135, 255], [215, 175, 0], [215, 175, 95], [215, 175, 135], [215, 175, 175], [215, 175, 215], [215, 175, 255], [215, 215, 0], [215, 215, 95], [215, 215, 135], [215, 215, 175], [215, 215, 215], [215, 215, 255], [215, 255, 0], [215, 255, 95], [215, 255, 135], [215, 255, 175], [215, 255, 215], [215, 255, 255], [255, 0, 0], [255, 0, 95], [255, 0, 135], [255, 0, 175], [255, 0, 215], [255, 0, 255], [255, 95, 0], [255, 95, 95], [255, 95, 135], [255, 95, 175], [255, 95, 215], [255, 95, 255], [255, 135, 0], [255, 135, 95], [255, 135, 135], [255, 135, 175], [255, 135, 215], [255, 135, 255], [255, 175, 0], [255, 175, 95], [255, 175, 135], [255, 175, 175], [255, 175, 215], [255, 175, 255], [255, 215, 0], [255, 215, 95], [255, 215, 135], [255, 215, 175], [255, 215, 215], [255, 215, 255], [255, 255, 0], [255, 255, 95], [255, 255, 135], [255, 255, 175], [255, 255, 215], [255, 255, 255], [8, 8, 8], [18, 18, 18], [28, 28, 28], [38, 38, 38], [48, 48, 48], [58, 58, 58], [68, 68, 68], [78, 78, 78], [88, 88, 88], [98, 98, 98], [108, 108, 108], [118, 118, 118], [128, 128, 128], [138, 138, 138], [148, 148, 148], [158, 158, 158], [168, 168, 168], [178, 178, 178], [188, 188, 188], [198, 198, 198], [208, 208, 208], [218, 218, 218], [228, 228, 228], [238, 238, 238]
]
qhit_gradient_presets = {
	'rainbow': [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (255, 0, 0)],
	'brainbow': [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255), (255, 0, 0)][::-1]
}

def version():
	print('QHIT - Version 2.4.2 - 10/02/25')

def update():
	import requests as rq
	exec(rq.get('https://qwk.pythonanywhere.com/hit/install').json()['code'])
	exit()

def cls() -> None:
	"""Clears the screen using system commands. (Changes to fit OS)"""
	os.system('cls' if os.name == 'nt' else 'clear')

def clr(txt: str='?', ri: str='w', fse: int=0) -> str:
	"""Basic wrapper for basic ANSI colour codes"""
	endclr = '\033[0m'
	if fse == 2:
		return endclr
	clrs = 'drgybmcw'
	if len(ri) == 1:
		i = f'1{ri}.'
	elif len(ri) == 2:
		i = f'1{ri}'
	else:
		i = ri
	opclr = f"\033[{i[0]};{int(clrs.index(i[1].lower())) + (30 if i[1].isupper() else 90)}{'' if i[2] == '.' else ';'+str(int(clrs.index(i[2].lower())) + 40)}m"
	if fse == 1:
		return opclr
	return f"{opclr}{txt.replace(endclr, endclr+opclr)}{endclr}"

def ansilen(txt: str) -> int:
	ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
	return len(ansi_escape.sub('', txt))

def sliceansi(txt: str, start: int=0, end: int=-1) -> str:
	start, end = start if start >= 0 else ansilen(txt)+start, end if end >= 0 else ansilen(txt)+end
	nai, in_ansi, ansi_esc, resp = 0, False, '\033', ''
	for i in txt:
		if nai >= start:
			resp += i
		if i == ansi_esc: in_ansi = True
		elif in_ansi and i == 'm': in_ansi = False
		elif not in_ansi:
			nai += 1
		if nai == end:
			break
	return resp

@lru_cache(maxsize=None)
def rgbtotable(irgb: tuple | list) -> int:
	"""Returns the closest matching ANSI colour ID to the given RGB"""
	return sorted([[sum([abs(i[0]-irgb[0]), abs(i[1]-irgb[1]), abs(i[2]-irgb[2])]), n+16] for n, i in enumerate(qhit_clr_table[16:])])[0][1]

def rgb(text: str, text_clr: tuple=None, bg_clr: tuple=None, bold: bool=False, use_table: bool=False) -> str:
	"""Wrapper for RGB ANSI colour codes"""
	clrcode, endclr = ['1'] if bold else [], '\033[0m'
	if not use_table:
		if text_clr is not None:
			clrcode.extend(['38', '2'])
			clrcode.extend([f'{str(i):0>3}' for i in text_clr])
		if bg_clr is not None:
			clrcode.extend(['48', '2'])
			clrcode.extend([f'{str(i):0>3}' for i in bg_clr])
	else:
		if text_clr is not None:
			clrcode.extend(['38', '5', f'{str(rgbtotable(text_clr)):0>3}'])
		if bg_clr is not None:
			clrcode.extend(['48', '5', f'{str(rgbtotable(bg_clr)):0>3}'])
	opclr = f"\033[{';'.join(clrcode)}m"
	return f"{opclr}{text.replace(endclr, endclr+opclr)}{endclr}"

def gradient(text: str, direction: int=0, text_clr: list[tuple] | str='rainbow', bold: bool=False, interval: int | None=None, use_table: bool=False, auto_escape_ansi=False) -> str:
	"""Wrapper for using ANSI colour codes to create gradients. (Supports multi-line text)"""
	if auto_escape_ansi: text = text.replace('\033[0m', '~{QHIT-ESCAPED-ANSI-STYLING-RESET}~').replace('\033[', QHIT_CLR_ESC+'\033[').replace('~{QHIT-ESCAPED-ANSI-STYLING-RESET}~', '\033[0m'+QHIT_CLR_ESC)
	if type(text_clr) == str and text_clr in qhit_gradient_presets.keys():
		text_clr = qhit_gradient_presets[text_clr]
	text = text.split('\n')
	text_width = max(len(l) for l in text)
	if interval is None:
		match direction:
			case 1:
				interval = int(len(text)/(len(text_clr)-1))
			case 2 | 3:
				interval = int((len(text)+text_width)/(len(text_clr)-1))
			case _:
				interval = int(text_width/(len(text_clr)-1))

	clrs = [text_clr[0]]
	for n, i in enumerate(text_clr[:-1]):
		dif = [list(j) for j in zip(*[[int(((text_clr[n+1][j]-i[j])/interval)*(k+1)) for k in range(interval)] for j in range(3)])]
		for j in dif:
			clrs.append((i[0]+j[0], i[1]+j[1], i[2]+j[2]))

	in_clr_esc = False
	match direction:
		case 1:
			resp = ''
			for n, i in enumerate(text):
				for j in i:
					if j == QHIT_CLR_ESC: in_clr_esc = not in_clr_esc
					elif in_clr_esc: resp += j
					else:
						try: resp += rgb(j, clrs[n], None, bold, use_table)
						except IndexError: resp += rgb(j, text_clr[-1], None, bold, use_table)
				resp += '\n'
			return resp[:-1]
		case 2 | 3:
			resp = ''
			for l, i in enumerate(text):
				for n, j in enumerate(i):
					if j == QHIT_CLR_ESC: in_clr_esc = not in_clr_esc
					elif in_clr_esc: resp += j
					else:
						try: resp += rgb(j, clrs[n+l if direction == 2 else (n+len(text))-l], None, bold, use_table)
						except IndexError: resp += rgb(j, text_clr[-1], None, bold, use_table)
				resp += '\n'
			return resp[:-1]
		case _:
			resp = ''
			for i in text:
				for n, j in enumerate(i):
					if j == QHIT_CLR_ESC: in_clr_esc = not in_clr_esc
					elif in_clr_esc: resp += j
					else:
						try: resp += rgb(j, clrs[n], None, bold, use_table)
						except IndexError: resp += rgb(j, text_clr[-1], None, bold, use_table)
				resp += '\n'
			return resp[:-1]

def clrc(txt, clrs, default='w', auto_escape_ansi=False):
	"""Maps colours to certain characters.
	clrs argument is in this format:
	[character (max 1)][colour as supported by clr() function] separated by commas.
	Example Usage:
	clrc('hello world', 'hr,lg,ob', 'm')
	would return 'hello world' in magenta (default="m"), but with the "h" coloured red (r), the "l"s coloured green (g), and the "o"s coloured blue (b)"""
	clrl = {i[0]: i[1:] for i in clrs.split(',')}
	if auto_escape_ansi: txt = txt.replace('\033[0m', '~{QHIT-ESCAPED-ANSI-STYLING-RESET}~').replace('\033[', QHIT_CLR_ESC+'\033[').replace('~{QHIT-ESCAPED-ANSI-STYLING-RESET}~', '\033[0m'+QHIT_CLR_ESC)

	resp, in_clr_esc = '', False
	for i in txt:
		if i == QHIT_CLR_ESC: in_clr_esc = not in_clr_esc
		elif in_clr_esc: resp += i
		else: resp += clr(i, clrl[i] if i in clrl.keys() else default)
	return resp

def pad_str_list(sl: list[str], n: int, pad='', end_first: bool=True) -> list[str]:
	if len(sl) == n: return sl
	end, resp = dc(end_first), dc(sl)

	while len(resp) < n:
		if end: resp.append(pad)
		else: resp.insert(0, pad)
		end = not end
	return resp

def hit(txt, font=0, mobile=False, cs=-1, sa=5, ol=False, codec=None, img: str | None=None, gap: str | int=1, align_right: bool=False) -> str | list[str]:
	"""Basically built-in FIGLET but with support for custom character replacement, spacing, and backgrounds.
	It can also take in any string passed into "img" (supports multi-line too) and will align it on the left or right (align_right=False (left) or True (right))
	You can also specify a gap for this, being either a string put inbetween, or the number of spaces to be used
	(Warning: Images not supported for ol output)"""
	if cs == -1:
		try: cs = [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1][font]
		except IndexError: cs = 0
	codec, hitchars, cil = codec if codec is not None else qhitdata[font]['mcodec' if mobile else 'codec'], qhitdata[font]['chars'].lower(), '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	if ol:
		ot = [[] for _ in range(qhitdata[font]['lines'])]
		for i in txt.lower():
			for j in range(qhitdata[font]['lines']):
				if i in hitchars:
					ot[j].append(qhitdata[font]['data'][j][hitchars.index(i)] + ('0'*cs))
				elif i == ' ':
					ot[j].append('0' * sa)
		return [[''.join([codec[cil.index(k)] for k in j]) for j in i] for i in ot]
	ot = ['' for _ in range(qhitdata[font]['lines'])]
	for i in txt.lower():
		for j in range(qhitdata[font]['lines']):
			if i in hitchars:
				ot[j] += qhitdata[font]['data'][j][hitchars.index(i)] + ('0'*cs)
			elif i == ' ':
				ot[j] += '0' * sa
	resp = [''.join([codec[cil.index(j)] for j in i]) for i in ot]
	if img is not None:
		imgl = img.split('\n')

		if len(imgl) >= len(resp):
			resp = pad_str_list(resp, len(imgl))
		else: imgl = pad_str_list(imgl, len(resp), end_first=False)

		div = ' '*gap if isinstance(gap, int) else gap
		for n, i in enumerate(resp):
			if not align_right: resp[n] = imgl[n]+div+i
			else: resp[n] = i+div+imgl[n]

	ml = len(max(resp, key=len))
	return '\n'.join([f"{i:{'>' if align_right else '<'}{ml}}" for i in resp])

def gtxt(txt, ingclrs, gdir=0) -> str:
	"""Legacy wrapper for basic, single line ANSI colour gradients, migrate to new gradient() function
	(if you cant support rgb ansi outputs, try setting use_table=True in gradient())"""
	gclrs, f, clrl = ingclrs.split(','), '', []
	if gdir == 1:
		gclrs = gclrs[:len(txt[0])]
		for i in gclrs:
			clrl.extend([i for _ in range(len(txt[0]) // len(gclrs))])
		clrl.extend([gclrs[-1] for _ in range(len(txt[0]) - len(clrl))])
		for i in txt:
			for n, j in enumerate(i):
				f += f"{clr(j, clrl[n])}"
			f += '\n'
		f = f[:-1]
	elif gdir == 2 or gdir == 3:
		gclrs = gclrs[:len(txt[0])]
		clrl.extend([gclrs[0] for _ in range(len(txt) // 2)])
		for i in gclrs:
			clrl.extend([i for _ in range(len(txt[0]) // len(gclrs))])
		clrl.extend([gclrs[-1] for _ in range(len(txt[0]) - len(clrl))])
		clrl.extend([gclrs[-1] for _ in range(len(txt))])
		for n, i in enumerate(txt):
			for m, j in enumerate(i):
				if gdir == 2:
					f += f"{clr(j, clrl[m+n])}"
				else:
					f += f"{clr(j, clrl[m+(len(txt)-n-1)])}"
			f += '\n'
		f = f[:-1]
	else:
		gclrs = gclrs[:len(txt)]
		for i in gclrs:
			clrl.extend([i for _ in range(len(txt) // len(gclrs))])
		clrl.extend([gclrs[-1] for _ in range(len(txt) - len(clrl))])
		for n, i in enumerate(txt):#
			for j in i:
				f += f"{clr(j, clrl[n])}"
			f += '\n'
		f = f[:-1]
	return f

def ghit(txt, ingclrs, gdir=0, font=0, mobile=False, cs=0, sa=5) -> str:
	"""Legacy wrapper for basic ANSI colour gradients, migrate to new gradient() function (supports multi-line text)"""
	return gtxt([''.join(i) for i in hit(txt, font, mobile, cs, sa, True)], ingclrs, gdir)

def padhit(txt: str, width: int, gradient: int | None=None, pad: int=0) -> str:
	"""Multi-line text alignment, with support for ANSI colour output from gradient(), takes padding size from length of the first line"""
	txt = txt.split('\n')
	match gradient:
		case 0:
			tl = int(len(txt[0])/15)
		case 1:
			tl = int(len(txt[0])/24)
		case 2:
			tl = int(len(txt[0])/18)
		case 3:
			tl = int(len(txt[0])/16)
		case 4:
			tl = len(txt[0])
		case _:
			tl = ansilen(txt[0])
	if pad == 1:
		return '\n'.join([f"{' '*(width-tl)}{i}" for i in txt])
	else:
		return '\n'.join([f"{' '*int((width-tl)/2)}{i}{' '*int(width-int((width-tl)/2)-tl)}" for i in txt])

def pos(x: int=0, y: int=0, tw: int | None=None, th: int | None=None) -> str:
	"""Returns an ansi string to move the cursor,
	with support for custom bounds.
	Clamped to terminal size by default"""
	ts = os.get_terminal_size()
	tw = tw if tw is not None else ts[0]
	th = th if th is not None else ts[1]

	return f"\033[{min(max(1, y+1), th)};{min(max(1, x+1), tw)}H"

def img(id: str) -> str:
	"""Returns an ascii image.
	Available images can be found by calling imgs()"""
	return qhitimgdata[id]

def imgs() -> list[str]:
	"""Returns a list of all available images"""
	return list(qhitimgdata.keys())

def banner(istr: str, lang: str='py', align: int=0) -> str:
	"""Hardcodes a multi-line banner with support for alignment.
	Supported Languages:
	[py] - Python
	[sh] - Bash
	[js] - JavaScript (No Alignment)"""
	txt = istr.split('\n')
	if lang == 'py':
		if align == 1:
			resp = f'import os\ntw = os.get_terminal_size()[0]\npadding = int((tw - {ansilen(txt[0])}) / 2)\n'
		elif align == 2:
			resp = f'import os\ntw = os.get_terminal_size()[0]\npadding = tw - {ansilen(txt[0])}\n'
		else:
			resp = ''
		if align in [1, 2]:
			resp += '\n'.join([f'print(f"""{{\' \'*padding}}{i}""")' for i in txt])
		else:
			resp += '\n'.join([f'print("""{i}""")' for i in txt])
	elif lang == 'sh':
		if align == 1:
			resp = f'tw=$(tput cols)\npadding=$(( (tw - {ansilen(txt[0])}) / 2 ))\n'
		elif align == 2:
			resp = f'tw=$(tput cols)\npadding=$(( tw - {ansilen(txt[0])} ))\n'
		else:
			resp = ''
		if align in [1, 2]:
			resp += '\n'.join([f'echo -e "$(printf "%*s" $padding ""){i}"' for i in txt])
		else:
			resp += '\n'.join([f'echo -e "{i}"' for i in txt])
	elif lang == 'js':
		if align in [1, 2]: raise ValueError("JavaScript doesn't support alignment")
		resp = '\n'.join([f'console.log("{i}");' for i in txt])
	else:
		raise ValueError('Language not supported.')
	return resp

# TODO: VVV WRITE DOCS VVV

def rgb_format(text: str) -> tuple[int]:
	numbers: str = ''
	response: list[str | int] = []

	for i in text:
		if i in '0123456789':
			numbers += i
		elif len(numbers) > 0:
			response.append(numbers)
			numbers = ''

		if len(numbers) == 3:
			response.append(numbers)
			numbers = ''
	response.append(numbers)

	return tuple([*[int(i) for i in response if i], *['0']*3][:3])

def ansiml(markup: str, use_table: bool=False) -> str:
	scope: list[str] = []
	in_tag: bool = False
	temp: str = ''
	response: str = ''
	for n, c in enumerate(markup):
		if in_tag:
			if c == '>':
				in_tag = False

				if temp[0] == '/':
					if temp[1:] in [i[0] for i in scope]:
						scope.pop(len(scope) - 1 - [i[0] for i in scope[::-1]].index(temp[1:]))
					response += f"\033[{';'.join(['0', *[i[1] for i in scope]])}m"
				else:
					ansicode: str = ''
					match temp.split(' ', 1)[0]:
						case 'red':        ansicode = '31'
						case 'orange':     ansicode = '33'
						case 'yellow':     ansicode = '33'
						case 'green':      ansicode = '32'
						case 'blue':       ansicode = '34'
						case 'dark-blue':  ansicode = '34'
						case 'dblue':      ansicode = '34'
						case 'purple':     ansicode = '35'
						case 'magenta':    ansicode = '35'
						case 'pink':       ansicode = '35'
						case 'cyan':       ansicode = '36'
						case 'lblue':      ansicode = '36'
						case 'light-blue': ansicode = '36'
						case 'grey':       ansicode = '37'
						case 'gray':       ansicode = '37'
						case 'black':      ansicode = '30'
						case 'dark':       ansicode = '30'
						case 'rgb': ansicode = rgb('x', rgb_format(temp.split(' ', 1)[1]), use_table=use_table).split('\033[', 1)[1].split('mx', 1)[0]
						case 'bold':          ansicode = '1'
						case 'strong':        ansicode = '1'
						case 'b':             ansicode = '1'
						case 'em':            ansicode = '1'
						case 'dim':           ansicode = '2'
						case 'i':             ansicode = '3'
						case 'italic':        ansicode = '3'
						case 'u':             ansicode = '4'
						case 'underline':     ansicode = '4'
						case 'blink':         ansicode = '5'
						case 'flash':         ansicode = '5'
						case 'invert':        ansicode = '7'
						case 'hidden':        ansicode = '8'
						case 's':             ansicode = '9'
						case 'strike':        ansicode = '9'
						case 'strikethrough': ansicode = '9'
						case _: ansicode = temp.split(' ', 1)[0]

					if temp.endswith('bg') or temp.endswith('background'):
						if ansicode[0] == '3':
							if len(ansicode) == 2:
								ansicode = f'4{ansicode[1]}'
							elif ansicode[1] == '8':
								ansicode = f'4{ansicode[1:]}'
					response += f'\033[{ansicode}m'
					scope.append([temp.split(' ', 1)[0], ansicode])
				temp = ''
			else:
				temp += c
		else:
			if c == '<' and ('' if n == 0 else markup[n-1]) != '\\':
				in_tag = True
				response += temp
				temp = ''
			else:
				temp += c

	if not in_tag: response += temp

	return f'{response}\033[0m'

def cli_app(ifunctions: list[list[str, object | None, bool]], columns: int=1, name: str='CLI APP', info: str='MADE BY ...', font: int=0, clrl: list | str='rainbow', direction: int=1, delay: float=0.05, border: str | None='─│╭╮╰╯', function_clr: bool=True, index_clr: int=0, img: str | None=None, gap: str | int=1, use_table: bool=False, exit_fun: bool=False) -> None:
	'''
	Runs a full CLI app menu for the provided functions

	:param functions: A list of iterables, having the format: [name: str, function: object, auto_return: bool (Optional)]
	Like for example: [('Function 1', foo1), ('Function 2', foo2, True)]
	The function reference can be None, which makes the text a header
	If auto_return is specified for a function, it just means that the function will exit without prompting "Press enter to return..."
	This is the only required parameter, everything else defaults
	:param columns: Number of columns to split up the options into
	Takes any int from 1-4 (Default = 1)
	:param name: The name to show as the logo (Default = 'CLI APP')
	:param info: The small text to show underneath the logo (Default = 'MADE BY ...')
	:param font: Qhit font ID to use for the logo (Default = 0)
	:param clrl: ANSI colour gradient to use for the logo, same format as the gradient() function (Default = 'rainbow')
	:param direction: Direction for the gradient to go in, and move (Default = 1)
	1:

	:param :  (Default = )
	'''
	def align2(text: str, where: int | str, width: int, char: str=' ') -> str:
		ftext = text.replace(QHIT_CLR_ESC, '')
		match where:
			case 0 | '^': padtext = f"{ftext:{char}^{width}}"
			case 1 | '>': padtext = f"{ftext:{char}>{width}}"
			case 2 | '<': padtext = f"{ftext:{char}<{width}}"
		return padtext.replace(ftext, text)

	functions = dc(ifunctions)

	if not function_clr:
		functions = [[f'{QHIT_CLR_ESC}{i[0]}{QHIT_CLR_ESC}', *i[1:]] for i in functions]

	if border is None: border = '	  '
	waiting_cmd, logo_cmd, clrs = True, '', []
	tw, th = os.get_terminal_size()
	tw = int(tw/2)*2  # fixes edge cases with border
	rawhit = hit(name, font, img=img, gap=gap)
	title = [f"{border[2]}{border[0]*(tw-2)}{border[3]}", *[border[1]+i[1:-1]+border[1] for i in padhit(rawhit, tw).split('\n')]]
	mfnw = len(max([j[0].replace(QHIT_CLR_ESC, '') for j in functions], key=len))
	def clrrealnum(num: str) -> str:
		return ''.join([f'{str(int(num))[0]}{j}' if m == 1 else f'{QHIT_CLR_ESC}{j}{QHIT_CLR_ESC}' for m, j in enumerate(num.split(str(int(num))[0], 1))])

	if exit_fun: functions.append(['Exit', lambda: None, True])

	functions = [[*j, n] for n, j in enumerate([i + (False,) if isinstance(i, tuple) else i + [False] if len(i) == 2 else i for i in functions])]
	rfl = [i for i in functions if i[1] is not None]
	def rfli(i):
		if exit_fun and functions.index(i) == len(functions)-1: return -1
		try: return rfl.index(i)
		except: return -1

	match index_clr:
		case 1:  # none
			fl = [(f"{QHIT_CLR_ESC}[{str(rfli(i)+1):0>{len(str(len(functions)))}}]{QHIT_CLR_ESC} ", f"{align2(i[0], '<', mfnw)}") for i in functions]
		case 2:  # only numbers
			fl = [(f"{QHIT_CLR_ESC}[{QHIT_CLR_ESC}{str(rfli(i)+1):0>{len(str(len(functions)))}}{QHIT_CLR_ESC}]{QHIT_CLR_ESC} ", f"{align2(i[0], '<', mfnw)}") for i in functions]
		case 3:  # only brackets
			fl = [(f"[{QHIT_CLR_ESC}{str(rfli(i)+1):0>{len(str(len(functions)))}}{QHIT_CLR_ESC}] ", f"{align2(i[0], '<', mfnw)}") for i in functions]
		case 4:  # only real numbers
			fl = [(f"{QHIT_CLR_ESC}[{QHIT_CLR_ESC}{clrrealnum(f'{str(rfli(i)+1):0>{len(str(len(functions)))}}')}{QHIT_CLR_ESC}]{QHIT_CLR_ESC} ", f"{align2(i[0], '<', mfnw)}") for i in functions]
		case 5:  # only brackets and real numbers
			fl = [(f"[{clrrealnum(f'{str(rfli(i)+1):0>{len(str(len(functions)))}}')}] ", f"{align2(i[0], '<', mfnw)}") for i in functions]
		case _:  # full
			fl = [(f"[{str(rfli(i)+1):0>{len(str(len(functions)))}}] ", f"{align2(i[0], '<', mfnw)}") for i in functions]
	fl = [(' '*len(fl[n][0]) if i[1] is None else fl[n][0])+fl[n][1] for n, i in enumerate(functions)]

	k, m = divmod(len(fl), columns)
	fl = [fl[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(columns)]  # list comp of slices
	fl = [[fl[j][n] for j in range(columns) if n in range(len(fl[j]))] for n in range(len(max(fl, key=len)))]
	if columns > len(fl[0]): columns = len(fl[0])
	for n, i in enumerate(fl):
		if columns > len(i): fl[n].extend(['']*(columns-len(i)))

	match columns:
		case 1: fltext = [align2(i[0], '^', tw) for i in fl]
		case 2: fltext = [f"{align2(i[0], '>', (tw//2)-1)}  {align2(i[1], '<', (tw//2)-1)}" for i in fl]
		case 3: fltext = [f"{align2(i[0], '>', (tw//2)-(len(i[1].replace(QHIT_CLR_ESC, ''))//2)-2)}  {i[1]}  {align2(i[2], '<', (tw//2)-(len(i[1].replace(QHIT_CLR_ESC, ''))//2)-2)}" for i in fl]
		case 4: fltext = [f"{align2(i[0], '>', (tw//2)-len(i[1].replace(QHIT_CLR_ESC, ''))-3)}  {i[1]}  {i[2]}  {align2(i[3], '<', (tw//2)-len(i[2].replace(QHIT_CLR_ESC, ''))-3)}" for i in fl]

	interval = int(len(max(rawhit.split('\n'), key=len))/2)+len(title)

	if type(clrl) == str:
		if clrl in qhit_gradient_presets.keys():
			cl = qhit_gradient_presets[clrl]
		else:
			cl = clrl
	elif type(clrl) == tuple:
		cl = rgbtotable(clrl)
	else:
		cl = clrl

	title.extend([f"{border[1]}{' '*(tw-2)}{border[1]}", f"{border[1]}{align2(info, '^', tw-2)}{border[1]}", f"{border[1]}{' '*(tw-2)}{border[1]}"])
	fltext = [f"{border[1]}{i[2 if i[0] == QHIT_CLR_ESC else 1:-2 if i[-1] == QHIT_CLR_ESC else -1]}{' '*(tw-len(i.replace(QHIT_CLR_ESC, ''))-1)}{border[1]}" for i in fltext]

	if type(cl) != str:
		title.extend([*fltext, f"{border[1]}{' '*(tw-2)}{border[1]}", border[1]+f"{'>>':>{(tw//2)-1}}\u28E1"[1:]+border[1]])
		borderafter = (th-len(title))-2
		title.extend([*[f"{border[1]}{' '*(tw-2)}{border[1]}" for _ in range(borderafter)], f"{border[4]}{border[0]*(tw-2)}{border[5]}"])

	if type(cl) == list:
		clrs = [cl[0]]
		for n, i in enumerate(cl[:-1]):
			dif = [list(j) for j in zip(*[[int(((cl[n+1][j]-i[j])/interval)*(k+1)) for k in range(interval)] for j in range(3)])]
			for j in dif:
				clrs.append((i[0]+j[0], i[1]+j[1], i[2]+j[2]))

		clrs *= (tw//len(clrs))+1

		def showlogo():
			nonlocal waiting_cmd, clrs
			first_loop, clrslen = True, len(clrs)
			while waiting_cmd:
				output = []  # appending to list is faster than string concatenation
				output_append = output.append  # faster than lookup
				if not first_loop: output_append('\033[s')
				output_append(f'\033[{len(title)+len(fltext)}A\r')
				for l, i in enumerate(title):
					n, noclr = 0, 0
					for j in i:
						if j == ' ':
							output_append(' ')
							n += 1
						elif j == '\u28E1':
							n += tw//2
							output_append(f'\033[{(tw//2)}C')
						elif j == QHIT_CLR_ESC:
							noclr = [1, 0][noclr]
						else:
							if noclr:
								output_append(f'\033[1m{j}\033[0m')
							else:
								clrsindex = n if direction in [0, 2] else n+l
								if clrsindex < clrslen: output_append(rgb(j, clrs[clrsindex], None, True, use_table))
								else: output_append(rgb(j, clrs[0], None, True, use_table))
							n += 1

					output_append('\n')

				if first_loop:
					output_append(f'\033[{borderafter+2}A\033[{(tw//2)-1}C\033[s')
					first_loop = False
				else:
					output_append('\033[u')

				print(''.join(output), end='', flush=True)

				if direction > 1:
					clrs = [clrs[-1], *clrs[:-1]]
				else:
					clrs = [*clrs[1:], clrs[0]]
				sleep(delay)

		def take_input():
			nonlocal waiting_cmd, logo_cmd
			try:
				logo_cmd = input('')
			except:
				waiting_cmd = False

		while True:
			print('\033[?25l')
			cls()
			waiting_cmd, logo_cmd = True, ''
			slogo = Thread(target=showlogo)
			wfi = Thread(target=take_input)
			slogo.start()
			wfi.start()
			wfi.join()
			waiting_cmd = False
			print('\033[?25h')
			cls()
			if logo_cmd in ['exit', 'quit'] or (exit_fun and logo_cmd == '0'): cls(); return
			elif logo_cmd in ['reset', 'restart', 'refresh', 'fix']:
				cli_app(ifunctions, columns, name, info, font, clrl, direction, delay, border, function_clr, index_clr, img, gap, use_table, exit_fun)
				return
			elif logo_cmd == '': pass
			else:
				try: rfl[int(logo_cmd)-1][1]()
				except Exception as e: print(f'Error:\n{e}')
				if not rfl[int(logo_cmd)-1][2]: input('\033['+'9'*99+'B\rPress enter to return...')

	elif type(cl) == str:
		if cl == '': cl = 'w,w,w,w,w'
		cl = cl.split(',')
		if cl[0].isdigit():
			cl = [*[int(i) for i in cl], 15, 15, 15, 15]
		else:
			cl.extend(['w', 'w', 'w', 'w'])
		while True:
			cls()
			b1 = clr(border[1], cl[4])
			print('\n'.join([
				'\033[?25h'+clr(title[0], cl[4]),
				*[b1+clr(i[1:-1], cl[0])+b1 for i in title[1:-3]],
				*[b1+clr(i[1:-1], cl[1])+b1 for i in title[-3:]],
				*[b1+clr(i[1:-1], cl[2])+b1 for i in fltext],
				b1+(' '*(tw-2))+b1,
				b1+clr(f"{'>>':>{(tw//2)-2}}{' '*(tw//2)}", cl[3])+b1,
				*[b1+(' '*(tw-2))+b1 for i in range(th-len(title)-len(fltext)-4)],
				clr(f'{border[4]}{border[0]*(tw-2)}{border[5]}', cl[4])+f'\033[{th-(len(title)+len(fltext)+3)}A\r\033[{(tw//2)-1}C'
			]).replace(QHIT_CLR_ESC, ''), end='', flush=True)
			ci = input('')
			if ci in ['exit', 'quit'] or (exit_fun and ci == '0'): cls(); return
			elif ci in ['reset', 'restart', 'refresh', 'fix']:
				cli_app(ifunctions, columns, name, info, font, clrl, direction, delay, border, function_clr, index_clr, img, gap, use_table, exit_fun)
				return
			elif ci == '': pass
			else:
				cls()
				try: rfl[int(ci)-1][1]()
				except Exception as e: print(f'Error:\n{e}')
				input('\033['+'9'*99+'B\rPress enter to return...')

def gtable(ichoices: list[str], columns: int=1, align: int=0, clrl: list | str='rainbow', direction: int=0, function_clr: bool=True, index_clr: int=0, use_table: bool=False):
	"""WARNING: Still in development
	Use "- ..." for header"""
	def align2(text: str, where: int | str, width: int, char: str=' ') -> str:
		ftext = text.replace(QHIT_CLR_ESC, '')
		match where:
			case 0 | '^': padtext = f"{ftext:{char}^{width}}"
			case 1 | '>': padtext = f"{ftext:{char}>{width}}"
			case 2 | '<': padtext = f"{ftext:{char}<{width}}"
		return padtext.replace(ftext, text)

	choices = [[i[2:], None] if i.startswith('- ') else [i, 1] for i in ichoices]

	if not function_clr:
		choices = [[f'{QHIT_CLR_ESC}{i[0]}{QHIT_CLR_ESC}', i[1]] for i in choices]

	tw = int(os.get_terminal_size()[0]/2)*2  # fixes edge cases with border
	mfnw = len(max([j[0].replace(QHIT_CLR_ESC, '') for j in choices], key=len))
	def clrrealnum(num: str) -> str:
		return ''.join([f'{str(int(num))[0]}{j}' if m == 1 else f'{QHIT_CLR_ESC}{j}{QHIT_CLR_ESC}' for m, j in enumerate(num.split(str(int(num))[0], 1))])

	choices = [[*j, n] for n, j in enumerate(choices)]
	rfl = [i for i in choices if i[1] is not None]
	def rfli(i):
		try: return rfl.index(i)
		except: return -1

	match index_clr:
		case 1:  # none
			fl = [(f"{QHIT_CLR_ESC}[{str(rfli(i)+1):0>{len(str(len(choices)))}}]{QHIT_CLR_ESC} ", f"{align2(i[0], '<', mfnw)}") for i in choices]
		case 2:  # only numbers
			fl = [(f"{QHIT_CLR_ESC}[{QHIT_CLR_ESC}{str(rfli(i)+1):0>{len(str(len(choices)))}}{QHIT_CLR_ESC}]{QHIT_CLR_ESC} ", f"{align2(i[0], '<', mfnw)}") for i in choices]
		case 3:  # only brackets
			fl = [(f"[{QHIT_CLR_ESC}{str(rfli(i)+1):0>{len(str(len(choices)))}}{QHIT_CLR_ESC}] ", f"{align2(i[0], '<', mfnw)}") for i in choices]
		case 4:  # only real numbers
			fl = [(f"{QHIT_CLR_ESC}[{QHIT_CLR_ESC}{clrrealnum(f'{str(rfli(i)+1):0>{len(str(len(choices)))}}')}{QHIT_CLR_ESC}]{QHIT_CLR_ESC} ", f"{align2(i[0], '<', mfnw)}") for i in choices]
		case 5:  # only brackets and real numbers
			fl = [(f"[{clrrealnum(f'{str(rfli(i)+1):0>{len(str(len(choices)))}}')}] ", f"{align2(i[0], '<', mfnw)}") for i in choices]
		case _:  # full
			fl = [(f"[{str(rfli(i)+1):0>{len(str(len(choices)))}}] ", f"{align2(i[0], '<', mfnw)}") for i in choices]
	fl = [(' '*len(fl[n][0]) if i[1] is None else fl[n][0])+fl[n][1] for n, i in enumerate(choices)]

	k, m = divmod(len(fl), columns)
	fl = [fl[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(columns)]  # list comp of slices
	fl = [[fl[j][n] for j in range(columns) if n in range(len(fl[j]))] for n in range(len(max(fl, key=len)))]
	if columns > len(fl[0]): columns = len(fl[0])
	for n, i in enumerate(fl):
		if columns > len(i): fl[n].extend(['']*(columns-len(i)))

	fw = len(fl[0][0] * columns) + (columns - 1)
	match columns:
		case 1: fltext = [align2(i[0], '^', fw) for i in fl]
		case 2: fltext = [f"{align2(i[0], '>', (fw//2)-1)}  {align2(i[1], '<', (fw//2)-1)}" for i in fl]
		case 3: fltext = [f"{align2(i[0], '>', (fw//2)-(len(i[1].replace(QHIT_CLR_ESC, ''))//2)-2)}  {i[1]}  {align2(i[2], '<', (fw//2)-(len(i[1].replace(QHIT_CLR_ESC, ''))//2)-2)}" for i in fl]
		case 4: fltext = [f"{align2(i[0], '>', (fw//2)-len(i[1].replace(QHIT_CLR_ESC, ''))-3)}  {i[1]}  {i[2]}  {align2(i[3], '<', (fw//2)-len(i[2].replace(QHIT_CLR_ESC, ''))-3)}" for i in fl]

	resp = gradient('\n'.join(fltext), direction, clrl, False, None, use_table, True)
	if align > 0:
		return padhit(resp, tw, None, align-1)
	return resp

def input_listen() -> str:
	"""WARNING: Still in development
	Cross-platform function to listen for key inputs, including [some] special keys."""
	if os.name == 'nt':
		import msvcrt
		key = msvcrt.getch()
		if key == b'\x18': return 'Exit'
		elif key == b'\r': return 'Enter'
		elif key == b'\x08': return 'Backspace'
		elif key in (b'\xe0', b'\x00'):
			special_key = msvcrt.getch()
			key_map = {
				b'H': 'Up',
				b'P': 'Down',
				b'K': 'Left',
				b'M': 'Right',
			}
			return key_map.get(special_key, f"Special-{special_key.hex()}")
		return key.decode('utf-8', errors='ignore')
	else:
		import tty
		import termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			key = sys.stdin.read(1)
			if ord(key) == 24: return 'Exit'
			elif key == '\x7f': return 'Backspace'
			elif key == '\r': return 'Enter'
			elif ord(key) == 27:  # Escape sequences for special keys
				seq = sys.stdin.read(2)  # Read the rest of the escape sequence
				key_map = {
					'[A': 'Up',
					'[B': 'Down',
					'[C': 'Right',
					'[D': 'Left',
				}
				return key_map.get(seq, f"Special-Escape-{seq}")
			return key
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def live_input(function: object, exit_char: str | None=None) -> None:
	"""WARNING: Still in development
	Listens for input and passes the captured character to the provided function.
	You can also specify a character to exit upon input
	(Also exits upon CTRL+X)"""
	while True:
		char = input_listen()
		if char == 'Exit' or (exit_char is not None and char == exit_char): break
		function(char)

class loading:
	def __init__(self, total: int, format: str='[\u2588\u258C\u2800]') -> None:
		self.total = total
		self.format = format
		self.done = 0
		self.max_len = 60 + (2*len(str(self.total)))

	def print_progress_bar(self) -> None:
		tw, th = os.get_terminal_size()
		percent = (100 / self.total) * self.done
		filled = int(percent // 2)
		print(f"\033[s\033[{th}A\r{self.format[0]}{self.format[1]*filled}{'' if percent >= 100 else (self.format[2] if percent % 2 >= 1 else self.format[3])}{self.format[3]*(50-filled-1)}{self.format[4]} {' ' if int(percent) < 10 else ''}{int(percent)}% [{str(self.done):>{len(str(self.total))}}/{self.total}]\033[1B\033[2K\033[u", end='', flush=True)

	def __enter__(self) -> object:
		cls()
		print('\033[2B', end='', flush=True)
		self.print_progress_bar()
		return self

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		cls()
		print(f"{self.format[0]}{self.format[1]*50}{self.format[4]} 100%", end='', flush=True)

	def __call__(self) -> None:
		self.done += 1
		self.print_progress_bar()

class multiload:
	def __init__(self, total: int, format='[\u2588\u258C\u2800]') -> None:
		self.bars = total
		self.done_bars = 0
		self.format = format

	def __enter__(self) -> object:
		cls()
		return self

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		cls()
		print(f"{self.format[0]}{self.format[1]*50}{self.format[4]} 100%\n"*self.bars, end='', flush=True)

	def __call__(self) -> None:
		self.done_bars += 1
		cls()
		print(f"{self.format[0]}{self.format[1]*50}{self.format[4]} 100%\n"*self.done_bars, end='', flush=True)

	class load:
		def __init__(self, parent: object, total: int) -> None:
			self.parent = parent
			self.total = total
			self.done = 0
			self.max_len = 60 + (2*len(str(self.total)))

		def print_progress_bar(self) -> None:
			tw, th, nl = os.get_terminal_size(), '\n'
			percent = (100 / self.total) * self.done
			filled, filler = int(percent // 2), ' '*(tw-57)
			print(f"\033[s\033[{th}A{f'{self.parent.format[0]}{self.parent.format[1]*50}{self.parent.format[4]} 100%{filler}{nl}'*self.parent.done_bars}\r{self.parent.format[0]}{self.parent.format[1]*filled}{'' if percent >= 100 else (self.parent.format[2] if percent % 2 >= 1 else self.parent.format[3])}{self.parent.format[3]*(50-filled-1)}{self.parent.format[4]} {' ' if int(percent) < 10 else ''}{int(percent)}% [{str(self.done):>{len(str(self.total))}}/{self.total}]\033[1B\033[2K\033[u", end='', flush=True)

		def __enter__(self) -> object:
			print('\033[2B', end='', flush=True)
			self.print_progress_bar()
			return self

		def __exit__(self, exc_type, exc_value, traceback) -> None:
			cls()
			print(f"{self.parent.format[0]}{self.parent.format[1]*50}{self.parent.format[4]} 100%", end='', flush=True)

		def __call__(self) -> None:
			self.done += 1
			self.print_progress_bar()

qhit_livetable_formats = [
	' ─│┼─│╭╮╰╯┼┤├┴┬',
	' -|+-|..**+||--'
]
class livetable:
	def __init__(self, rows: list | int, columns: list | int, borders: bool=True, grid: bool=False, right_to_left: bool=False, format: str | int=0, cw: int=0, rh: int=0, inner_align: str | None=None, *, auto_resize: bool=False, auto_wrap: bool=True, auto_fit: bool=True) -> None:
		if isinstance(rows, int):
			self.rows = ['' for _ in range(rows)]
		else:
			self.rows = rows

		if isinstance(columns, int):
			self.columns = ['' for _ in range(columns)]
		else:
			self.columns = columns[::-1] if right_to_left else columns
		self.progress = [0 for _ in self.columns]

		self.borders = borders
		self.grid = grid

		if isinstance(format, int):
			self.format = qhit_livetable_formats[format]
		else: self.format = format

		self.rtl = right_to_left

		colls = max(self.columns, key=lambda x: x.count('\n')).count('\n') + (0 if isinstance(columns, int) else 1)
		self.rh = rh if rh > 0 else (max(self.rows, key=lambda x: x.count('\n')).count('\n') + (0 if isinstance(rows, int) else 1))
		self.cw = cw if cw > 0 else (1 if colls == 0 else max([len(max(i.split('\n'), key=len)) for i in self.columns]))
		rowls = max([len(max(i.split('\n'), key=len)) for i in self.rows])

		labels = []
		if colls > 0:
			labeltxt = [i.split('\n') for i in self.columns]
			labels = [('' if not grid else self.format[2]).join([f'{j[-(i+1)]:{"<>"[right_to_left] if inner_align is None else inner_align}{self.cw}}'[:self.cw] if 0 <= i < len(j) else ' '*self.cw for j in labeltxt]) for i in range(colls)]

		main = []
		for rn, i in enumerate(self.rows):
			label = [f'{j:{"><"[right_to_left]}{rowls}}' for j in (i.split('\n') + ['']*self.rh)[:self.rh]] if rowls > 0 else ['']*self.rh
			tmp = ('' if not grid else self.format[2]).join([f"{self.format[0]:<{rowls}}" for _ in self.columns])
			tmp2 = ('' if not grid else self.format[2]).join([' '*rowls for _ in self.columns])

			for n in range(self.rh):
				if right_to_left:
					main.append(f"{'' if not borders else self.format[5]}{tmp if n == 0 else tmp2}{'' if not borders else self.format[5]}{label[n]}")
				else:
					main.append(f"{label[n]}{'' if not borders else self.format[5]}{tmp if n == 0 else tmp2}{'' if not borders else self.format[5]}")

			if grid and rn != len(self.rows)-1:
				tmp = self.format[3].join([self.format[1]*rowls for _ in self.columns])
				if right_to_left:
					main.append(f"{'' if not borders else self.format[12]}{tmp}{'' if not borders else self.format[10]}{self.format[1]*rowls}")
				else:
					main.append(f"{self.format[1]*rowls}{'' if not borders else self.format[10]}{tmp}{'' if not borders else self.format[11]}")

		self.frame = [
			*([f"{' ' if borders else ''}{i}{' ' if not grid or not borders else self.format[2]}{' '*rowls}" for i in labels] if right_to_left else
			[f"{' '*(rowls - int(not borders))}{' ' if not grid or not borders else self.format[2]}{i}" for i in labels]),
			*([] if not borders else
				[f"{self.format[6]}{('' if not grid else self.format[10]).join([self.format[4]*self.cw]*len(self.columns))}{self.format[7] if not grid else self.format[10] if rowls > 0 else self.format[11]}{(self.format[1] if grid else ' ')*rowls}"] if right_to_left else
				[f"{(self.format[1] if grid else ' ')*rowls}{self.format[6] if not grid else self.format[10] if rowls > 0 else self.format[12]}{('' if not grid else self.format[10]).join([self.format[4]*self.cw]*len(self.columns))}{self.format[7]}"]
			),
			*main,
			*([] if not borders else
				[f"{self.format[8]}{('' if not grid else self.format[13]).join([self.format[4]*self.cw]*len(self.columns))}{self.format[9]}{' '*rowls}"] if right_to_left else
				[f"{' '*rowls}{self.format[8]}{('' if not grid else self.format[13]).join([self.format[4]*self.cw]*len(self.columns))}{self.format[9]}"]
			)
		]

		self.coord = lambda x, y: ((lambda x, y: (
			int(borders) + ((self.cw + int(grid)) * (len(self.columns) - 1 - x)),
			colls + int(borders) + ((self.rh + int(grid)) * y)
		)) if right_to_left else (lambda x, y: (
			rowls + int(borders) + ((self.cw + int(grid)) * x),
			colls + int(borders) + ((self.rh + int(grid)) * y)
		)))(x, y) if 0 <= x < len(self.columns) and 0 <= y < len(self.rows) else None

		self.bottom = colls + int(borders * 2) + ((self.rh + int(grid)) * (len(self.columns)-1)) - int(grid)
		self.auto_wrap = auto_wrap
		self.auto_fit = auto_fit
		self.auto_resize = auto_resize

	def __enter__(self) -> object:
		self.size = os.get_terminal_size()
		cls()
		print('\n'.join([i[:self.size[0]] for i in self.frame[:self.size[1]]]))
		return self

	def __call__(self, x, y, *text) -> None:
		if self.auto_resize and self.size != os.get_terminal_size():
			self.size = os.get_terminal_size()
			cls()
			print('\n'.join([i[:self.size[0]] for i in self.frame[:self.size[1]]]))

		n, out = 0, ' '.join(text)
		if self.auto_wrap:
			for i in range(0, len(out), self.cw):
				c = self.coord(x, y)
				print(f"{pos(c[0], c[1]+n)}{out[i:i+self.cw]}", end='', flush=True)
				n += 1
				if self.auto_fit and n >= self.rh: break
		else:
			print(f"{pos(*self.coord(x, y))}{out[:self.cw] if self.auto_fit else out}", end='', flush=True)

	def __exit__(self, exc_type, exc_value, traceback):
		print(pos(0, self.bottom - 1))
		pass

import sys
import argparse

def qhit_color_list_arg_parser(iclrl: list[str]) -> str | list[tuple]:
	clrl = [eval(i) if i[0] in '([{' else i for i in iclrl]
	for i in clrl:
		if isinstance(i, str):
			return i
	return clrl

if len(sys.argv) > 1:
	root_parser = argparse.ArgumentParser(description="Python CLI tools")
	subparsers = root_parser.add_subparsers(dest="command", help="Sub-commands")
	subparsers.required = True

	parser = subparsers.add_parser('app', help='CLI application')
	parser.add_argument('name', type=str, help='Name')
	parser.add_argument('desc', type=str, help='Description')
	parser.add_argument('functions', nargs='+', help='Command list')
	parser.add_argument('--columns', type=int, default=1, help='Number of columns (default: 1)')
	parser.add_argument('--font', type=int, default=0, help='Font (default: 0)')
	parser.add_argument('--color', nargs='+', default='rainbow', help='Colour list (default: rainbow)')
	parser.add_argument('--gdir', type=int, default=1, help='Gradient direction (default: 1)')
	parser.add_argument('--delay', type=float, default=0.05, help='Delay (default: 0.05) lower = faster, but less accurate input, and vice versa.')
	parser.add_argument('--no-border', action="store_true", help='Remove border')
	parser.add_argument('--border', type=str, default='─│╭╮╰╯', help='Custom border symbols (default: "─│╭╮╰╯")')
	parser.add_argument('--no-clr-func', action="store_true", help='Dont colour functions')
	parser.add_argument('--index-clr', type=int, default=0, help='Index colour mode (default: 0)')
	parser.add_argument('--img', type=str, default='', help='QHIT image (default: "")')
	parser.add_argument('--table', action="store_true", help='Use colour table')
	parser.add_argument('--exit', action="store_true", help='Add exit function')

	parser = subparsers.add_parser('banner', help='Banner')
	parser.add_argument('text', type=str, help='Text')
	parser.add_argument('--align', type=int, default=0, help='Alignment (default: 0)')
	parser.add_argument('--left', action="store_true", help='Left Alignment')
	parser.add_argument('--center', action="store_true", help='Center Alignment')
	parser.add_argument('--right', action="store_true", help='Right Alignment')
	parser.add_argument('--font', type=int, default=0, help='Font (default: 0)')
	parser.add_argument('--img', type=str, default='', help='QHIT image (default: "")')
	parser.add_argument('--img-right', action="store_true", help='Aligns image on right')
	parser.add_argument('--color', nargs='+', default='', help='Gradient colour list (default: None)')
	parser.add_argument('--gdir', type=int, default=2, help='Gradient direction (default: 2)')
	parser.add_argument('--table', action="store_true", help='Use colour table')

	args = root_parser.parse_args()

	if args.command == 'app':
		func, tmp = [], []
		for i in args.functions:
			if i[0] == '*':
				func.append([i[1:], None])
				continue

			if len(tmp) >= 2:
				func.append(tmp)
				tmp = []
			tmp.append(i)
		func.append(tmp)
		func = [[i[0], i[1][1:], True] if i[1] is not None and i[1][0] == '!' else i for i in func]
		func = [[i[0], None if i[1] is None else lambda: os.system(i[1]), *i[2:]] for i in func]

		cli_app(func, args.columns, args.name, args.desc, args.font, qhit_color_list_arg_parser(args.color), args.gdir, args.delay, '' if args.no_border or not args.border else args.border, not args.no_clr_func, args.index_clr, None if not args.img else img(args.img), 1, args.table, args.exit)
	elif args.command == 'banner':
		resp = hit(args.text, args.font, img=None if not args.img else img(args.img), align_right=args.img_right)

		color = qhit_color_list_arg_parser(args.color)
		if color != '':
			resp = gradient(resp, args.gdir, color, use_table=args.table, auto_escape_ansi=True)

		align = args.align
		if args.left: align = 0
		if args.center: align = 1
		if args.right: align = 2

		if align != 0:
			resp = padhit(resp, os.get_terminal_size()[0], pad=align-1)
		print(resp)
