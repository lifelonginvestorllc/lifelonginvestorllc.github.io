from datetime import datetime
import pandas as pd
from telethon.sync import TelegramClient
import csv
from zoneinfo import ZoneInfo

# Credentials from https://my.telegram.org
api_id = 29514174
api_hash = '896f7987b68ec68a1694209fc72049e8'
target = -609042762 # telegram group id
saveMessageToFile = False

# Start client session
client = TelegramClient('my_session', api_id, api_hash)

with client:
    messages = []
    for message in client.iter_messages(target, limit=2000):
        # Convert UTC to Eastern Time (or your local time)
        local_time = message.date.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York"))

        messages.append({
            'date': local_time,
            'sender_id': message.sender_id,
            'text': message.text.strip(),
        })
    if saveMessageToFile:
        with open('liats_live_messages.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['date', 'sender_id', 'text'])
            writer.writeheader()
            writer.writerows(messages)
    df = pd.DataFrame(messages)
    df['date'] = pd.to_datetime(df['date'])

    # Date range to filter (local time)
    start_date = datetime(2025, 1, 1, tzinfo=ZoneInfo("America/New_York"))
    end_date = datetime(2025, 6, 20, 23, 59, 59, tzinfo=ZoneInfo("America/New_York"))

    mask = (
        df['text'].str.contains("Daily Report:") &
        (df['date'] >= start_date) &
        (df['date'] <= end_date) &
        (df['date'].dt.hour == 18) &
        (df['date'].dt.minute == 0)
    )

    filtered = df[mask]

    with open('../dailyReport.txt', 'a', encoding='utf-8') as f:
        for _, row in filtered.sort_values(by='date').iterrows():
            # full_text = row['text']
            # start_idx = full_text.find("LifelongInvest")
            f.write(f"{row['date'].strftime('%Y-%m-%d %H:%M:%S')} - {row['text']}\n")

    print("Done")