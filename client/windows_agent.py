import socket
import win32evtlog
import time

# Параметры сервера
REMOTE_HOST = '192.168.12.77'
REMOTE_PORT = 61

# Лог событий Windows
system_eventlog = win32evtlog.OpenEventLog(None, 'System')
security_eventlog = win32evtlog.OpenEventLog(None, 'Security')
application_eventlog = win32evtlog.OpenEventLog(None, 'Applitcation')


def win_log_collector():
    flags= win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ#EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    system_events = win32evtlog.ReadEventLog(system_eventlog, flags, 0)
    security_events = win32evtlog.ReadEventLog(security_eventlog, flags, 0)
    application_events = win32evtlog.ReadEventLog(application_eventlog, flags, 0)

    return system_events, security_events, application_events


# Клиент TCP
def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((REMOTE_HOST, REMOTE_PORT))
        while True:
            try:
                events = []
                
                system_events, security_events, application_events = win_log_collector()

                events.extend(system_events)
                events.extend(security_events)
                events.extend(application_events)

                for event in (events):
                    message = f"{event.EventID};{event.EventType};{event.Sid};{event.Reserved};{event.SourceName};{event.ComputerName};{event.StringInserts[0] if event.StringInserts else 'No message'};{event.TimeWritten if event.TimeWritten else '0'}"
                    s.sendall(message.encode('utf-8'))

            except Exception as e:
                print(f"Ошибка при отправке данных: {e}")
            time.sleep(1) # Задержка для экономии ресурсов

client()