# coding=utf-8

from flask import Flask, request
from weixin import receive, reply
import make_query as engine


app = Flask(__name__)

llm, chat_prompt, memory = engine.init()

conversations = {}

@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/wx", methods=['GET', 'POST'])
def make_appointment():
    if request.method == 'POST':
        xml_str = request.data
        print(f'Handle web data: {xml_str}')
        rec_msg = receive.parse_xml(xml_str)

        if isinstance(rec_msg, receive.Msg) and rec_msg.MsgType == 'text':
            to_user = rec_msg.FromUserName
            from_user = rec_msg.ToUserName
            query = rec_msg.content
            output = engine.gpt_response(llm, chat_prompt, memory, query)
            print(f'output: {output}')

            # store chat history
            qa_pair = {'query': query, 'answer': output}
            if from_user in conversations.keys():
                conversations[from_user].append({'query': query, 'answer': output})
            else:
                pairs = []
                pairs.append({'query': query, 'answer': output})
                conversations[from_user] = pairs

            reply_msg = reply.TextMsg(to_user, from_user, output)
            response = reply_msg.send()
            print(f'response: {response}')
            return response
        else:
            return 'success'

    