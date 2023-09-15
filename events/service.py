from line_bot_api import *
from urllib.parse import parse_qsl


#預約相關的功能都會寫在這裡
#增加多個服務項目
services = {
    1: {
        'category': '婚禮',
        'img_url': 'https://imgur.com/BvonVPh',
        'title': '紅酒',
        'duration': 'Red Wine',
        'description': '這個愛的時刻，讓紅酒成為您們的杯中驚喜，見證您們的愛情故事。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    },
    2: {
        'category': '婚禮',
        'img_url': 'https://imgur.com/2w59MIm',
        'title': '香檳/氣泡酒',
        'duration': 'Champagne/Sparkling wine',
        'description': '香檳/氣泡酒不僅是婚禮上的一種美味飲品，更是一種象徵愛情和慶祝的文化符號。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    },
    3: {
        'category': '大型活動',
        'img_url': 'https://imgur.com/jNkQKBt',
        'title': '威士忌',
        'duration': 'Whisky',
        'description': '威士忌是一種充滿歷史和文化的烈酒，具有豐富的風味和多樣性，象徵著品味和品質的飲品。',
        'price': 0000,
        'post_url': 'https://linecorp.com'
    },
    4: {
        'category': '大型活動',
        'img_url': 'https://imgur.com/BvonVPh',
        'title': '紅酒',
        'duration': 'Red Wine',
        'description': '紅酒，這經典的葡萄酒，彷彿是時光的藝術品。它以深邃的紅色和令人陶醉的風味，帶您踏上一場美味的旅程。',
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
        alt_text='請選擇想服務類別',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://imgur.com/4oa2gSl',
                    action=PostbackAction(
                        label='婚禮',
                        display_text='想預定婚禮用酒',
                        data='action=service&category=婚禮'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://imgur.com/gLoo0k7',
                    action=PostbackAction(
                        label='',
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
#         alt_text = "選擇預約項目"
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
                      "label": "預約",
                      "data": f"action=select_date&service_id={service_id}",
                      "displayText": f"我想預約【{service['title']} {service['duration']}】"
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