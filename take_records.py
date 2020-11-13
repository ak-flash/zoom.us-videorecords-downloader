import logging
logging.basicConfig(filename='downloader.log', format='%(asctime)s -  %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
import requests
import json
import os
import configparser
import time
import wget
from colorama import Fore, Back, Style
from colorama import init
init()


config = configparser.ConfigParser()
config.read('config.ini')

save_path = config["SAVE_FILE_PATH"]["path"] + '/'

for (each_key, each_val) in config.items("DATE"):
	if each_key == 'start':
		from_date = each_val[6:10] + '-' + each_val[3:5] + '-' + each_val[0:2]
	if each_key == 'end':
		to_date = each_val[6:10] + '-' + each_val[3:5] + '-' + each_val[0:2]

for (each_key, each_val) in config.items("ZOOM"):
	if each_key == 'jwt_token':		
		zoom_token = each_val
	
		
zoom_api_url = 'https://api.zoom.us'
headers = {'authorization': 'Bearer ' + zoom_token, 'content-type': 'application/json'}



try: 
	if not os.path.exists(save_path):
		os.mkdir(save_path)
except OSError as error: 
	print(error)	
	
def test_receive_conferences(zoom_login, date_start, date_end):
	url = zoom_api_url + '/v2/report/users/' + zoom_login + '/meetings?from=' + date_start +'&to=' + date_end
	response = requests.get(url, headers=headers)

	#print(response.json())
	
	
def receive_vrecords(zoom_login, date_start, date_end):
	
	url = zoom_api_url + '/v2/users/' + zoom_login + '/recordings?from=' + date_start +'&to=' + date_end
	response = requests.get(url, headers=headers)

	#print(response.json())	
	vrecords = json.loads(response.text)

	if vrecords.get('message') is None:
		if vrecords['total_records'] != 0:

			print(Fore.BLACK + Back.YELLOW + zoom_login + Style.RESET_ALL + ' ' + config["DATE"]["start"] + ' - ' + config["DATE"]["end"] + ' Конференций с видеозаписями: ' + str(vrecords['total_records']) + ' шт')	
			
			if not os.path.exists(save_path + zoom_login):
				os.mkdir(save_path + zoom_login)
			
			for meetings in vrecords['meetings']:
				
				print(Fore.BLACK + Back.WHITE + 'Начинаю скачивание файла из конференции ' + meetings['topic'] + Style.RESET_ALL)	
				
				for recording_file in meetings['recording_files']:
					
					if recording_file['file_type'] == 'MP4':

						print('Файл ' + str(recording_file['file_type']) + ' размером ' + str(round(recording_file['file_size']/1000000, 2)) + ' Мб')
						
						download_url_api = zoom_api_url + '/recording/download/' + recording_file['id'] + '?access_token=' + zoom_token
						#file_url = requests.get(download_url_api, allow_redirects=True)
						file_name =  save_path + zoom_login + '/' + recording_file['recording_start'][0:10] + ' ' + recording_file['recording_start'][11:13] + '-' + recording_file['recording_start'][14:16] + ' - '+ str(meetings['topic'].replace('"', "")) + ' - ' + str(recording_file['recording_type']) + '.mp4'
						#open(file_name, 'wb').write(file_url.content)
						wget.download(download_url_api, out=file_name)
						print('');
						print(Back.GREEN + 'Файл от ' + str(recording_file['recording_start'][0:10]) + ' ' + str(recording_file['recording_start'][11:13]) + ':' + str(recording_file['recording_start'][14:16]) + ' - загружен' + Style.RESET_ALL)
						
						logging.info(zoom_login + ': файл размером ' + str(round(recording_file['file_size']/1000000, 2)) + ' Мб от ' + str(recording_file['recording_start'][0:10]) + ' ' + str(recording_file['recording_start'][11:13]) + ':' + str(recording_file['recording_start'][14:16]) + ' ' + meetings['topic'])
						
						time.sleep(3)

		else:
			print('На логине ' + zoom_login + ' отсутствуют видеозаписи')
	else:
		print('Ошибка: ' + vrecords['message'])


if __name__ == '__main__':
	try:
		print(Fore.CYAN + 'Author: Andrey Klyausov 2020 ver.1' + Style.RESET_ALL)
		print('')
		for (each_key, each_val) in config.items("ZOOM_LOGIN"):
			if each_val == '1':
				#test_receive_conferences(each_key, from_date, to_date)
				receive_vrecords(each_key, from_date, to_date)
	except BaseException:
		import sys
		print(sys.exc_info()[0])
		import traceback
		print(traceback.format_exc())
	finally:
		print("Press Enter to close ...")
		input()