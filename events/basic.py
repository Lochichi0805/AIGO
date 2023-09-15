from line_bot_api import *

# @關於我們
def about_us_event(event):
    # Line Available sticker list
    emoji = [
        {
            "index": 0,
            "productId": "5ac1de17040ab15980c9b438",
            "emojiId": "074"
        },
        {
            "index": 1,
            "productId": "5ac1de17040ab15980c9b438",
            "emojiId": "066"
        },
        {
            "index": 8,
            "productId": "5ac1de17040ab15980c9b438",
            "emojiId": "070"
        },
        {
            "index": 9,
            "productId": "5ac1de17040ab15980c9b438",
            "emojiId": "075"
        },
        {
            "index": 107,
            "productId": "5ac21a18040ab15980c9b43e",
            "emojiId": "048"
        },
        {
            "index": 111,
            "productId": "5ac21a18040ab15980c9b43e",
            "emojiId": "046"
        }
    ]

    # 文字回覆
    text_message = TextSendMessage(text ='''$$ 鳳翊洋行 $$
歡迎使用鳳翊洋行官方聊天機器人

本店販售各式菸酒，威士忌、紅酒、高粱、清酒、啤酒等。

營業時間皆有提供外送服務及全台宅配服務。

歡迎使用更多功能了解更多資訊，謝謝！

$《未滿$歲禁止購買菸酒類商品》''', emojis=emoji)

    # 貼圖回覆
    sticker_message = StickerSendMessage(
        package_id = '1070',
        sticker_id = '17849'
    )

    about_us_img = " https://i.imgur.com/dXBEINz.jpg"

    # 圖片回覆
    image_message = ImageSendMessage(
        original_content_url = about_us_img,
        preview_image_url = about_us_img
    )

    # 當 USER 有反應時，觸發設定之回覆給使用者
    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message]
    )

# @營業據點
def location_event(event):
    location_message = LocationSendMessage(
        title = "鳳翊洋行",
        address = "830高雄市鳳山區五甲二路52號",
        latitude = 22.604481,
        longitude = 120.34482
    )
    
    line_bot_api.reply_message(
        event.reply_token,
        location_message
    )