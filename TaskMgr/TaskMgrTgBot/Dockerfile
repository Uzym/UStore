FROM python:3.10.6
COPY . ./app
RUN pip3 install -U -r ./app/requirements.txt
ENTRYPOINT [ "python3", "./app/main.py" ]