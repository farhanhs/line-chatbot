from flask import Flask, request, abort
#flask網頁工具
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

line_bot_api = LineBotApi('i8QhiXQup8rdl6IPnGgIMp65u8Z54IjMrBWkvUMf5wCElTrDd8Qe/8vgf5AksmRI5ZaxAptKhyAsZwCGocAnRA78MXndZ0IS5MxAwCwoIUYsGSd3Jt8ifVEvI8iIGhOv+52sgs+Ya4eqHunaJESP6AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b1ec8ca0fbdca57105c818c8f0d85940')

#準備一個路徑URN
#此路徑為simulate-ai
#用戶訪問的時候，回傳1+1


@app.route("/fake")
def fake():
    
    crewresult = request.get_data('https:// www.toutiao.com')
    
    return crewresult.txt
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #responce message
    user_id = event.source.user_id
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    user_id = event.source.user_id
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text='我是印度大蟒蛇'))
    except LineBotApiError as e:
    # error handle
        raise e

if __name__ == "__main__":
    app.run()

