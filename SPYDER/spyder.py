#!/usr/bin/python3

import sys
import random

from argparse import ArgumentParser, FileType
from requests import get, Session
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from termcolor import colored

class Spider:
	def __init__(self):
		if __name__ == '__main__':
			self.session = Session()
			self.list = []

			self.args()
			if self.reach_host():
				print("-"* 69)
				print("""	 ____    ____   __   __  ____    _____   ____  
	/ ___|  |  _ \  \ \ / / |  _ \  | ____| |  _ \ 
	\___ \  | |_) |  \ V /  | | | | |  _|   | |_) |
	 ___) | |  __/    | |   | |_| | | |___  |  _ < 
	|____/  |_|       |_|   |____/  |_____| |_| \_\

			- Jack Prince (Insta - itz.jack.prince)""")
				print('-' * 69)
				print()
				self.spider(self.url)
				print('-' * 69)
				print("Finished.")
				print('-' * 69)
				print()
				exit(0)

	def args(self):
		parser = ArgumentParser(description="Recurrsive Web Spider.", usage="./%(prog)s [DOMAIN]")
		parser.add_argument(metavar="[DOMAIN]", dest="domain", help="Domain for automatic spidering.")
		parser.add_argument("-v", "--version", action="version", version="SPYDER: version: 1.0", help="Prints the current version.")
		parser.add_argument("-c", "--cookies", metavar="", help="Set custom cookies.")
		parser.add_argument("-o", "--output", metavar="", help="Output File.")
		parser.add_argument("--clean", action="store_true", help="Clean ouput.")
		self.args = parser.parse_args()

		if self.args.output:
			f = open(self.args.output, 'w')
			f.write('')
			f.close()

	def reach_host(self):
		try:
			r = get(f"http://{self.args.domain}", timeout=10)	
			if r.status_code == 200:
				self.url = r.url 
				return True
				
			else:
				return False

		except Exception as e:
			sys.stderr.write("[-] Unreachable Host.\n")
			exit()

	def request(self, url):
		try:
			if not self.args.cookies:
				html = self.session.get(url, allow_redirects=False, timeout=3)
			else:
				html = self.session.get(url, allow_redirects=False, timeout=3, headers={'cookies': self.args.cookies})
			return html.content

		except KeyboardInterrupt:
			exit()

	def spider(self, url):
		try:
			html = self.request(url)
			soup = BeautifulSoup(html, 'html.parser')

			for a in soup.find_all('a', href=True):
				link = urljoin(url, a['href'])

				if '#' in link:
					link = link.split('#')[0]

				if link not in self.list and self.args.domain in link:
					self.list.append(link)
					if self.args.clean:
						f = link.split("?")[0]
					else:
						f = link.split("#")[0]
					print("[+] {}".format(f))
					if not self.args.clean:
						print()
					if self.args.output:
						with open(self.args.output, 'a') as p:
							p.write(f + "\n\n")

					self.spider(link)

		except (KeyboardInterrupt, EOFError):
			print()
			exit()

		except Exception as e:
			pass

if __name__ == '__main__':
	Spider()