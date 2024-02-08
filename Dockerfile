FROM python

COPY app /app

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]