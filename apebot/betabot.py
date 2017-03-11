# -*- coding: utf-8 -*-

from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

from matrix_client.client import MatrixClient

password = input('Password? ')

client = MatrixClient("https://matrix.org")
engine = IntentDeterminationEngine()


def on_message(room, event):
    if event['type'] == "m.room.message":
        if event['content']['msgtype'] == "m.text":

            if event['sender'] != '@apebot:matrix.org':
                room.send_text("You said '{}'".format(event['content']['body']))
                for intent in engine.determine_intent(event['content']['body']):
                    room.send_text('{} {}'.format(intent.get('intent_type'), intent.get('confidence')))
                    if intent.get('intent_type') == 'HideIntent':
                        if intent.get('confidence') > 0:
                            #room.send_text(json.dumps(intent, indent=4))
                            room.send_text('*Apebot hides')
    else:
        pass

weather_keyword = ['weather']
for wk in weather_keyword:
    engine.register_entity(wk, "WeatherKeyword")

weather_types = ['snow', 'rain', 'wind', 'sleet', 'sun']
for wt in weather_types:
    engine.register_entity(wt, "WeatherType")

locations = ['Seattle', 'San Fransisco', 'Tokyo']
for loc in locations:
    engine.register_entity(loc, 'Location')

weather_intent = IntentBuilder("WeatherIntent")\
        .require("WeatherKeyword")\
        .optionally("WeatherType")\
        .require('Location')\
        .build()

hide_keyword = ['hide']
for hk in hide_keyword:
    engine.register_entity(hk, "HideKeyword")

hide_intent = IntentBuilder("HideIntent").require("HideKeyword").build()

engine.register_intent_parser(weather_intent)
engine.register_intent_parser(hide_intent)

# Existing user
token = client.login_with_password(username="@apebot:matrix.org", password=password)

room = client.join_room("#apebot:matrix.org")
room.add_listener(on_message)
room.send_text("ApeBot reporting for duty")

try:
    client.listen_forever()
except KeyboardInterrupt:
    pass
finally:
    room.send_text("ApeBot going to sleep")
