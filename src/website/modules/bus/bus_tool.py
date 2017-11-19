# -*- coding: utf-8 -*-
"""
Created on Mon May 08 22:21:49 2017

@author: James
"""

import requests
import json

URL = "http://ikuass.kuas.edu.tw/"


class ikuasbus:
    def __init__(self, date):
        url = URL + "Bus/GetTimetable"
        payload = {
                "apiKey": "87vGou@pHO9nhk2",
                "drivedate": date
                }
        r = requests.post(url, data=payload)
        r = r.text
        self.data = json.loads(r)

    def get_busid(self, n):
        return self.data['data'][n]['busId']

    def get_driveTime(self, n):
        return self.data['data'][n]['driveTime']

    def get_startStation(self, n):
        return self.data['data'][n]['startStation']

    def get_endStation(self, n):
        return self.data['data'][n]['endStation']

    def get_specialBus(self, n):
        return self.data['data'][n]['specialBus']

    def get_specialMsg(self, n):
        return self.data['data'][n]['specialMsg']

    def get_limitCount(self, n):
        return self.data['data'][n]['limitCount']

    def get_resEnable(self, n):
        return self.data['data'][n]['resEnable']

    def get_resCode(self, n):
        return self.data['data'][n]['resCode']

    def get_resName(self, n):
        return self.data['data'][n]['resName']

    def get_datalen(self):
        return len(self.data['data'])


class ikuaslogin:
    def __init__(self, userId, userPw):
        url = URL + 'User/DoLogin'
        payload = {
                "apiKey": "87vGou@pHO9nhk2",
                "userId": userId,
                "userPw": userPw,
                "userKeep": "0"
                }
        r = requests.post(url, data=payload)
        r = r.text
        self.data = json.loads(r)
        self.Id = userId
        self.Pw = userPw

    def get_userKey(self):
        return self.data['data']['userKey']

    def get_userName(self):
        return self.data['data']['userName']

    def get_userEmail(self):
        return self.data['data']['userEmail']

    def get_userMobile(self):
        return self.data['data']['userMobile']


class ikuasset:
    def __init__(self, userName, userKey):

        self.Tf = None
        self.Ans = None
        self.Name = userName
        self.Key = userKey

    def busset(self, busid):
        url = 'http://ikuass.kuas.edu.tw/Bus/CreateUserReserve'
        # API URL  預約校車
        payload = {
                "apiKey": self.Key,
                "userId": self.Namee,
                "busId": busid
                }
        r = requests.post(url, data=payload)
        r = r.text
        data = json.loads(r)
        self.Tf = data['success']
        self.Ans = data['message']
        return data['message']

    def get_success(self):
        return self.Tf

    def get_message(self):
        return self.Ans
