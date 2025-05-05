FROM python:3.13.3-bookworm

WORKDIR /root/
RUN mkdir /run/sshd
RUN apt-get update && apt-get install openssh-server -y

RUN pip install --no-cache-dir --upgrade pip
COPY --chown=1 ./requirements.txt /root/sigrh/
RUN pip install --no-cache-dir -r /root/sigrh/requirements.txt
CMD ["/usr/sbin/sshd", "-D"]

