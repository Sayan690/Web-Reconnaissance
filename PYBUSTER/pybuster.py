#!/usr/bin/python3

import sys

from argparse import *
from requests import *
from threading import *

class Vividict(dict):
	"""return --> dict
	
	function --> makes entry for arbitrary keys and their values in the dictionary.

	"""

	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

class PyBuster:
	def __init__(self):
		if __name__ == "__main__":
			self.extensions = []
			self.status_codes = []
			self.codes = ["[+] Negative status codes: ", 404, ', ', 403, ', ']
			self.agent = "Macintosh Mac OS X"
			self.count = 0

			self.headers = Vividict()
			self.words = self.prepare_words()
			
			self.args()
			self.reach_host()
			self.print_format()
			self.prepare_threads()
			self.endl()

	def args(self):

		# Parsing command line arguments by the argparse library.

		parser = ArgumentParser(description="Web directory brute forcer.", usage="./%(prog)s -u [URL] -w [WORDLIST]")
		parser.add_argument("-V", "--version", action="version", version="PyBuster: version: 1.0", help="Prints the current version.")
		parser.add_argument(metavar="[URL]", help="Url of the website.", dest="url")
		parser.add_argument("-w", "--wordlist", metavar="", help="Wordlist for brute forcing.", type=FileType("r"), required=True)
		parser.add_argument("-H", "--headers", metavar="", help="Custom Headers.")
		parser.add_argument("-c", "--cookies", metavar="", help="Set custom cookies.")
		parser.add_argument("-a", "--user-agent", dest="agent", metavar="", help="Set custom user agent.")
		parser.add_argument("-t", "--threads", metavar="", help="Threads to use. (default - 50)", type=int, default=50)
		parser.add_argument("-r", "--allow-redirect", action="store_true", help="Allows redirection.", dest="allow")
		parser.add_argument("-T", "--timeout", metavar="", help="Timeout in seconds. (default - 5)", type=int, default=5)
		parser.add_argument("-b", "--blacklist", metavar="", help="Blacklist status codes. (default - 404)", type=int, nargs="+", dest="codes")
		parser.add_argument("--auth", action="store_true", help="HTTP authentication.")
		parser.add_argument("--user", metavar="", help="Username for authentication.")
		parser.add_argument("--pass", metavar="", help="Password for authentication.", dest="passwd")
		parser.add_argument("-x", "--extensions", metavar="", help="Extensions to use.", nargs="+")
		self.args = parser.parse_args()
		self.basic_correction()

	def basic_correction(self):

		# Basic correction of the arguments.

		if self.args.auth:
			if not self.args.user or not self.args.passwd:
				sys.stderr.write("[-] Please specify username and password for authentication.\n")
				exit()

		if self.args.user or self.args.passwd:
			if not self.args.auth:
				sys.stderr.write("[-] Please specify '--auth' switch for authenticating.\n")
				exit()

		if self.args.headers:
			if "User-Agent" in self.args.headers:
				sys.stderr.write("[-] For User-Agent, we have a particular switch. Please use it instead.\n")
				exit()

			if "cookie" in self.args.headers or "Cookie" in self.args.headers:
				sys.stderr.write("[-] For cookies, we have a particular switch. Please use it instead.\n")
				exit()

			if self.args.headers.count(':') > 1:
				sys.stderr.write("[-] Sorry, only one header is accepted in this version.\n")
				exit()

			if ":" not in self.args.headers:
				sys.stderr.write("[-] Wrong headers.")
				sys.exit()

			headers = self.args.headers.split(":")
			
			if headers[0][-1] == ' ':
				headers[0] = headers[0][:-1]

			if headers[1][0] == ' ':
				headers[1] = headers[1][1:]

			for i in range(0, len(headers)-1):
				self.headers[headers[i]] = headers[i+1]

		if self.args.extensions:
			self.check_extensions()

		if self.args.agent:
			self.headers['User-Agent'] = self.args.agent

		else:
			self.headers['User-Agent'] = self.agent

		if self.args.cookies:
			self.headers['cookie'] = self.args.cookies

	def check_extensions(self):

		# Prints the extensions in correct format and also appends the extensions to self.extensions.

		for i in self.args.extensions:
			if i[0] != ".":
				ext = f".{i}"

			else:
				ext = i

			if "," in ext:
				if " " not in ext and ext[-1] != " ":
					l = ext.replace(",", " ").split(" ")
					for i in l:
						p = i

						if p not in self.extensions:
							if p != "" and p[-1] == " ":
								self.extensions.append(p[:-1])

							else:
								self.extensions.append(p)
						
				else:
					p = ext.replace(",", "")

			elif " " in ext:
				p = ext.replace(" ", "")

			else:
				p = ext
			
			if p not in self.extensions:
				if p != "" and p[-1] == " ":
					self.extensions.append(p[:-1])

				else:
					self.extensions.append(p)
		_ = self.extensions
		self.extensions = []
		for f in _:
			if f != "":
				self.extensions.append(f)

		for i in range(0, len(self.extensions)):

			if self.extensions[i][0] != ".":
				self.extensions[i] = f".{self.extensions[i]}"

	def prepare_words(self):

		# Generator function for the words.

		words = self.args.wordlist.read().split()
		for word in words:
			yield word

	def print_format(self):

		# Prints the format of PyBuster.

		print("-" * 50)
		print("PyBuster Version: 1.0")
		print("by Jack Prince (Insta - itz.jack.98).")
		print("-" * 50)
		print("[+] Url: {}".format(self.args.url))
		print("[+] Wordlist: {}".format(self.args.wordlist.name))
		print("[+] Threads: {}".format(self.args.threads))

		if self.args.codes:

			for i in self.args.codes:

				if not i == 404:
					self.codes.append(i)
					self.codes.append(", ")

		for i in self.codes:
			try:
				code = int(i)
				self.status_codes.append(code)
			except (TypeError, ValueError):
				continue

		for letters in self.codes[:-1]:
			print(letters, end="")
		print("\n[+] User-Agent: {}".format(self.agent))
		print("[+] Timeout: {}s".format(self.args.timeout))
		if len(self.extensions) > 0:
			extensions = ["[+] Extensions: "]
			for ext in self.extensions:
				extensions.append(ext)
				extensions.append(", ")

			for letters in extensions[:-1]:
				if letters != ", " and "[" not in letters:
					print(letters[1:], end="")

				else:
					print(letters, end="")
			print()
		print("-" * 50)
		print("Staring PyBuster...")
		print("-" * 50)
		print()

	def reach_host(self):

		# Checks that connection to the host is possible.

		try:
			if "http" not in self.args.url:
				if not self.args.auth:
					r = get(f"http://{self.args.url}", headers=self.headers, allow_redirects=True, timeout=self.args.timeout)
				else:
					r = get(f"http://{self.args.url}", headers=self.headers, allow_redirects=True, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))
				if r.url[-1] == "/":
 					self.url = r.url

				else:
 					self.url = r.url + "/"

			else:
				if self.args.url[-1] == "/":
 					self.url = self.args.url
 					if not self.args.auth:
 						r = get(self.args.url, headers=self.headers, allow_redirects=True, timeout=self.args.timeout)
 					else:
 						r = get(self.args.url, headers=self.headers, allow_redirects=True, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))
				else:
 					self.url = self.args.url + "/"
 					if not self.args.auth:
 						r = get(self.args.url, headers=self.headers, allow_redirects=True, timeout=self.args.timeout)
 					else:
 						r = get(self.args.url, headers=self.headers, allow_redirects=True, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))

		except (exceptions.ConnectionError, exceptions.ReadTimeout):
			sys.stderr.write("[-] Unreachable host or host needs authentication.\n")
			exit()

	def request(self):

		# Prints the found url(s) and also their status codes.

		if self.r.status_code not in self.status_codes:
			if self.r.url != self.url:
				if len(self.r.url) <= 31:
					print("\r"+self.r.url + f"\t\t\t\t\t\t\tStatus: {self.r.status_code}")

				elif len(self.r.url) > 31 and len(self.r.url) <= 38:
					print("\r"+self.r.url + f"\t\t\t\t\t\tStatus: {self.r.status_code}")
				elif len(self.r.url) > 40:
					print("\r"+self.r.url + f"\t\t\t\t\tStatus: {self.r.status_code}")
				elif len(self.r.url) > 50:
					print("\r"+self.r.url + f"\t\t\t\tStatus: {self.r.status_code}")
				else:
					print("\r"+self.r.url + f"\t\t\t\t\t\tStatus: {self.r.status_code}")

		elif self.r.status_code == 401:
			sys.stderr.write("[-] Webpage requires authentication.\n")
			exit()

	def main(self):
		# Main method that requests the website and finds the web directories.

		while True:
			try:
				self.word = next(self.words)
				word = self.word

				self.count += 1
				print(f"\rProgress: {self.count}", end="")

				if len(self.extensions) > 0:
					for i in self.extensions:
						self.word += i
						if self.args.allow:
							if not self.args.auth:
								self.r = get(self.url + self.word, headers=self.headers, allow_redirects=True, timeout=self.args.timeout)
							else:
								self.r = get(self.url + self.word, headers=self.headers, allow_redirects=True, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))
						else:
							if not self.args.auth:
								self.r = get(self.url + self.word, headers=self.headers, allow_redirects=False, timeout=self.args.timeout)
							else:
								self.r = get(self.url + self.word, headers=self.headers, allow_redirects=False, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))

						self.request()
						self.word = word

				if self.args.allow:
					if not self.args.auth:
						self.r = get(self.url + self.word, headers=self.headers, allow_redirects=True, timeout=self.args.timeout)
					else:
						self.r = get(self.url + self.word, headers=self.headers, allow_redirects=True, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))
				else:
					if not self.args.auth:
						self.r = get(self.url + self.word, headers=self.headers, allow_redirects=False, timeout=self.args.timeout)
					else:
						self.r = get(self.url + self.word, headers=self.headers, allow_redirects=False, timeout=self.args.timeout, auth=(self.args.user, self.args.passwd))
				self.request()

			except (exceptions.ConnectionError, exceptions.ReadTimeout, ValueError):
				continue

			except (StopIteration, KeyboardInterrupt, EOFError):
				break
				sys.exit()

	def prepare_threads(self):

		# Prepares the threads for working.

		try:
			thread_list = []

			for _ in range(self.args.threads+1):
				thread = Thread(target=self.main)
				thread_list.append(thread)

			for self.threads in thread_list:
				self.threads.start()

			for self.threads in thread_list:
				self.threads.join()
		except (KeyboardInterrupt, EOFError):
			self.endl()
			sys.exit()

	def endl(self):

		# Prints the ending format of the tool.

		print("\n")
		print("-" * 50)
		print("[+] Finished.")
		print("-" * 50)
		sys.exit()

if __name__ == "__main__":

	# Calling the made class.

	PyBuster()