import smtplib
from random import randint

def send(content, email):
	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()
	mail.login('mentorkyrgyzstan@gmail.com', 'Success99')
	mail.sendmail('mentorkyrgyzstan@gmail.com', 'talantbekov_k@auca.kg',content)	
	mail.close()
	
def get_code():
	code = ""
	while(len(code) != 5):
		code = code + str(randint(1, 9))
	return code	