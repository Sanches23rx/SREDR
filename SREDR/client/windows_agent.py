import socket
import win32evtlog
import time
import os
from multiprocessing import Process
import subprocess

uniqID='1a2b3c4d'

# Параметры сервера
#REMOTE_HOST = '192.168.12.77'
#REMOTE_PORT = 61

REMOTE_HOST = '192.168.1.11'
REMOTE_PORT = 61

#events
collect_evt_list = ['1102', '4624', '4625', '4657', '4663', '4688', '4700', '4702', '4719', '4720', '4722', '4723', '4724', '4727', '4728', '4732', '4735', '4737', '4739', '4740', '4754', '4755', '4756', '4767', '4799', '4825', '4946', '4948', '4956', '5024', '5033', '8001', '8002', '8003', '8004', '8005', '8006', '8007', '8222']

# Лог событий Windows
system_eventlog = win32evtlog.OpenEventLog(None, 'System')
security_eventlog = win32evtlog.OpenEventLog(None, 'Security')
application_eventlog = win32evtlog.OpenEventLog(None, 'Applitcation')

def event_handler(): #ОБработка правил
     #
     pass

def win_log_collector():
    flags= win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ#EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    system_events = win32evtlog.ReadEventLog(system_eventlog, flags, 0)
    security_events = win32evtlog.ReadEventLog(security_eventlog, flags, 0)
    application_events = win32evtlog.ReadEventLog(application_eventlog, flags, 0)

    return system_events, security_events, application_events

def get_hostinfo():
    #uniqID
    system_name = subprocess.check_output(['cmd', '/c', 'hostname'])
    os_info = subprocess.check_output(['cmd', '/c', 'ver'])
    
    #currentuser = 


    data_hash = 

# Клиент TCP
def client_run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((REMOTE_HOST, REMOTE_PORT))
        s.sendall(bytes('!INIT,' + '\n', encoding='utf-8'))
        while True:
            try:
                events = []
                
                system_events, security_events, application_events = win_log_collector()

                events.extend(system_events)
                events.extend(security_events)
                events.extend(application_events)

                for event in (events):
                    if str(event.EventID) in collect_evt_list:
                        message = f"{event.EventID};{event.EventType};{event.Sid};{event.Reserved};{event.SourceName};{event.ComputerName};{event.StringInserts[0] if event.StringInserts else 'No message'};{event.TimeWritten if event.TimeWritten else '0'}"
                        print(message[:140])
                        #s.sendall(message.encode('utf-8'))

            except Exception as e:
                print(f"Ошибка при отправке данных: {e}")
            time.sleep(1) # Задержка для экономии ресурсов


if __name__ == '__main__':
    p1 = Process(target=client_run)
    p1.start()
    #p2 = Process(target=log)
    #p2.start()
    #p1.join()
    #p2.join()
    #app.run(debug=True)