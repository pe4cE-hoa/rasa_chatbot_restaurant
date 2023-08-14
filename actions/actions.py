# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from datetime import datetime, timedelta, time

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]
menu_collection = db["menu"]
feedback_collection = db["feedback"]
bookings_collection = db["bookings"]
table_manager = client["table_manager"]
seat_count = 3 # chỉ số test
seat_count_available = 0

ALLOWED_DATE_BOOKING = ["hôm nay", "ngày mai", "ngày kia"]
ALLOWED_TIME_BOOKING = ["19", "20", "21", "22", "23"]


class ValidateBookingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_booking_form"

    def validate_date_booking(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `date_booking` value."""

        if slot_value.lower() not in ALLOWED_DATE_BOOKING:
            dispatcher.utter_message(text=f"Xin lỗi hiện tại nhà hàng chỉ đặt bàn trong vòng 2 ngày.")
            return {"date_booking": None}
        dispatcher.utter_message(text=f"OK! bạn đã đặt bàn vào {slot_value}.")
        return {"date_booking": slot_value}

    def validate_time_booking(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `time_booking` value."""

        if slot_value.lower() not in ALLOWED_TIME_BOOKING:
            dispatcher.utter_message(text=f"Xin lỗi hiện tại chúng tôi chỉ đặt bàn từ {ALLOWED_TIME_BOOKING[0]} đến {ALLOWED_TIME_BOOKING[1]}")
            return {"time_booking": None}
        dispatcher.utter_message(text=f"OK! bạn đã đặt bàn vào lúc {slot_value}.")
        return {"time_booking": slot_value}
    