# coding=utf-8

from flask import Flask, request
# from weixin import receive, reply
import make_query as engine
import os
from langchain.memory import ConversationBufferMemory


app = Flask(__name__)

# llm, chat_prompt, memory, chat_message_history = engine.init()
llm, chat_prompt, memory = engine.init()

conversations = {}


@app.route("/")
def hello():
    return "Hello, world!"


'''
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
'''


@app.route("/chat", methods=['POST'])
def chat():
    data = request.get_json()
    query = data['query']
    if query.lower() == "hello":
        query = ""
        global memory
        # memory = ConversationBufferMemory(
        #     memory_key="chat_history", chat_memory=chat_message_history)
        memory = ConversationBufferMemory(memory_key="chat_history")
    output = engine.gpt_response(llm, chat_prompt, memory, query)
    return {'answer': output}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
