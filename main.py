from flask import Flask, request, abort
#flask網頁工具
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextMessage, StickerSendMessage,FollowEvent
)
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['postgres://cylegcylzxwpwj:dc166c1f65eb773e5afb3e8049b5b5745a6134cfede1af72fb9c6d314cb80514@ec2-35-172-73-125.compute-1.amazonaws.com:5432/d63rc5ndhs0nhb'] = 'postgresql://localhost/postgresql-globular-31142'
db = SQLAlchemy(app)
line_bot_api = LineBotApi('i8QhiXQup8rdl6IPnGgIMp65u8Z54IjMrBWkvUMf5wCElTrDd8Qe/8vgf5AksmRI5ZaxAptKhyAsZwCGocAnRA78MXndZ0IS5MxAwCwoIUYsGSd3Jt8ifVEvI8iIGhOv+52sgs+Ya4eqHunaJESP6AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b1ec8ca0fbdca57105c818c8f0d85940')

#準備一個路徑URN
#此路徑為simulate-ai
#用戶訪問的時候，回傳1+1

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)

    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
    package_id = "1"
    sticker_id = "2"
    # package_id = "1181660"
    # sticker_id = "7389429"
    try:
        line_bot_api.push_message(user_id, TextSendMessage(text=profile.display_name + ',你好。請問需要什麼幫助？'))
        line_bot_api.push_message(user_id, TextSendMessage(text='我是印度大蟒蛇'))
        line_bot_api.push_message(user_id, StickerSendMessage(package_id=package_id, sticker_id=sticker_id))
    except LineBotApiError as e:
    # error handle
        print(e.status_code)
        print(e.request_id)
        print(e.error.message)
        print(e.error.details)
        raise e


@handler.add(FollowEvent)
def handle_follow(event):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    user_id = event.source.user_id
    #print(user_profile.user_id)
    #with open('./user.txt', 'a') as myfile:
    #    myfile.write(json.dumps(vars(user_profile)))
    #生成範本消息
    #alt_text:消息在賴聊天列表的替代文字
    #title
    #action
    #   messageaction
    #      label:案件的字樣
    #      text:
    #   uriaction
    #      label:案件的字樣
    #      text:
    #   postbackaction
    #       label
    #       text：發一個textevent
    #       data:會發一個postbackenevt給server
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://06imgmini.eastday.com/mobile/20180911/20180911033555_983b530c3845a1c818fd76c086a5587d_3.jpeg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackAction(
                    label='回傳動作', date='special', text='以用戶身份發話'
                )
                MessageAction(
                    label='message',
                    text='message text')
                URIAction(
                    label='自拍輸入'
                    uri='https://line.me/R/nv/camera/'
                )
            ),

        ]
    )
    )

        follow_text_send_message=TextMessage('kkk')

        line_bot.reply_message(event.reply_token, follow_text_send_message)

if __name__ == "__main__":
    app.run()

