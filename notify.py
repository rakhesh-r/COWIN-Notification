import atexit
from datetime import datetime
import hashlib
from typing import List

import telebot as tb
import os
from dotenv import load_dotenv
import logging
import sched
import time
import utils
import cowin_api
import http_client

load_dotenv()
API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')
print('Key' + API_KEY)
s = sched.scheduler(time.time, time.sleep)
bot = tb.TeleBot(API_KEY, parse_mode='markdown')

# channels
CH_ADMIN = '-1001204018026'
CH_DK_45_1 = '@cowindk45dose1'
CH_DK_45_2 = '@cowindk45dose2'
CH_DK_18_1 = '@cowindk18dose1'
CH_DK_18_2 = '@cowindk18dose2'

p_message_dk_m_18_1, p_message_dk_m_18_2, p_message_dk_m_45_1, p_message_dk_m_45_2 = "init", "init", "init", "init"


def get_message1(center_name, center_block, date, vaccine, capacity, address, pin, time_from, time_to, fee):
    return f"""
*◉ {center_name} - {center_block}*
 ◦ Date : *{date}*
 ◦ Vaccine : *{vaccine}*
 ◦ Available slots : *{capacity}*
 ◦ Time : *{time_from} - {time_to}*
 ◦ Fee type : *{fee}*
 ◦ Address  : {address}, {pin}
"""


def get_message2(center_name, center_block, date, vaccine, capacity, address, pin, time_from, time_to):
    return f"""
*◉ {center_name} - {center_block}*
 ◦ Date : *{date}*
 ◦ Vaccine : *{vaccine}*
 ◦ Available slots : *{capacity}*
 ◦ Time : *{time_from} - {time_to}*
 ◦ Address  : {address}, {pin}
"""


def get_message_footer():
    return """
    
[Link to CoWIN portal](https://selfregistration.cowin.gov.in/) 
"""


def get_message_header(count: int = 0):
    if count > 1:
        return """Vaccination centre,
"""
    else:
        return """Vaccination centres,
"""


def get_messages(data: dict):
    messages_18_plus_dose_1 = []
    messages_18_plus_dose_2 = []
    messages_45_plus_dose_1 = []
    messages_45_plus_dose_2 = []
    for center in data['centers']:
        for session in center['sessions']:
            available_capacity_dose1 = session['available_capacity_dose1']
            if available_capacity_dose1 > 0:
                # print(available_capacity_dose1)
                if session['min_age_limit'] == 45:
                    if center['fee_type'] == "Free":
                        messages_45_plus_dose_1.append(
                            get_message2(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose1, center['address'], center['pincode'], center['from'],
                                         center['to']))
                    else:
                        messages_45_plus_dose_1.append(
                            get_message1(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose1, center['address'], center['pincode'], center['from'],
                                         center['to'], center['fee_type']))
                elif session['min_age_limit'] == 18:
                    if center['fee_type'] == "Free":
                        messages_18_plus_dose_1.append(
                            get_message2(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose1, center['address'], center['pincode'], center['from'],
                                         center['to']))
                    else:
                        messages_18_plus_dose_1.append(
                            get_message1(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose1, center['address'], center['pincode'], center['from'],
                                         center['to'], center['fee_type']))
            available_capacity_dose2 = session['available_capacity_dose2']
            if available_capacity_dose2 > 0:
                # print(available_capacity_dose2)
                if session['min_age_limit'] == 45:
                    if center['fee_type'] == "Free":
                        messages_45_plus_dose_2.append(
                            get_message2(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose2, center['address'], center['pincode'], center['from'],
                                         center['to']))
                    else:
                        messages_45_plus_dose_2.append(
                            get_message1(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose2, center['address'], center['pincode'], center['from'],
                                         center['to'], center['fee_type']))
                elif session['min_age_limit'] == 18:
                    if center['fee_type'] == "Free":
                        messages_18_plus_dose_2.append(
                            get_message2(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose2, center['address'], center['pincode'], center['from'],
                                         center['to']))
                    else:
                        messages_18_plus_dose_2.append(
                            get_message1(center['name'], center['block_name'], session['date'], session['vaccine'],
                                         available_capacity_dose2, center['address'], center['pincode'], center['from'],
                                         center['to'], center['fee_type']))
    return messages_18_plus_dose_1, messages_18_plus_dose_2, messages_45_plus_dose_1, messages_45_plus_dose_2


def is_message_changed(message: str, old_message: str):
    hash_object_new = hashlib.sha256(message.encode())
    hex_dig_new = hash_object_new.hexdigest()
    # print(hex_dig_new)
    hash_object_old = hashlib.sha256(old_message.encode())
    hex_dig_old = hash_object_old.hexdigest()
    # print(hex_dig_old)
    if hex_dig_old == hex_dig_new:
        return False
    else:
        return True


def send_message(dk_m_18_1: List[str], dk_m_18_2: List[str], dk_m_45_1: List[str], dk_m_45_2: List[str]):
    for message in dk_m_18_1:
        bot.send_message(CH_DK_18_1,
                         message)
    for message in dk_m_18_2:
        bot.send_message(CH_DK_18_2,
                         message)
    for message in dk_m_45_1:
        bot.send_message(CH_DK_45_1,
                         message)
    for message in dk_m_45_2:
        bot.send_message(CH_DK_45_2,
                         message)


