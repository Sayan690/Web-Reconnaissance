#!/usr/bin/python3

import sys
import time
import socket

from argparse import ArgumentParser, FileType
from requests import *
from threading import Thread

class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

class Disturb:
	def __init__(self):
		self.type = []
		self.count = 1
		self.headers = Vividict()
		self.subdomains = []
		self.args()
		self.reach_host()
		self.words = self.prepare_words()
		self.st = time.time()
		print("-" * 69)
		print(""" 
 ____    _   _   ____    ____    ___   ____    _____   _   _   ____    ____  
/ ___|  | | | | | __ )  |  _ \  |_ _| / ___|  |_   _| | | | | |  _ \  | __ ) 
\___ \  | | | | |  _ \  | | | |  | |  \___ \    | |   | | | | | |_) | |  _ \ 
 ___) | | |_| | | |_) | | |_| |  | |   ___) |   | |   | |_| | |  _ <  | |_) |
|____/   \___/  |____/  |____/  |___| |____/    |_|    \___/  |_| \_\ |____/
					
					- Jack Prince (Insta - itz.jack.98)""")
		print("-" * 69)
		print()
		self.prepare_threads()
		self.end = time.time()
		print(f"\n[+] Sub-domains found: {len(self.subdomains)}")
		print(f"[+] Time Taken: {round(self.end-self.st, 2)}s.")

	def args(self):
		parser = ArgumentParser(description="Sub-domain brute forcer.", usage="./%(prog)s domain -w [wordlist]")
		parser.add_argument(metavar="domain", help="Domain for brute forcing.", dest="domain")
		parser.add_argument("-v", "--version", action="version", version="subdisturb: version: 1.0", help="Prints the current version.")
		parser.add_argument("-w", "--wordlist", metavar="", help="Wordlist for brute forcing.", type=FileType("r"), required=True)
		parser.add_argument("-c", "--cookies", metavar="", help="Set custom cookies.")
		parser.add_argument("-t", "--threads", metavar="", help="Threads to use. (default - 100)", type=int, default=100)
		parser.add_argument("-o", "--output", metavar="", help="Output File.", type=FileType("w"))
		self.args = parser.parse_args()

		if self.args.cookies:
			self.headers['cookie'] = self.args.cookies

		self.headers['User-Agent'] = 'Macintosh Mac OS X'

	def reach_host(self):
		try:
			if not "http" in self.args.domain:
				r = get(f"http://{self.args.domain}", headers=self.headers, timeout=5)

			else:
				r = get(self.args.domain)

			if r.status_code == 200:
				self.type.append(r.url.split("://"))
				return True

			else:
				return False
		except:
			sys.stderr.write("[-] Unreachable host.")
			exit()

	def prepare_words(self):
		words = self.args.wordlist.read().split()
		for word in words:
			if word[-1] == ".":
				word = word[:-1]

			if "#" not in word:
				yield word

	def prepare_threads(self):
		try:
			thread_list = []
			for _ in range(self.args.threads+1):
				thread_list.append(Thread(target=self.main))

			for self.threads in thread_list:
				self.threads.start()

			for self.threads in thread_list:
				self.threads.join()

		except (KeyboardInterrupt, EOFError):
			exit()

	def main(self):
		while True:
			try:
				word = (next(self.words)).lower()
				url = f"{self.type[0][0]}://{word}.{self.args.domain}"
				self.count += 1
				print(f"\r[+] Progress: {self.count}", end="")
				self.r = get(url, headers=self.headers, timeout=3)
				if self.r.status_code == 200:
					self.subdomains.append(url)
					print(f"\r[+] {url}")
					if self.args.output:
						with open(self.args.wordlist.name, 'a') as f:
							f.write(f"{url}\n")

			except (exceptions.ConnectionError, exceptions.ReadTimeout, ValueError, socket.timeout):
				continue

			except (StopIteration, KeyboardInterrupt, EOFError):
				break

if __name__ == '__main__':
	Disturb()
