FROM python:2.7
MAINTAINER Cem Gokmen <cgokmen@gatech.edu>

COPY . /verne
WORKDIR /verne

RUN chmod +x install_git.sh
RUN ./install_git.sh

RUN chmod +x install_rtimulib.sh
RUN ./install_rtimulib.sh

RUN pip install -r requirements.txt

VOLUME /dev/geigerCounter
VOLUME /dev/i2c-1
VOLUME /data

CMD python main.py
