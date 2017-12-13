import smtplib
from random import randint

def send(content, email):
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login('akmatbek_u@auca.kg', 'E123456e')
	mail.sendmail('akmatbek_u@auca.kg', email ,content)	
	mail.close()
	
def get_code():
	code = ""
	while(len(code) != 5):
		code = code + str(randint(1, 9))
	return code	