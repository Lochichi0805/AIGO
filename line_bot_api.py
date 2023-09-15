from flask import Flask, request, abort

from linebot import(
    LineBotApi,WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent,TextMessage,TextSendMessage,FollowEvent,UnfollowEvent,StickerSendMessage,ImageSendMessage,LocationSendMessage,
    FlexSendMessage,TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,PostbackAction
)

# 連線Line bot API(通關密語xD)
# Channel access token
line_bot_api = LineBotApi("AXAFsb6qiU4YdzrJt8wJYbCUbw15nA7hH4TPAbYokGse1isE2WelFQ8Wbae3azf8ZF1CwSUKkLNbA/A8CfSQzUVjzvwv/09T5U9XaKv+tqk084NxVgomnqmyr/PYNdXnbeYlJp/NVkcvREuYQHtgQAdB04t89/1O/w1cDnyilFU=")
# Channel secret
handler = WebhookHandler("14850b57fa56d80e8ff6ef777a9b11e2")