FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV OPENAI_API_KEY {{set your own api key here}}
ENV OPENAI_API_BASE {{set you own api base here}}

COPY ./app /app

RUN pip install langchain
RUN pip install openai
RUN pip install flask


