from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,QuickReply,QuickReplyButton,PostbackAction
)
import os
import datetime 

app = Flask(__name__)
 
YOUR_CHANNEL_ACCESS = os.environ.get("access_token")
YOUR_CHANNEL_SECRET = os.environ.get("channel_secret")

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


db = SQLAlchemy(app)
migrate = Migrate(app,db)
db.init(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://{}:{}@{}/{}?charset=utf8".format("root", "", "localhost", "test")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.Text(), nullable=False)
    line_name = db.Column(db.Text(), nullable=False)
    state = db.Column(db.Integer, primary_key=True)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    state_list = ['やばい','普通','良い']
    state = ['1','2','3']

    if event.message.text in state:
        user_list = [ _user.line_id for _user in User.query.all()]        
        user_id = event.source.userID 
        if user_id in user_list:
            _user = User.query.filter(User.line_id == user_id).first()
            _user.state = int(event.message.text)
            db.session.add(_user)
            db.session.commit()
        else:
            _user = User()
            _user.line_id = user_id
            _user.line_name = line_bot_api.get_profile(user_id = user_id)
            db.session.add(_user)
            db.session.commit()
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="入力してね"))
if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run(host="0.0.0.0",port=port)
    
