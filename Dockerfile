FROM lambci/lambda:build-python3.6
ENV LANG C.UTF-8
ENV AWS_DEFAULT_REGION us-east-2

# create deploy_package.zip
WORKDIR /var/task
# copy
COPY requirements.txt requirements.txt
COPY lambda_function.py lambda_function.py
COPY modules modules
COPY ng_words.txt ng_words.txt
# pip
RUN /bin/cp -f /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
  pip install -r requirements.txt -t /var/task
# zip
RUN find . -type d -name '__pycache__' | xargs rm -rf
RUN zip -r deploy_package.zip *

# start
WORKDIR /home/root
COPY start.sh start.sh
CMD ["/bin/bash", "./start.sh"]
