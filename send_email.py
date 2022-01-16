import os 
import smtplib

from email.message import EmailMessage
from typing import List

# getting email address and password from system variables
EMAIL_ADDRESS = os.environ.get('GMAIL_PYTHON_USER')
EMAIL_PASSWORD = os.environ.get('GMAIL_PYTHON_PASSWORD')


def generate_timeslots(start_hour: int = 6, timeslots_num: int = 18):

    timeslots_dict = dict()
    for i in range(0, timeslots_num):
        if i + start_hour <= 23:
            timeslots_dict[i] = f'{i+start_hour}:00-{i++start_hour+1}:00'
        else:
            timeslots_dict[i] = f'{i + start_hour-24}:00-{i + +start_hour + 1 - 24}:00'

    return timeslots_dict


class ClientsEmail:
    def __init__(self, first_name, second_name, email, trainings):
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.trainings = trainings  # list (LessonType, Day, Hour)


lesson_types = {0: 'Cullulite Killer', 1: 'Zumba', 2: 'Zumba Advanced', 3: 'Fitness', 4: 'Crossfit',
                5: 'Brazilian Butt', 6: 'Pilates', 7: 'City Pump', 8: 'Stretching', 9: 'Yoga'}

timeslots_dict = generate_timeslots(start_hour=6, timeslots_num=18)

client1 = ClientsEmail('Kacper', 'Motyka', 'kmotyka2000@gmail.com', [('Pilates', 'Wed', '16:00-17:00'), ('Pump', 'Tue', '17:00-18:00')])
client2 = ClientsEmail('Kacper', 'Motyka', 'kacpermotyka4@gmail.com', [('Essa', 'Wed', '16:00-17:00'), ('Essa23', 'Tue', '17:00-18:00')])


def send_emails_to_clients(clients: List[ClientsEmail]):

    for client in clients:

        msg = EmailMessage()
        msg['Subject'] = 'Your trainings were scheduled!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = client.email

        msg_str = f'Dear {client.first_name} {client.second_name},\n\nYour trainings: \n\n'
        for training in client.trainings:
            msg_str += f'\t{training[0]} - Day: {training[1]} Hours: {training[2]}\n'
        msg_str += '\nLooking forward to meeting you!'
        msg.set_content(msg_str)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # login to gmail account using system variables
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            # sending message
            smtp.send_message(msg)






