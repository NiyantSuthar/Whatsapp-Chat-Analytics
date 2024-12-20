import re
import pandas as pd


def preprocess(data):
    # Adjusted pattern for the new format including AM/PM notation
    pattern = r'(?i)\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime format (adjusting for AM/PM format)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        # Split the message into user and content
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # If user exists in the message
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # Group notifications
            users.append('group_notification')
            messages.append(entry[0])

    # Add user and message columns to DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    # Add additional time-related columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df