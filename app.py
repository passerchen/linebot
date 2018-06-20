from flask import Flask, request, abort,Response

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi('zeBfDqrG50nJsE0rkLJ0L19h7LP1Gb4P6iRxEs+BwjqfIclLNmthXXU/sfxbWt3LL2AABWCD3quCA0VmjehdKSx/3/qf7HyGq+iyGUYZ0hQ5cUwQKLHVeiE3NCTQfouapznnlUIqy3/q0O3uddTCxQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('1496755558a888ad6e228c7a1fdfbfd1')
parser = WebhookParser('1496755558a888ad6e228c7a1fdfbfd1')
#UserID
line_bot_api.push_message('U7e54e871672bd5f9aefd6f059622edab', 
    TextSendMessage(text='準備下班了!!!!'))

#亂貼 group id
line_bot_api.push_message('Cc463c39db1386fd085e33a42cccd0ee9', 
	TextSendMessage(text='https://d762d4a9.ngrok.io/getfile/QQ.pdf'))   
#    TextSendMessage(text='https://www.ga.ntnu.edu.tw/aff/form/insurance2.pdf'))   

# 監聽所有來自 /callback 的 Post Request

@app.route('/YUSCO/<path:path>')
def send_images(path):
    line_bot_api.push_message('Cc463c39db1386fd085e33a42cccd0ee9', 
            TextSendMessage(text='https://d762d4a9.ngrok.io/YUSCO/QQ.pdf'))    	
    return send_from_directory('YUSCO', path)


@app.route('/getfile/<name>')
def get_output_file(name):
    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(OUTPUT_DIR, name)
    print(file_name)

    if not os.path.isfile(file_name):
        return "No File"

    # read without gzip.open to keep it compressed
    with open(file_name, 'rb') as f:
        resp = Response(f.read())
    # set headers to tell encoding and to send as an attachment
    #resp.headers["Content-Encoding"] = 'gzip'
    resp.headers["Content-Disposition"] = "attachment; filename={0}".format(name)
    resp.headers["Content-type"] = "application/pdf"
    return resp


@app.route("/callback", methods=['POST'])
#def send_images(path):
#    return send_from_directory('callback', path)
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)





    # handle webhook body
    try:
        #handler.handle(body, signature)
        events = parser.parse(body, signature)
        
    except InvalidSignatureError:
        abort(400)    

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        text=event.message.text
        print('**** user input=' + str(text))
        #userId = event['source']['userId']
        if(text.lower()=='me'):
            content = str(event.source.user_id)
            #content = str(event.source.group_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content)
            )

            line_bot_api.push_message('U7e54e871672bd5f9aefd6f059622edab', 
            TextSendMessage(text='準備下班了aaaa!!!!'))
            line_bot_api.push_message('Cc463c39db1386fd085e33a42cccd0ee9', 
            TextSendMessage(text='https://d762d4a9.ngrok.io/getfile/QQ.pdf'))
            #TextSendMessage(text='https://www.ga.ntnu.edu.tw/aff/form/insurance2.pdf'))
        elif(text.lower()=='jpg'):        	          
            message = ImageSendMessage(
        	    original_content_url='https://d762d4a9.ngrok.io/callback/qq.jpg',
        	    preview_image_url='https://d762d4a9.ngrok.io/callback/qq.jpg'
        	    #original_content_url='https://www.ga.ntnu.edu.tw/aff/form/insurance2.pdf',
        	    #preview_image_url='https://www.ga.ntnu.edu.tw/aff/form/insurance2.pdf'
            )

            line_bot_api.reply_message(event.reply_token,message)

        elif(text.lower()!=' '):
             content = str(event.message.text)
             #content ="test"
             line_bot_api.reply_message(
                 event.reply_token,
                 TextSendMessage(text=content)
             )
             line_bot_api.push_message('Cc463c39db1386fd085e33a42cccd0ee9', 
	              TextSendMessage(text='https://d762d4a9.ngrok.io/getfile/'+content+'.pdf'))    
        elif(text.lower()=='/profile'):
            profile = line_bot_api.get_profile(str(event.source.user_id))
            print(profile.display_name)
            print(profile.user_id)
            print(profile.picture_url)
            print(profile.status_message)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='還在練習> <')
            )

    return 'OK'

@app.route("/", methods=['GET'])
def basic_url():
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
#    message = TextSendMessage(text=event.message.text)
    message = TextSendMessage(text='真難搞')            
    line_bot_api.reply_message(
        event.reply_token,
        message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
