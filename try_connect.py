from connection import connection


test=connection()

test_client_single=test.connectSock()
test_client_mul=test.multiSock()
