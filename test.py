import sched
import time
import imgkit
import hashlib

# s = sched.scheduler(time.time, time.sleep)
#
#
# def do_something(sc):
#     print("Doing stuff...")
#     # do your stuff
#     s.enter(5, 1, do_something, (sc,))


# imgkit.from_string("""
# <h3><strong style="font-size: 14px;"><img src="https://www.cowin.gov.in/assets/images/covid19logo.jpg" alt="" width="104" height="30" /></strong></h3>
# <h3><span style="color: #003366;">Bantwal</span> UPHC - Bantwal</h3>
# <ul>
# <li>Date<strong>: 13-06-2021</strong></li>
# <li>Vaccine : <strong>COVAXIN</strong></li>
# <li>Available slots : <strong>90</strong></li>
# <li>Time : <strong>10:00:00 - 15:00:00</strong></li>
# <li>Address : Polali Dwara, 574219</li>
# </ul>
# """, 'out.png')


def is_message_changed(message: str, old_message: str):
    hash_object_new = hashlib.sha256(message.encode())
    hex_dig_new = hash_object_new.hexdigest()
    print(hex_dig_new)
    hash_object_old = hashlib.sha256(old_message.encode())
    hex_dig_old = hash_object_old.hexdigest()
    print(hex_dig_old)
    if hex_dig_old == hex_dig_new:
        return False
    else:
        return True


#print(is_message_changed("test", "tessdsdsdst"))

def get_message2(center_name, center_block, date, vaccine, capacity, address, pin, time_from, time_to):
    return f"""
*{center_name} - {center_block}*
 Date : *{date}*
 Vaccine : *{vaccine}*
 Available slots : *{capacity}*
 Time : *{time_from} - {time_to}*
 Address  : {address}, {pin}
"""

