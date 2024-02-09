FROM python

COPY app /app

COPY cmd.sh /

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi && chmod +x /cmd.sh

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 9090 9191

USER uwsgi

CMD ["/cmd.sh"]