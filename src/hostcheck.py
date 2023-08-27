import socket
import logic.test


def main():
    hostname = socket.gethostname()
    print("Hostname:", hostname)


if __name__ == '__main__':
    main()
