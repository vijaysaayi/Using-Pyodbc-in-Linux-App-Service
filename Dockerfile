# load base python image
FROM appsvc/python

LABEL Name=pyodbc-for-app-services Version=0.0.1
EXPOSE 5000

WORKDIR /app
ADD app /app

#pyodbc
RUN apt-get update \
        && apt-get install -y --no-install-recommends build-essential gcc unixodbc-dev

RUN python3 -m pip install -r requirements.txt


# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
        && apt-get install -y --no-install-recommends openssh-server \
        && echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222

ENTRYPOINT ["init.sh"]
