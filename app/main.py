# coding=utf-8

from flask import Flask, request
# from weixin import receive, reply
from make_query import ChatEngine
import os
from langchain.memory import ConversationBufferMemory
from history_db import HistoryHandler


app = Flask(__name__)


engine = ChatEngine()
llm, chat_prompt, chat_message_history = engine.init()
memory = ConversationBufferMemory(
    memory_key="chat_history")

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
    '''
    TODO: user_id and session_id
    '''
    user_id = request.headers.get('User-Id')
    session_id = request.headers.get('Session-Id')
    print(f'user id: {user_id}, session_id: {session_id}')
    if query.lower() == "hello":
        query = ""
        global memory
        memory = ConversationBufferMemory(
            memory_key="chat_history")

    output = engine.gpt_response(
        user_id, session_id, llm, chat_prompt, memory, query)
    # save chat history
    history_handler = HistoryHandler()
    human_data = {"user_id": user_id, "session_id": session_id,
                  "type": 1, "message": query}
    history_handler.insert_one_history(**human_data)
    ai_data = {"user_id": user_id, "session_id": session_id,
               "type": 0, "message": output}
    history_handler.insert_one_history(**ai_data)

    return {'answer': output}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
