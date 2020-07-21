import random
from flask import Flask, request, abort
#flask網頁工具
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, FollowEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction, ImageMessage, MessageAction, URIAction,VideoMessage,VideoSendMessage
)
import os
import connect_sql as cs
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, \
    line_channel_secret

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


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
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
        alt_text='為什麼你可以賣這麼便宜！',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i2.kknews.cc/SIG=k2b84c/n61o000109s2r818333p.jpg',
            title='競拍表單',
            text='請選擇服務類型',
            actions=[
                MessageAction(
                    label='今日拍賣',
                    text='我要看商品',
                ),
                MessageAction(
                    label='我要拍賣',
                    text='我要拍賣商品',
                ),
                MessageAction(
                    label='抽個大吉',
                    text='postback text',
                ),
            ]
        )
    )
    line_bot_api.push_message(user_id,buttons_template_message)

@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(client_id, client_secret,
                                 access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'Cute kitten being cute on '
            }
            path = os.path.join('static', 'tmp', dist_name)
            client.upload_from_path(path, config=config, anon=False)
            os.remove(path)
            print(path)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳成功'))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
        return 0

    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    elif isinstance(event.message, TextMessage):
        if event.message.text =='我要看商品':
            try:
                client = ImgurClient(client_id, client_secret)
                images = client.get_album_images(album_id)
                index = random.randint(0, len(images) - 1)
                url = images[index].link
                image_message = ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                    )
                line_bot_api.push_message(user_id, TextSendMessage(
                    text=profile.display_name + ',你好。現在競拍的商品為：'))
                line_bot_api.reply_message(
                    event.reply_token, image_message)
                line_bot_api.push_message(user_id, TextSendMessage(text='底標為：'))
                line_bot_api.push_message(user_id, StickerSendMessage(
                        package_id=package_id, sticker_id=sticker_id))
            except LineBotApiError as e:
                    # error handle
                    print(e.status_code)
                    print(e.request_id)
                    print(e.error.message)
                    print(e.error.details)
                    raise e
        if event.message.text == "看看大家都傳了什麼圖片":

            return 0
        else:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=' yoyo'),
                    TextSendMessage(text='請傳一張圖片給我')
                ])
            return 0

if __name__ == "__main__":
    app.run()