def send_message2(dk_m_18_1: List[str], dk_m_18_2: List[str], dk_m_45_1: List[str], dk_m_45_2: List[str]):
    global p_message_dk_m_18_1, p_message_dk_m_18_2, p_message_dk_m_45_1, p_message_dk_m_45_2
    message = ""
    if len(dk_m_18_1) > 0:
        for tmp_msg in dk_m_18_1:
            message = message + tmp_msg
        message = get_message_header() + message + get_message_footer()
        print("CH_DK_18_1" + message)
        if is_message_changed(message, p_message_dk_m_18_1):
            bot.send_message(CH_DK_18_1,
                             message)
            p_message_dk_m_18_1 = message
    message = ""
    if len(dk_m_18_2) > 0:
        for tmp_msg in dk_m_18_2:
            message = message + tmp_msg
        message = get_message_header() + message + get_message_footer()
        print("CH_DK_18_2" + message)
        if is_message_changed(message, p_message_dk_m_18_2):
            bot.send_message(CH_DK_18_2,
                             message)
            p_message_dk_m_18_2 = message
    message = ""
    if len(dk_m_45_1) > 0:
        for tmp_msg in dk_m_45_1:
            message = message + tmp_msg
        message = get_message_header() + message + get_message_footer()
        print("CH_DK_45_1" + message)
        if is_message_changed(message, p_message_dk_m_45_1):
            bot.send_message(CH_DK_45_1,
                             message)
            p_message_dk_m_45_1 = message
    message = ""
    if len(dk_m_45_2) > 0:
        for tmp_msg in dk_m_45_2:
            message = message + tmp_msg
        message = get_message_header() + message + get_message_footer()
        print("CH_DK_45_2" + message)
        if is_message_changed(message, p_message_dk_m_45_2):
            bot.send_message(CH_DK_45_2,
                             message)
            p_message_dk_m_45_2 = message


def do_something(sc):
    print("Doing stuff...")
    # do your stuff
    # bot.send_message("-1001204018026", "New hello")
    dk_m_18_1, dk_m_18_2, dk_m_45_1, dk_m_45_2 = get_messages(
        cowin_api.get_calendar_data_by_district_id(cowin_api.DISTRICT_DK, utils.getDateNow()))
    bot.send_message(CH_ADMIN, f"""
{datetime.now().strftime("%H:%M:%S")}
dk_m_18_1 = {len(dk_m_18_1)}
dk_m_18_2 = {len(dk_m_18_1)}
dk_m_45_1 = {len(dk_m_45_1)}
dk_m_45_2 = {len(dk_m_45_2)}""")
    send_message2(dk_m_18_1, dk_m_18_2, dk_m_45_1, dk_m_45_2)
    # do your stuff
    s.enter(60, 1, do_something, (sc,))


@atexit.register
def exit_handler():
    print("Notification push ended at " + datetime.now().strftime("%H:%M:%S"))
    bot.send_message(CH_ADMIN, "Notification push ended at " + datetime.now().strftime("%H:%M:%S"))


print("Notification push started at " + datetime.now().strftime("%H:%M:%S"))
bot.send_message(CH_ADMIN, "Notification push started at " + datetime.now().strftime("%H:%M:%S"))
s.enter(1, 1, do_something, (s,))
s.run()

# get_message_agelimit_45(cowin_api.get_calendar_data_by_district_id(cowin_api.DISTRICT_DK, utils.getDateNow()))
# c = 10;
# message_m = f"""
# *Pudu PHC - Bantwal*
#  Date : *30-09-1991*
#  Vaccine : *COVAXIN*
#  Available slots : *{c}*
#  Address  : Near Bus Stop Maripalla Pudu, 574143
#  Time : *10:00:00 to 15:30:00*
#  Fee : Free
#
#  [Link to CoWIN portal](https://selfregistration.cowin.gov.in/)
#
#  [Pudu PHC - Bantwal](https://www.google.com/maps/dir/?api=1&destination=12%2C74)
# """
# m_18_1, m_18_2, m_45_1, m_45_2 = get_messages(
#     cowin_api.get_calendar_data_by_district_id(cowin_api.DISTRICT_DK, utils.getDateNow()))
# for message_m in m_18_2:
#     bot.send_message("-1001204018026",
#                      message_m)
# for message_m in m_18_1:
#     bot.send_message("-1001204018026",
#                      message_m)
# for message_m in m_45_1:
#     bot.send_message("-1001204018026",
#                      message_m)
# for message_m in m_45_2:
#     bot.send_message("-1001204018026",
#                      message_m)
# bot.send_message(CH_TEST,
#                  get_message_header() + get_message2("TEST", "Mangalore", "11-11-2021", "COVAXIN", "10", "Address",
#                                                      "12345", "11:00",
#                                                      "12:00") + get_message1("TEST2", "Mangalore", "11-11-2021",
#                                                                              "COVAXIN", "10",
#                                                                              "Address", "12345 hfjdhjd fdjh dfjd fdjhd jhfdjfhjd fhjhfjd hfjdhf", "11:00",
#                                                                              "12:00", "Free") + get_message_footer())
