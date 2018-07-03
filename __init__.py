from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import requests

class Match(object):
    pass

class DecipherIndustriesSkill(MycroftSkill):

    def __init__(self):
        super(DecipherIndustriesSkill, self).__init__(name="DecipherIndustriesSkill")

        self.api_url = "http://api.essense.decipher.digital/api/v1"

    @intent_handler(IntentBuilder("").require("State").require("Entity"))
    def handle_entity_state_intent(self, message):
        spoken_entity = message.data.get("Entity")
        split_spoken_entity = spoken_entity.split()
        matched_entity = Match()
        matched_entity.matches = 0

        res = requests.get(self.api_url + '/state')
        if res.status_code == 200:
            json_data = res.json()
            for name, data in json_data["switches"]:
                split_name = data["name"].split("_")
                i = 0
                matches = 0
                while i < len(split_spoken_entity):
                    j = 0
                    while j < len(split_name):
                        if split_spoken_entity[i] == split_name[j]:
                            matches += 1
                if matches > matched_entity.matches:
                    matched_entity.matches = matches
                    matched_entity.name = data.name
                    matched_entity.state = data.state

            if matched_entity.matches > 0:
                self.speak_dialog("entity.state", data={
                    "entity": " ".join(matched_entity.name), 
                    "state": "off" if matched_entity.state == 0 else "on"})
            else:
                self.speak_dialog("no.match")
        else:
            self.speak_dialog("something.has.gone.wrong")

        
def create_skill():
    return DecipherIndustriesSkill()
