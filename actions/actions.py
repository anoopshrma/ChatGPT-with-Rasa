# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import requests


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
    
    # Get user message from Rasa tracker
        user_message = tracker.latest_message.get('text')
        print(user_message)

    # def get_chatgpt_response(self, message):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer ADD_YOUR_OPENAI_API_KEY_HERE',
            'Content-Type': 'application/json'
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [   {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user query'}
                            {'role': 'user', 'content': 'You: ' + user_message}
                            ],
            'max_tokens': 100
        }
        response = requests.post(url, headers=headers, json=data)
                # response = requests.post(api_url, headers=headers, json=data)

        if response.status_code == 200:
            chatgpt_response = response.json()
            message = chatgpt_response['choices'][0]['message']['content']
            dispatcher.utter_message(message)
        else:
            # Handle error
            return "Sorry, I couldn't generate a response at the moment. Please try again later."
        
                # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
      
      
      
