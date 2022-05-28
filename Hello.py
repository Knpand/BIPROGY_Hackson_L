# def hello():
#     print("HelloWorld")


# from flask import Flask, render_template
# import os

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return render_template('index.html') 

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
#     # app.run(debug=True)

#     app.run()


# def wrapLog(func):
#     def _wrapLog():
#         print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "start", func.__name__)
#         func()
#         print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "end", func.__name__ )
#     return _wrapLog

# sche = BlockingScheduler()
# @sche.scheduled_job('interval',minutes=30)
# @wrapLog
# def job1():
#     pass() #実行したい処理

import datetime as dt
import pandas as pd

def test():
    print('hello world!!')
    print(dt.datetime.utcnow().strftime('%Y/%m/%d %H:%M'))
    print(pd.DataFrame(columns=['A', 'B', 'C'], index=[i for i in range(2)]))

test()