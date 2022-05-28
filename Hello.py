# -*- coding: utf-8 -*-
import requests
import json
import datetime
from dateutil import tz
import dateutil.parser
import jwt
import time
import random
from pprint import pprint
from tzlocal import get_localzone

#
# Meetingクラス
#
class MeetingClass:
    _token = None
    _meeting_id = None
    _meeting_status = None
    _meeting_uuid = None
    _meeting_json = None

    CONST_ZOOM_URL = ' https://api.zoom.us/v2'
    CONST_ZOOM_API_KEY = ''                       #  APIキー
    CONST_ZOOM_API_SECRET = ''      #  APIの秘密鍵
    CONST_ZOOM_USER_ID = ''                           # 主催者のメールアドレス
    CONST_ZOOM_TOKEN_EXPIRE_SEC = 600                                   # トークン有効期限：600秒


    # トークン（JWT）作成メソッド
    def _GenerateToken(self,expire_sec):
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"iss": self.CONST_ZOOM_API_KEY, "exp": int(time.time() + expire_sec)}
        self._token = jwt.encode(payload, self.CONST_ZOOM_API_SECRET, algorithm='HS256', headers=header)

    #  デフォルト設定JSON生成メソッド
    def _CreateDefaultSettings(self,contact_name:str,contact_email:str):

        return {
            'host_video': True,             # start video when the host joins
            'participant_video': True,      # start video when the participants join
            'join_before_host': True,       # no host
            'jbh_time': 0,                  # Allow the participant to join the meeting at anytime.(デフォルトっぽい)
            'mute_upon_entry': True,        # mute paticipants upon entry
            'approval_type': 0,             # automatically approve
            'cn_meeting': False,            # host meeting in china
            'in_meeting': False,            # host meeting in india
            'watermark': False,             # add a watermark when viewing a shared screen
            'use_pmi': False,               # personal meeting id
            'registration_type': 1,         # The meeting's registration type
            'audio': "voip",                # How participants join the audio portion of the meeting
            'auto_recording': "none",       # The automatic recording settings
            'enforce_login': False,                     # enfoce login
            'waiting_room': False,                      # Whether to enable the Waiting Room feature if this values true,this disables the join_before_hosts setting
            'registrants_email_notification': False,    # Whether to sedn registants email notifications abount their registration approval cancellation or rejection
            'meeting_authentication': False,    # if true ,only authenticated users can join the meeting
            'contact_name': contact_name,       # The contact name for meeting registration
            'contact_email': contact_email}     # The contact email for meeting registration

    #  リクエストヘッダ生成メソッド
    def _GetHeaders(self,expire_sec: int):

        # トークン（JWT）作成
        self._GenerateToken(self.CONST_ZOOM_TOKEN_EXPIRE_SEC)

        # トークンを設定し、ヘッダ(JSON)作成
        headers = {'Authorization': f"Bearer {self._token}",
                   'Content-Type': 'application/json'}

        return headers

    #   
    #  リモート会議生成メソッド
    #
    def CreateMeeting(self, topic: str, start_time: datetime, duration_min: int,pass_code: str,contact_name:str,contact_email:str):
        print("debug")
        # リモート会議作成用のURLを生成
        end_point =  f'/users/{self.CONST_ZOOM_USER_ID}/meetings'

        #　トークンのタイムアウト値を指定し、リクエストヘッダを生成
        headers = self._GetHeaders(self.CONST_ZOOM_TOKEN_EXPIRE_SEC)

        # パスコードが未指定なら自動生成する
        if not pass_code:
            pass_code = str(random.randint(100000, 999999))
        
        # 会議のデフォルトパラメータを設定
        
        default_setting = self._CreateDefaultSettings(contact_name,contact_email)

        # リクエストのボディ部を生成
        body = {
            "topic": topic, # 会議の題名（Invitationに含まれる）
            'type': 2,  # scheduled meeting
            "start_time": start_time.isoformat(),
            "duration": duration_min,
            "timezone": "Osaka, Sapporo, Tokyo",
            "password": pass_code,
            #"agenda": agenda,
            "settings": default_setting}

        try:
            # リクエスト送信（生成：POST）
            # This API has a daily rate limit of 100 requests per day. 
            # Therefore, only 100 Create a Meeting API requests are permitted within a 24 hour window for a user.
       
            response = requests.request('POST',
                                    self.CONST_ZOOM_URL + end_point,
                                    headers=headers,
                                    data=json.dumps(body)).json()
            print("debug2")
            # レスポンス(JSON)からデータ取得
            self._meeting_id = response['id']   # meeting id
            self._status = response['status']   # 会議の状態
            self._uuid = response['uuid']       # uuid
            self._meeting_json = response       # レスポンス全体

            return self._meeting_id

        except Exception as e:
            # print(e)
            return "err"


    # # 　これは要件次第
    # #  リモート会議招待用テキスト取得メソッド
    # #
    def GetInvitation(self, meeting_id: int):
 
        # リモート会議招待用テキスト取得のURLを生成
        end_point = f"/meetings/{meeting_id}/invitation"
 
        #　トークンのタイムアウト値を指定し、リクエストヘッダを生成
        headers = self._GetHeaders(self.CONST_ZOOM_TOKEN_EXPIRE_SEC)
 
        # リクエスト送信（取得：GET）
        invitation = requests.request("GET",
                                self.CONST_ZOOM_URL + end_point,
                                headers=headers).json()
        return invitation

if __name__ == '__main__':
    date=datetime.datetime.utcnow()
    # .strftime('%Y/%m/%d %H:%M')
    MTGobj=MeetingClass()
    meetID=MTGobj.CreateMeeting("sample",date,30,"Biprogy123","icebreak","icebreak_mt1@itresourcetech.net")


    print(meetID)

    invitation = MTGobj.GetInvitation(meetID)
    pprint(invitation)