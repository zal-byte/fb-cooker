import mechanize, sys, requests
from bs4 import BeautifulSoup as BS

class Cooker(object):
	url_login = "https://m.facebook.com"
	b_0 = None
	c_0 = None
	def __init__(self):		
		self.b_sub = ""
		self.b_0 = mechanize.Browser()
		self.c_0 = mechanize.LWPCookieJar()
		self.b_0.set_cookiejar(self.c_0)
		self.b_0.set_handle_equiv(True)
		self.b_0.set_handle_redirect(True)
		self.b_0.set_handle_referer(True)
		self.b_0.set_handle_robots(False)
		self.b_0.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
		
		self.b_0.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1')]

	def login(self, user, passwd):
		self.b_0.open(self.url_login + "/login.php")
		self.b_0.select_form(nr=0)
		self.b_0.form['email'] = user
		self.b_0.form['pass'] = passwd

		self.b_sub = self.b_0.submit()

		bs = BS(self.b_sub.get_data(), 'html5lib')
		print(bs.title.string)
		if self.b_sub.get_data().__contains__(b'home_icon'):
			return 1
		elif 'checkpoint' in self.b_sub.geturl():
			return 2
		return 0

	def resCode(self, code):
		bs = BS(self.b_sub.get_data(), 'html5lib')
		if code:
			#loged successfuly
			print("[ * ] "+str(bs.title.string) + " [ * ]")
			print("[ * ] "+str(self.b_sub.geturl()) + " [ * ]")
			print("[ + ] Login Successfuly")
			if code == 2:
				#Checkpoint
				print("--- [ ! ] But has checkpoint")
			else:
				return 1
			return 0
		else:
			#Unsuccessfuly
			print("[ ! ] Login Unsuccessfuly")

	def cooker(self):
		c_cook = self.b_0._ua_handlers['_cookies'].cookiejar
		cookie_dict = {}
		for c in c_cook:
			cookie_dict[c.name] = c.value
		return cookie_dict

	def cookie_save(self):
		c_cook = self.b_0._ua_handlers['_cookies'].cookiejar
		sexo = ""
		for c in c_cook:
			sexo += c.name + "=" + c.value + ";"
		fuero = open("cook_00.coi", "w")
		fuero.write(sexo)
		fuero.close()

	def verify(self, code):
		self.b_0.open("https://mbasic.facebook.com/login/checkpoint")
		self.b_0.select_form(nr=0)
		self.b_0.set_all_readonly(False)
		self.b_0.form['approvals_code'] = str(code)

		b_c = self.b_0.submit()
		bs = BS(b_c.get_data(), 'html5lib')
		print("[ * ] " + bs.title.string + " | Verify")
		if b_c.get_data().__contains__(b'save_device'):
			self.save_device()
		else:
			print("Verify error")

	def save_device(self):
		self.b_0.open("https://mbasic.facebook.com/login/checkpoint")
		self.b_0.select_form(nr=0)
		self.b_0.set_all_readonly(False)
		self.b_0.form['name_action_selected'] = ["dont_save",]

		b_d = self.b_0.submit()
		bs = BS(b_d.get_data(), 'html5lib')
		print("[ * ] " + bs.title.string )
		# print("save_device() : "+str(b_d.geturl()))
		self.home()

	def home(self):
		r = requests.get('https://mbasic.facebook.com/home.php', cookies=self.cooker())
		bs = BS(r.text, 'html5lib')
		print("[ * ] " + bs.title.string)

def banner():
	ban = """
	Facebook Cooker ( Cookie )
	Creator : zal-byte
	Github : zal-byte
	"""
	return ban

usernames = ""
passwords = ""


def main():
	Cook = Cooker()
	resCode = Cook.login(usernames, passwords)
	
	ret = Cook.resCode( resCode )
	if ret == 0:
		print("Input code ?")
		wh = input("Do you want to input code verification ? (y/n) > ")
		if wh.lower() == "y":
			code = input("Verify Code > ")
			cose = Cook.verify(code)

	elif ret == 1:
		#????????????/
		print("Save cookies ? (y/n) ")
		wh = input("Do you want to save the cookies ? > ")
		if wh.lower() == "y":
			print("SS")



def preload():
	global usernames, passwords
	print(banner())

	usernames += input("Username : ")
	passwords += input("Password : ")



	if usernames != None or usernames != "":
		if passwords != None or passwords != "":
			main()
		else:
			print("Password...... (?)")
	else:
		print("Username....... (?)")

if __name__ == "__main__":
	preload()