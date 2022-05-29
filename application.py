from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,QuickReply,QuickReplyButton,MessageAction
)
import os
import datetime 
# from local_config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

YOUR_CHANNEL_ACCESS = os.environ.get("YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://{}:{}@{}/{}?charset=utf8".format("root", "", "localhost", "test")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     line_id = db.Column(db.Text(), nullable=False)
#     line_name = db.Column(db.Text(), nullable=False)
#     mail =  db.Column(db.Text(), nullable=True)
#     state = db.Column(db.Integer, primary_key=True)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    state_list = ['やばい...','普通','良い!']
    state = ['1','2','3']

    # if event.message.text in state:
    #     user_list = [ _user.line_id for _user in User.query.all()]        
    #     user_id = event.source.userID 
    #     if user_id in user_list:
    #         _user = User.query.filter(User.line_id == user_id).first()
    #         _user.state = int(event.message.text)
    #         db.session.add(_user)
    #         db.session.commit()
    #     else:
    #         _user = User()
    #         _user.line_id = user_id
    #         _user.line_name = line_bot_api.get_profile(user_id = user_id)
    #         _user.state = int(event.message.text)
    #         db.session.add(_user)
    #         db.session.commit()
    # else:
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text="入力してね"))

    items = [QuickReplyButton(action=MessageAction(label=state_list[i], text=state[i])) for i in range(len(state_list))]
    messages = TextSendMessage(text='現在の進捗はどうですか？',quick_reply=QuickReply(items=items))
    line_bot_api.reply_message(event.reply_token, messages=messages)

# Botを登録しているユーザに一括送信
def notify():
    state_list = ['やばい...','普通','良い!']
    state = ['1','2','3']
    items = [QuickReplyButton(action=MessageAction(label=state_list[i], text=state[i])) for i in range(len(state_list))]
    messages = TextSendMessage(text='現在の進捗はどうですか？',quick_reply=QuickReply(items=items))
    line_bot_api.broadcast(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
