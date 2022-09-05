import sys
import json
import datetime
from pprint import pprint

def start(fname):
    with open(fname) as inf:
        records = json.load(inf)
        conversations = records['conversations']
        
        for conversation in conversations:
            participants = {} # chat_id -> name
            
            for participant in conversation[
                'conversation']['conversation']['participant_data']:

                participants[participant['id']['chat_id']] = participant.get(
                    'fallback_name', 'Unknown')

            has_text = False
            for event in conversation['events']:
                if 'chat_message' not in event: continue
                if 'segment' not in event[
                        'chat_message']['message_content']: continue
                
                text = []

                for segment in event[
                        'chat_message']['message_content']['segment']:
                    if segment['type'] == 'TEXT' or segment['type'] == 'LINK':
                        text.append(segment['text'])
                        
                sender = participants.get(
                    event['sender_id']['chat_id'], 'Unknown')

                ts = int(int(event['timestamp'])/1000000)
                dt = datetime.datetime.fromtimestamp(ts).strftime(
                    "%Y-%m-%d %H:%M %p")
                
                print("\n%s (%s):" % (sender, dt))
                for t in text:
                    print("    %s" % t)

                has_text = True

            if has_text:
                print("\n" + "-"*60)

if __name__ == "__main__":
    start(*sys.argv[1:])
