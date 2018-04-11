#!/usr/bin/python
# -*- coding: utf-8 -*-

import _thread
import threading
import logging
import socket
import sys
from crc16branco import calcByte
'''
classe que implementa o servidor UDP com mult threads e CRC 
'''

class parsing():
    def __init__(self):
        logging.info('Initializing Broker')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 10000))
        self.clients_list = []

    def listen_clients(self):
        while True:
            msg, client = self.sock.recvfrom(4096)
            logging.info('Received data from client %s: %s', client, msg)
            t = threading.Thread(target=self.startParsing, args=(msg, client))
            t.start()


    def startParsing(self, con, cliente):
        while True:
            data = con
            if not data:
                break
            if type(data) == bytes:
                data = data.decode("utf-8")
                # data = data.split()
                print("Dados Convertidos para UTF-8: ", data)

            #print("Dados que chegaram: ",data)
            try:
                dataCRC = data[-5::]
                dataNoCRC = data[:-5]
                dataNoCRC = dataNoCRC.rstrip(" ")
                print(dataNoCRC)

                crc = 0xFFFF  # inicializa o crc
            except ValueError as e:
                print(e)
                print("Finalizando conexao do cliente", cliente)
                self.sock.sendto("CRC INVALIDO".encode('UTF-8'), ip)
                self.sock.close()
                _thread.exit()
                sys.exit(1)

            for ch in dataNoCRC:
                crc = calcByte(ch, crc)
            # falha do crc sai fora do parser
            if int(crc) != int(dataCRC):
                print("falaha do crc")
                print("crc calculado: " + str(crc))
                print("CRC recebido: "+ dataCRC)
                # nack = '\x15'
                nack = "Mensagem recebida! CRC Invalido"
                sock.sendto(nack.upper().encode('UTF-8'), cliente)
                self.sock.sendto(nack.upper().encode('UTF-8'), ip)
                # con.sendall(nack.upper().encode('UTF-8'))
                break
                sock.close()
                _thread.exit_thread()
            else:
              #  print("crc deu certo")
              #   ack = '\x06'
                ack = "Mensagem recebida! CRC VALIDO"
                self.sock.sendto(ack.upper().encode('UTF-8'), cliente)
                dadosParser = dataNoCRC.split()
                print(dadosParser)
                break

'''
inicialização do parser
'''
if __name__ == '__main__':
    # Make sure all log messages show up
    logging.getLogger().setLevel(logging.DEBUG)

    b = parsing()
    b.listen_clients()
    pass