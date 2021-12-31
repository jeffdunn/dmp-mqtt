FROM python:3.8
WORKDIR /dmp
RUN pip3 install gmqtt
COPY ./src/dmp/* ./
WORKDIR /
CMD python3 -m dmp \
  --listen-port $LISTEN_PORT \
  --dmp-server-host $DMP_SERVER_HOST \
  --dmp-server-port $DMP_SERVER_PORT \
  --dmp-account-number $DMP_ACCOUNT_NUMBER \
  --dmp-remote-key $DMP_REMOTE_KEY \
  --mqtt-broker-host $MQTT_BROKER_HOST \
  --mqtt-username $MQTT_USERNAME \
  --mqtt-password $MQTT_PASSWORD
