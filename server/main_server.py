from multiprocessing import Process
from log_processing import log_monitor
from win_server import tcp_server_for_win_logs


def main():
    p1 = Process(target=tcp_server_for_win_logs)
    p1.start()
    p2 = Process(target=log_monitor)
    p2.start()
    p1.join()
    p2.join()


main()