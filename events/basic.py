from line_bot_api import *


def about_us_event(event):
    emoji = [
        {
            "index": 0,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "225"
        },
        {
            "index": 13,
            "productId": "5ac21184040ab15980c9b43a",
            "emojiId": "225"
        }
    ]

    text_message = TextSendMessage(text='''$ Master SPA $
專業中醫推拿出身，融合東西方按摩手法

-嚴格把關：所有用品皆有消毒或採一次用品。

-設備齊全：夏天有冷氣，冬天有電毯和暖氣。

-獨立空間：專業乾淨高品質獨立按摩空間。''', emojis=emoji)

    sticker_message = StickerSendMessage(
        package_id='8522',
        sticker_id='16581271'
    )

    about_us_img = 'https://i.imgur.com/70A4WdI.jpg'

    image_message = ImageSendMessage(
        original_content_url=about_us_img,
        preview_image_url=about_us_img
    )

    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message])
# # @關於我們
# def about_us_event(event):
#     # Line Available sticker list
#     emoji = [
#         {
#             "index": 0,
#             "productId": "5ac21184040ab15980c9b43a",
#             "emojiId": "225"
#         },
#         {
#             "index": 13,
#             "productId": "5ac21184040ab15980c9b43a",
#             "emojiId": "225"
#         }
#     ]

#     # 文字回覆
#     text_message = TextSendMessage(text ='''$ 鳳翊洋行 $
# 歡迎使用鳳翊洋行官方聊天機器人
# 本店販售各式菸酒，威士忌、紅酒、高粱、清酒、啤酒等。                                 
# 營業時間皆有提供外送服務及全台宅配服務
# 本店付款方式可使用現金、刷卡、台灣pay、Line pay
# 歡迎使用更多功能了解更多資訊，謝謝！ 
# 《未滿18歲禁止購買菸酒類商品》''', emojis=emoji)

#     # 貼圖回覆
#     sticker_message = StickerSendMessage(
#         package_id = '1070',
#         sticker_id = '17843'
#     )

#     about_us_img = " https://i.imgur.com/70A4WdI.jpg"

#     # 圖片回覆
#     Image_message = ImageSendMessage(
#         original_content_url = about_us_img,
#         preview_image_url = about_us_img
#     )

#     # 當 USER 有反應時，觸發設定之回覆給使用者
#     line_bot_api.reply_message(
#         event.reply_token,
#         [text_message, sticker_message, Image_message]
#     )

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