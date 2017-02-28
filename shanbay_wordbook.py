#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re, math, urllib.parse, requests, time
from urllib import request
from bs4 import BeautifulSoup
from subprocess import call as shell

userid = 12345678
bookid = 1366

cookie_jar = requests.cookies.RequestsCookieJar()
cookie_jar.set('userid', str(userid))
book_uri = '/wordbook/%d' % bookid
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}

def get_resp(sess, uri):
	# url = 'https://www.shanbay.com/api/v1/account/login/web/'
	# s.put(url, {'username': " ", 'password': ""}, headers=header)
	url = 'https://www.shanbay.com' + uri
	resp = sess.get(url, headers=headers, cookies=cookie_jar)
	return resp.text

def get_units(s, book_uri):
	resp = get_resp(s, book_uri)
	soup = BeautifulSoup(resp, 'html.parser')
	div = soup.find('div', id='wordbook-wordlist-container').find_all('div', id='wordlist-')
	size = len(div)
	all_units = []
	for i in range( size ):
		tr = div[i].find('tr')
		info = {
			'uri': tr.a['href'],
			'name': tr.find('a').get_text().replace(' ', '_'),
			'cnt': tr.get_text().rstrip(' \n').split('：')[1]
		}
		all_units.append( info )
	return all_units

def filter_words(resp):
	soup = BeautifulSoup(resp, 'html.parser')
	table = soup.find('table', class_='table table-bordered table-striped').find('tbody').find_all('tr')
	size = len(table)
	words = [''] * size
	for i in range(size):
		words[i] = table[i].get_text().lstrip('\n').rstrip('\n').split('\n')
	return words

def get_words_of_unit(s, unit):
	page = math.ceil( int(unit['cnt']) / 20 )
	words = []
	for i in range(page):
		uri = unit['uri'] + '?page=%d' % (i+1)
		resp = get_resp(s, uri)
		words_Of_each_page = filter_words(resp)
		for word in words_Of_each_page:
			words.append( word )
	return words

def init_filename(filename):
	shell("cat blank.mp3 > _" + filename + ".mp3", shell=True)

def get_en_audio(word):
	url = 'https://media-audio1.baydn.com/us/'
	url += word[0] + '/' + word[0:2] + '/' + word + '_v3.mp3'
	try:
		request.urlretrieve(url, 'en.mp3')
		shell('avconv -i en.mp3 -f mp3 -ab 128k -ar 44100 -ac 2 -y -v quiet _en.mp3', shell=True)
		return 1
	except:
		return 0

def get_cn_audio(word):
	url = 'http://fanyi.baidu.com/gettts?lan=zh&text='
	url += urllib.parse.quote(word) + '&spd=5&source=web'
	try:
		request.urlretrieve(url, 'cn.mp3')
		shell('avconv -i cn.mp3 -f mp3 -ab 128k -ar 44100 -ac 2 -y -v quiet _cn.mp3', shell=True)
		return 1
	except:
		return 0

def get_audio(word, filename):
	has_en, has_cn = 1, 1
	word_en = word[0]
	word_cn = word[1].split('.')[-1].replace('...', '什么什么')
	has_en = get_en_audio(word_en)
	has_cn = get_cn_audio(word_cn)
	time.sleep(3)
	if has_en and has_cn:
		shell("cat _en.mp3 _cn.mp3 blank.mp3 >> _" + filename + ".mp3", shell=True)
		# shell("cat _en.mp3 blank.mp3 >> _" + filename + ".mp3", shell=True)
		return 1
	else:
		return 0

def get_text(word, filename):
	filename += '.csv'
	with open(filename, 'a') as f:
		en = word[0]
		cn = word[1]
		f.write(en+'\t'+cn+'\n')

def main():
	s = requests.Session()
	resp = get_resp(s, book_uri)
	all_units = get_units( s, book_uri )
	for i in range( len(all_units) ):
		print(all_units[i]['name'], '\n')
		words_of_unit = get_words_of_unit( s, all_units[i] )
		unit_name = all_units[i]['name']
		init_filename( unit_name )
		for i in range( len(words_of_unit) ):
			print(words_of_unit[i][0])
			get_audio(words_of_unit[i], unit_name)

if __name__ == '__main__':
	main()

