from line_bot_api import *
from urllib.parse import parse_qsl
import datetime

from extensions import db
from models.user import User
from models.reservation import Reservation#資料寫入資料庫中

#預訂相關的功能都會寫在這裡
#增加多個服務項目
services = {
    1: {
        'category': '婚禮',
        'img_url': 'https://i.imgur.com/BvonVPh.jpg',
        'title': '紅酒',
        'duration': 'Red Wine',
        'description': '這個愛的時刻，讓紅酒成為您們的杯中驚喜，見證您們的愛情故事。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    },
    2: {
        'category': '婚禮',
        'img_url': 'https://i.imgur.com/2w59MIm.jpg',
        'title': '香檳/氣泡酒',
        'duration': 'Champagne/Sparkling wine',
        'description': '香檳/氣泡酒不僅是婚禮上的一種美味飲品，更是一種象徵愛情和慶祝的文化符號。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    },
    3: {
        'category': '大型活動',
        'img_url': 'https://i.imgur.com/snyGO0G.jpg',
        'title': '威士忌',
        'duration': 'Whisky',
        'description': '威士忌是一種充滿歷史和文化的烈酒，具有豐富的風味和多樣性，象徵著品味和品質的飲品。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    },
    4: {
        'category': '大型活動',
        'img_url': 'https://i.imgur.com/2w59MIm.jpg',
        'title': '香檳/氣泡酒',
        'duration': 'Champagne/Sparkling wine',
        'description': '香檳和氣泡酒代表了葡萄酒的精華，它們擁有引人入勝的氣泡、多樣的風味和無盡的慶祝潛力。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    }
}

#alt_text的文字會顯示在三個地方 一用戶收到訊息時二在聊天清單中三用戶手機不支援時
#label是按鈕上的文字 display_text用戶點擊時會傳送到聊天室的訊息 data則是會傳送給我們的資料
#裡面每一個column都是一張圖片
#PostbackAction當用戶點擊時就會傳資料給我們
def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇使用場合',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/4oa2gSl.jpg',
                    action=PostbackAction(
                        label='婚禮',
                        display_text='想預定婚禮用酒',
                        data='action=service&category=婚禮'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://i.imgur.com/gLoo0k7.jpg',
                    action=PostbackAction(
                        label='大型活動',
                        display_text='想預定大型活動用酒',
                        data='action=service&category=大型活動'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])

#先定義一個function
# def service_event(event):
#     flex_message = FlexSendMessage(
#         alt_text = "選擇預訂項目"
#         contents = {

#         }
#     )
#貼上後所有的 "wrap": True 都要改成大寫
#新增完成後要回到app.py加上判斷式
def service_event(event):
    #底下三個要等上面的service建立後才寫,主要是要跑service的服務
    #data = dict(parse_qsl(event.postback.data))
    #bubbles = []
    #for service_id in services:
    data = dict(parse_qsl(event.postback.data))

    bubbles = []

    for service_id in services:
        if services[service_id]['category'] == data['category']:
            service = services[service_id]
            bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": service['img_url']
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": service['title'],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                  },
                  {
                    "type": "text",
                    "text": service['duration'],
                    "size": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "text": service['description'],
                    "margin": "lg",
                    "wrap": True
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": f"NT$ {service['price']}",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0
                      }
                    ],
                    "margin": "xl"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "postback",
                      "label": "預訂",
                      "data": f"action=select_date&service_id={service_id}",
                      "displayText": f"我想預訂【{service['title']}】"
                    },
                    "color": "#b28530"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "了解詳情",
                      "uri": service['post_url']
                    }
                  }
                ]
              }
            }

            bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text='請選擇想預訂的項目',
        contents={
          "type": "carousel",
          "contents": bubbles
        }
    )

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message])
    #預訂日期的功能
