FROM python:latest
WORKDIR /reg-scraper
COPY requirements.txt /reg-scraper/requirements.txt
RUN pip install -r requirements.txt

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

COPY /scraper/* /reg-scraper
CMD [ "python", "/reg-scraper/main.py" ]