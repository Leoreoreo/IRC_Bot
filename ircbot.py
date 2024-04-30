import os
import socket
import ssl

# Constants
HOST = 'chat.ndlug.org'
PORT = 6697
# NICK = f'ircle-{os.environ["USER"]}'
NICK = 'SomeRandomBot'

# Functions
def send_message(ssl_stream, channel, message):
    ssl_stream.write(f"PRIVMSG {channel} :{message}\r\n")
    ssl_stream.flush()

def ircle():
    # Connect to IRC server
    ssl_context = ssl.create_default_context()
    tcp_socket = socket.create_connection((HOST, PORT))
    ssl_socket = ssl_context.wrap_socket(tcp_socket, server_hostname=HOST)
    ssl_stream = ssl_socket.makefile('rw')

    # Identify ourselves
    ssl_stream.write(f'USER {NICK} 0 * :{NICK}\r\n')
    ssl_stream.write(f'NICK {NICK}\r\n')
    ssl_stream.flush()

    # Join #bots channel
    ssl_stream.write(f'JOIN #bots\r\n')
    ssl_stream.flush()

    # Read and respond to messages
    while True:
        message = ssl_stream.readline().strip()
        print(message)  # Log incoming messages

        # Respond to "!hello" command
        if '!hello' in message:
            send_message(ssl_stream, "#bots", "Hello there.")
        elif '!catsay' in message:
            send_message(ssl_stream, "#bots", "meow")


# Main Execution
def main():
    ircle()

if __name__ == '__main__':
    main()
