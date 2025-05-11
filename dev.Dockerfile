FROM python:3.12.10-bookworm

WORKDIR /root/
RUN mkdir /run/sshd
RUN apt-get update && apt-get install openssh-server -y

RUN pip install --no-cache-dir --upgrade pip
COPY --chown=1 ./requirements.txt /root/sigrh/
RUN pip install --no-cache-dir -r /root/sigrh/requirements.txt
RUN python -m spacy download es_core_news_lg && python -m spacy download en_core_web_lg

CMD ["/usr/sbin/sshd", "-D"]

