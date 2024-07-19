import socket

def check_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Timeout de 5 segundos
    is_connected = False

    try:
        sock.connect((ip, port))
        is_connected = True
    except (socket.timeout, socket.error):
        pass
    finally:
        sock.close()

    return is_connected