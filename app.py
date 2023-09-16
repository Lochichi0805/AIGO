# requirements製作 pip freeze > requirements.txt
# 在heroku上建立資料表 heroku run flask db upgrade,接著到pgAdmin中Register一個server (輸入Heroku PostgreSQL),然後到connection
# 接著要去連線,然後找到
from flask import Flask, request, abort
#可以將字串轉換成字典 action = service&category = 按摩調理>>{'action':'service','category':'按摩調理'}
from urllib.parse import parse_qsl

from events.basic import *
from events.service import *
from line_bot_api import *
from events.admin import *
from extensions import db, migrate
from models.user import User
import os

app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:1piAdFNkOc5vdyRJUIisLzhptVhsbGJV@dpg-ck2i15eru70s7382cdtg-a.singapore-postgres.render.com/aigo_t3fs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


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
    user = User.query.filter(User.line_id == event.source.user_id).first()#取得user的第一筆資料
    #如果沒有user的資料時,才會透過api去取得
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)#line API中說明get_profile可以取得的資料
        print(profile.display_name)
        print(profile.user_id)#相同的好友會因為不同的profile而有不同的user_id
        print(profile.picture_url)

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    
    print(user.id)
    print(user.line_id)
    print(user.display_name)
    

    if message_text == "@關於我們":
        about_us_event(event)

    elif message_text == "@營業據點":
        location_event(event)

    elif message_text == '@預訂服務':
        service_category_event(event)
    #管理者的line id可以去資料庫中取U1c2b304c3f1dcbcd22008a3d0ff6b785
    #開頭是*代表是管理者     
    elif message_text.startswith('*'):
        if event.source.user_id not in ['U72a5bfd4648cece9e05d94fd3227bc8f']:
            return
        if message_text in ['*data', '*d']:
            list_reservation_event(event)
        elif message_text in ['*group', '*g']:
            create_audience_group(event)

#接收postback的訊息
#parse_qsl解析data中的資料
@handler.add(PostbackEvent)
def handle_postback(event):
    #把傳進來的event儲存在postback.data中再利用parse_qsl解析data中的資料然後轉換成dict
    data = dict(parse_qsl(event.postback.data))
    #建立好def service_event(event) function後要來這裡加上判斷式
    #直接呼叫service_event(event)
    # if data.get('action') == 'service':
    #     service_event(event)
    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)    
    elif data.get('action') == 'confirm':
        service_confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 're_select':
        service_select_date_event(event)
    elif data.get('action') == 'cancel':
        service_cancel_event(event)
    #用get()來取得data中的資料,好處是如果沒有data時會顯示None,而不會出現錯誤
    # print('action:', data.get('action'))
    # print('category:', data.get('category'))
    # print('service_id:', data.get('service_id'))

    print('action:', data.get('action'))
    print('category:', data.get('category'))
    print('service_id:', data.get('service_id'))
    print('date:', data.get('date'))
    print('time:', data.get('time'))


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



