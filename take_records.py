import requests
import json
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

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


def receive_conferences(zoom_login, date_start, date_end):
	url = zoom_api_url + '/v2/report/users/' + zoom_login + '/meetings?from=' + date_start +'&to=' + date_end
	response = requests.get(url, headers=headers)

	print(response.json())

def receive_vrecords(zoom_login, date_start, date_end):
	url = zoom_api_url + '/v2/users/' + zoom_login + '/recordings?from=' + date_start +'&to=' + date_end
	response = requests.get(url, headers=headers)

	#print(response.json())	
	vrecords = json.loads(response.text)

	if vrecords.get('message') is None:
		if vrecords['total_records'] != 0:
			print(zoom_login + ' - Всего конференций с видеозаписями: ' + str(vrecords['total_records']) + ' шт')	
			
			if not os.path.exists(zoom_login):
				os.mkdir(zoom_login)
			
			for meetings in vrecords['meetings']:
				print('Начинаю скачивание файла из конференции ' + meetings['topic'])

				for recording_file in meetings['recording_files']:
					
					if recording_file['file_type'] == 'MP4':
						
						print('Файл ' + str(recording_file['file_type']) + ' размером ' + str(round(recording_file['file_size']/1000000, 2)) + ' Мб')
						
						download_url_api = zoom_api_url + '/recording/download/' + recording_file['id'] + '?access_token=' + zoom_token
						file_url = requests.get(download_url_api, allow_redirects=True)
						file_name =  zoom_login + '/' + recording_file['recording_start'][0:10] + ' ' + recording_file['recording_start'][11:13] + '-' + recording_file['recording_start'][14:16] + ' - '+ str(meetings['topic']) + '.mp4'
						open(file_name, 'wb').write(file_url.content)
						print('Файл от ' + str(recording_file['recording_start'][0:10]) + ' ' + str(recording_file['recording_start'][11:13]) + ':' + str(recording_file['recording_start'][14:16]) + ' - загружен')
		else:
			print('На логине ' + zoom_login + ' отсутствуют видеозаписи')
	else:
		print('Ошибка: ' + vrecords['message'])


for (each_key, each_val) in config.items("ZOOM_LOGIN"):
	if each_val == '1':
		receive_vrecords(each_key, from_date, to_date)