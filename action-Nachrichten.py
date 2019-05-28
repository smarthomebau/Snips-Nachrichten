#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes, MqttOptions
import io
import toml
import re
import feedparser
from subprocess import Popen

USERNAME_INTENTS = "hablijack"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None

def add_postfix(intent_name):
    return USERNAME_INTENTS + ":" + intent_name

def intent_callback_news(hermes, intent_message):
    tagesschau_url = 'http://www.tagesschau.de/export/podcast/hi/tagesschau-in-100-sekunden/'
    feed = feedparser.parse(tagesschau_url)
    podcast_url = feed['entries'][0]['links'][0]['href']
    player = Popen(["mpg123", podcast_url])
    hermes.publish_end_session(intent_message.session_id, "")

if __name__ == "__main__":
    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)

    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(add_postfix("newsInfo"), intent_callback_news)
        h.start()
