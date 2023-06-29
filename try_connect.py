from connection import Connection


test = Connection()

test_client_single = test.connectSock()
test_client_mul = test.multiSock()
