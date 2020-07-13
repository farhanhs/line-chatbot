from flask import Flask, request, abort
#flask網頁工具
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,FollowEvent,TemplateSendMessage,ButtonsTemplate,PostbackAction,ImageMessage,MessageAction,URIAction
)

app = Flask(__name__)

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
            thumbnail_image_url='https://i2.kknews.cc/SIG=k2b84c/n61o000109s2r818333p.jpg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackAction(
                    label='postback',
                    display_text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text'
                ),
                URIAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )
    line_bot_api.push_message(user_id,buttons_template_message)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.source.user_id
    image_id_text_send_messages = TextSendMessage(text=message_id)
    line_bot_api.reply_message(event.reply_token, image_id_text_send_messages)

if __name__ == "__main__":
    app.run()

