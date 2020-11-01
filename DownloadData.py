import csv
import json
import pathlib
import pytz
import requests
import os

from datetime import date, datetime, timedelta
import urllib3
import uuid

def getLocalTime():
    currentTime = datetime.now(pytz.utc)+timedelta(hours=7)
    return currentTime

def createTeamCSVFile(jsonContent, updateDate):
    updateDate=updateDate+timedelta(hours=-1)
    fileName = "Team_"+updateDate.strftime("%Y%m%d_%H")
    updateDateStr=updateDate.strftime("%Y-%m-%d %H:00")
    data = json.loads(jsonContent)['body']['results']

    count = 0;
    data_file = open('data/'+fileName + '.csv', 'w', encoding="utf-8-sig",newline='')
    total_file = open('data/Summary.csv', 'a', encoding="utf-8-sig",newline='')
    csv_writer = csv.writer(data_file)
    total_writer = csv.writer(total_file)

    for team in data:
        team['updatedate'] = updateDateStr
        if count == 0:
            header = "id, ten, soVanDongVien, quangDuong, thoiGian, updatedate"

            csv_writer.writerow([header])

        csv_writer.writerow([team['id'] ,team['runDoi']['ten'], team['soVanDongVien'], team['quangDuong'], team['thoiGian'], updateDateStr])
        total_writer.writerow([team['id'] ,team['runDoi']['ten'], team['soVanDongVien'], team['quangDuong'], team['thoiGian'], updateDateStr])
        count += 1
        if count > 19:
            break;
def IsInterestedHour(currenttTime):
    if (currenttTime.hour in (1,9,17)):
        return True
    else:
        return False

def DownloadTeamData():
    currentTime = getLocalTime()
    if (IsInterestedHour(currentTime))==False:
        print ("Skip this hour")
        return

    requestId=uuid.uuid4().hex

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Content-Type': 'application/json',
        'Origin': 'https://bidvrun.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://bidvrun.com/home/ranking-team/team/1/other-team',
        'Accept-Language': 'vi,en;q=0.9,en-US;q=0.8',
    }

    data = '{"body":{"content":{"bidvrunBody":{},"bidvrunHeaders":{"Content-Type":"application/json","Authorization":""},"method":"GET","uri":"/api/run/run_doi_giaichay?runGiaichayId=1&runDoiDoibidv=false&orderBy=xepHangBidv&queryOffset=1&queryLimit=50"}},"header":{"appToken":"eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJCSURWQVBJIiwiYXBwaWQiOjQzNSwiY2xpZW50aWQiOjIsInBsYW5pZCI6NDM0fQ.1JW3nQq6c3osVIxIY3vMVJcPTiw2JW7pvxV6ITI2wkHL0iaZ0vJFH7llRJThzwMeOSoCx7_K9KJjD0iytyUHLg","custToken":"","checksum":"icgcMBBgZxsXlVhA8QsAgaT3mw+yHKDbuEw9nVUfvvQ=","requestID":"'+requestId+'","aurthUrl":"11"}}'

    response = requests.post('https://bidvrun.com/bidvrunapiapp/global/vn/bidvrun/forward_unauth/v1', headers=headers, data=data, verify=False)

    createTeamCSVFile(response.content, currentTime)
    
print ('Downloading Team Data')
DownloadTeamData()
print ('Completed downloading')

