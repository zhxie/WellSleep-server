FROM python:3

WORKDIR /usr/src/WellSleep-server

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "flask", "run" ]
