from socket import *

"""
Registra no Banco de Dados um registro contendo nome, valor e tipo.
Nome ->
Valor ->
Tipo ->
"""
def registrar_recurso(nome, valor, tipo):
    registro = "{}, {}, {}\n".format(nome, valor, tipo)
    fl = open('db.txt', 'a')
    fl.write(registro)
    fl.close()

"""
Procura no banco de dados pelo registro de recursos do
nome passado como parametro
"""
def search_rr_in_db(hostName):
    fl = open('db.txt', 'r+')
    bd = fl.readlines()
    for item in bd:
        nome = item.split(',')[0]
        valor = item.split(',')[1]
        #tipo = item.split(',')[2].split('\n')[0]
        if(nome == hostName):
            fl.close()
            return valor.encode()
    fl.close()
    return None

"""
Recebe um hostName e procura no BD pelo registro, se nao existir no BD eh
feita uma consulta ao servidor nao local. Retorna o Registro de recursos.
"""
if(__name__ == "__main__"):
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    print('The server is ready to receive')
    while 1:
        hostName, clientAddress = serverSocket.recvfrom(2048)
        registro_recursos = search_rr_in_db(hostName.decode("utf-8"))

        if(registro_recursos is None):
            try:
                registro_recursos = gethostbyname(hostName.decode("utf-8")) #da erro se host nao existe ou esta sem conexao
                serverSocket.sendto(registro_recursos.encode(), clientAddress)
            except:
                serverSocket.sendto("Registro nao encontrado".encode(), clientAddress)
        else:
            serverSocket.sendto(registro_recursos, clientAddress)
