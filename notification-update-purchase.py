import requests
import json
import os.path
from twilio.rest import Client
import json, random, sys, urllib.request, smtplib
from email.message import EmailMessage

code = 'NL848*114**BR' # Alterar código de Rastreio.

def SMTP(track, content):
	try:
		msg = EmailMessage()

		msg['Subject'] = "Atualização na sua compra "+track
		msg['From'] = 'Rastreio Aliexpress <>' # <email@gmail.com>
		msg['To'] = '' # email@gmail.com
		msg.set_content(content)
		mailserver = smtplib.SMTP('smtp-mail.outlook.com', 587) # Outlook SMTP Server
		mailserver.connect('smtp-mail.outlook.com', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('', '')
		mailserver.sendmail(msg['From'], [msg['To']], msg.as_string())
		mailserver.quit()

	except Exception as error:
		print(f"ERRO: {str(error)}")


def SMPP(content):
    account_sid = '' # Twilio Acc SID
    auth_token = '' # Twilio Acc Token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+12512202285', #Twilio From Number
    body=content,
    to='+55' #Seu numero
    )

    print(message.sid)



def check_last_update(track, carrier_note):
    file_path = r'C:\Users\andre\Downloads\envios.log'
    fl = r'C:\Users\andre\Downloads\envios.log'
    fl_read = open(fl, 'r').readlines()
    if (os.path.isfile(file_path) == True) :
        with open(file_path, 'a+', encoding='utf-8') as fl:
            if carrier_note+'\n' in fl_read:
                print('Already exists')
                return True

            else:
                fl.write(carrier_note+'\n')
                fl.close()
                return False




def Tracking_order(track):
    r = requests.get('https://global.cainiao.com/global/detail.json?mailNos={}&lang=en-US&language=en-US'.format(track))
    json_data = r.json()
    _json = json_data['module'][0]['detailList']
    try:
        for i in _json:
            banner = '''
Atualização: {}
Código de Rastreio: {}
Origem: {}
Destino: {}
Status: {}
Carrier Note: {}
Hora: {}
            '''.format(i['desc'],json_data['module'][0]['mailNo'],json_data['module'][0]['originCountry'],json_data['module'][0]['destCountry'],json_data['module'][0]['status'], i['standerdDesc'],i['timeStr'])
            print('')
            print(banner)
            carrier_note = i['standerdDesc']
            chk = check_last_update(code,carrier_note)
            print(chk)
            if chk == False:
                 SMTP(code,banner)
                 SMPP(banner)
                 print('')
    except Exception as e:
        print('Error: '.format(e))


Tracking_order(code)
