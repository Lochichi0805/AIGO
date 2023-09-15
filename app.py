from flask import Flask, request, abort

from events.basic import *
from events.service import *
from line_bot_api import *

app = Flask(__name__)

# callback ： 串接手機及程式
@app.route("/callback", methods=['POST'])  # GET ：執行網頁時，參數會直接放在網址端
def callback():                            # POST：較有隱私，傳送參數不會放在網址端，網頁轉跳網址不變
    # get X-Line-Signature header value
    signature = request.headers["X-Line_Signature"]

    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Pleas check your channel access token/channel secret.")
        abort(400)

    return "OK"

# HandleMessage：啟動後，觸發事件用
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 把使用者輸入的英文轉成小寫存入變數meesage_text
    message_text = str(event.message.text).lower()

    if message_text == "@關於我們":
        about_us_event(event)

    elif message_text == "@營業據點":
        location_event(event)

    elif message_text == '@預訂服務':
        service_category_event(event)


# 解封鎖
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """Hello! 您好，歡迎您成為 鳳翊洋行 的好友！

我是鳳翊洋行的小幫手~

想了解更多可以點選下方選單查看更多功能喔！

期待您的光臨！"""

# 封鎖
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)

if __name__ == "__main__":
    app.run()



