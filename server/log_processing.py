import time
import os
import re
import sqlite3
from flask import Flask,jsonify
#def get_db_connection():

app = Flask(__name__)


def connect_to_DB():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row

    return conn


def log_parser(line):
    if "SYSCALL" in line:
        hostname = (re.search(r'node=.+?\s', line)).group(0).strip()
        event_type = (re.search(r'type=.+?\s', line)).group(0).strip()
        pid = (re.search(r'pid=\d+?', line)).group(0).strip()
        ppid = (re.search(r'ppid=\d+?', line)).group(0).strip()
        cmdline = (re.search(r'comm=.+?\s', line)).group(0).strip()
        exe_path = (re.search(r'exe=.+?\s', line)).group(0).strip()

        parsed_log = (hostname, event_type, pid, ppid, cmdline, exe_path)
    
    elif "EXECVE" in line:
        hostname = (re.search(r'node=.+?\s', line)).group(0).strip()
        event_type = (re.search(r'type=.+?\s', line)).group(0).strip()
        cmdargs = (re.search(r'a0.+$', line)).group(0).strip()

        parsed_log = (hostname, event_type, cmdargs)

    else:
        parsed_log = ''

    if parsed_log == None:
        pass
    else:
        return parsed_log


def log_collector(filename):
    with open(filename, 'r') as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            yield line

def push_logs_to_db(logs, conn, type):
    cursor = conn.cursor()
    lox = 'hcgcrgrg'
    try:
        cursor.execute(f"INSERT INTO {type} (logs) VALUES ({lox})")
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
        conn.rollback()

def insert_logs_to_DB(logs, conn):
    #if len(logs) == 6: choose type of logs
       push_logs_to_db(logs, conn, 'Linux')
    # else:
    #     push_logs_to_db(logs, conn, 'Windows')


def log_monitor():
    log_file = '/var/log/audit/audit.log'
    conn = connect_to_DB()

    for line in log_collector(log_file):
        parsed_log = log_parser(line)
        insert_logs_to_DB(parsed_log, conn)
        # check_susp(parsed_log) how postprocessing after sending to DB
        print(parsed_log) # test print


@app.route('/api/records', methods=['GET'])
def get_records():
    conn = connect_to_DB()
    records = conn.execute('SELECT * FROM Linux').fetchall()
    return jsonify([dict(record) for record in records])