#設定完這個function後就要到app.py中的handle_postback去新增判斷式
def service_select_date_event(event):

    data = dict(parse_qsl(event.postback.data))

    weekday_string = {
        0: '一',
        1: '二',
        2: '三',
        3: '四',
        4: '五',
        5: '六',
        6: '日',
    }

    business_day = [1, 2, 3, 4, 5, 6]

    quick_reply_buttons = []

    today = datetime.datetime.today().date()#取得當天的日期
    #weekday()取得星期幾?0是星期一
    for x in range(1, 11):
        day = today + datetime.timedelta(days=x)#透過datetime.timedelta()可以取得隔天的日期

        if day.weekday() in business_day:
            quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=f'{day} ({weekday_string[day.weekday()]})',
                                      text=f'我要預訂 {day} ({weekday_string[day.weekday()]}) 這天',
                                      data=f'action=select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預訂哪一天?',
                                   quick_reply=QuickReply(items=quick_reply_buttons))

    line_bot_api.reply_message(
        event.reply_token,
        [text_message])
    #選擇時間的功能
def service_select_time_event(event):

    data = dict(parse_qsl(event.postback.data))

    available_time = ['11:00', '14:00', '17:00', '20:00']

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_button = QuickReplyButton(action=PostbackAction(label=time,
                                                                    text=f'{time} 活動時間',
                                                                    data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
        quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問活動時間為何時?',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    line_bot_api.reply_message(
        event.reply_token,
        [text_message])


#confirm_template是用來確認,它包含了訊息和底下有兩個按鈕
#PostbackAction可以帶data的資料,MessageAction則是用戶按下去時會直接傳訊息到聊天室
def service_confirm_event(event):

    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])]#取得要預訂的服務項目資料,會出現1234對應到上面的service

    confirm_template_message = TemplateSendMessage(
        alt_text='請確認預訂品項',
        template=ConfirmTemplate(
            text=f'您即將預訂\n\n{booking_service["title"]} {booking_service["duration"]}\n預訂時間: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                PostbackAction(
                    label='確定',
                    display_text='確認沒問題!',
                    data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                ),
                MessageAction(
                    label='重新預訂',
                    text='我想重新預訂',
                    data='action=re_select'
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message])

#取消用的是ButtonsTemplat,有訊息的標題和訊息的內容
#action中可以設定一到四個按鈕
#這個function是判斷用戶是否預訂過,利用Reservation.query.filter搜尋資料,條件是user_id == user.id
def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),#代表沒有被取消
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           #需要大於當下的時間.first()是會回傳第一筆資料
    if reservation:#text顯示預訂項目名稱和服務時段
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預訂了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預訂了',
                text=f'{reservation.booking_service}\n預訂時間: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預訂',
                        display_text='我想取消預訂',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False


def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))

    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    user = User.query.filter(User.line_id == event.source.user_id).first()
    if is_booked(event, user):
        return

    reservation = Reservation(
        user_id=user.id,
        booking_service_category=f'{booking_service["category"]}',
        booking_service=f'{booking_service["title"]} {booking_service["duration"]}',
        booking_datetime=booking_datetime)

    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='沒問題! 感謝您的預訂，我已經幫你預訂成功了喔，到時候見!')])

#取消預訂 資料庫的欄位不會drop,是is_canceled欄位會改成true
def service_cancel_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        reservation.is_canceled = True

        db.session.add(reservation)
        db.session.commit()

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您的預訂已經幫你取消了')])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您目前沒有預訂喔')])


def test_event(event):
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
            'type': 'bubble',
            'direction': 'ltr',
            'hero': {
                'type': 'image',
                'url': 'https://example.com/cafe.jpg',
                'size': 'full',
                'aspectRatio': '20:13',
                'aspectMode': 'cover',
                'action': {'type': 'uri', 'uri': 'http://example.com', 'label': 'label'}
            }
        }
    )

    quick_message = TextSendMessage(text='Hello, world',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="label", text="text"))
                                    ]))

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message, quick_message])