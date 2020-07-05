from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('fU0yRtP3xz/+bZzaUG1McB+c4kRnI0k0vmVf+0swGg5ztrcwB2Fu29izMyqAn7yDRFcc+7vw90IP7alolXaA2QPsM2kjjQAXyAY63zRMksBT27l8f3f6LUOMuzmTRNf3dCIiyEYhA7E7EtIcMCVTPwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f29ed1ca596babd9e4be1aafc3950576')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()