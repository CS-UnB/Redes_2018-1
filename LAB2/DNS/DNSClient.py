from socket import *

serverName = '192.168.1.15'   #colocar o IP da maquina servidor
serverPort = 12000

"""
Recebe como parametro o nome do host, envia a mensagem para o DNS local e
recebe como retorno o endereco IP.
"""
def search_host(hostName):
    hostName = hostName.encode()
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(hostName, (serverName, serverPort))
    try:
        hostAddress, ServerAddress = clientSocket.recvfrom(2048)
    except:
        print("erro")    
    clientSocket.close()
    return hostAddress
