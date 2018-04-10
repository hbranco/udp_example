import socket
from crc16branco import calcByte


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 10000)
# message = "This is the message.  It will be repeated"
dataNoCRC = "mensagem enviada para ser analisada pelo crc16"
crc = 0xFFFF  # inicializa o crc
for ch in dataNoCRC:
    crc = calcByte(ch, crc)
print(crc)

dataNoCRC = dataNoCRC + " " + str(crc)

try:

    # Send data
    print('sending {!r}'.format(dataNoCRC))
    sent = sock.sendto(dataNoCRC.encode('UTF-8'), server_address)

    # Receive response
    print('waiting to receive')
    data, server = sock.recvfrom(4096)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()