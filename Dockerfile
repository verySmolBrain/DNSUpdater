FROM python:3.8-alpine
WORKDIR /data
COPY updater/ .
RUN pip install -r requirements.txt
RUN apk add --update --no-cache bind-tools
CMD ["python", "update.py"]