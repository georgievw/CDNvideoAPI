FROM python

COPY . /app

COPY cmd.sh /

WORKDIR /app

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi && chmod +x /cmd.sh

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 5000 9090 9191

USER uwsgi

CMD ["/cmd.sh"]