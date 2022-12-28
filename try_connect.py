from connection import connection


test=connection("192.168.4.1",23)

test_client_single=test.connectSock()
test_client_mul=test.multiSock()
