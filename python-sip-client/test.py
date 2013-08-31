from client_socket import *
from register_request import *

def main(proxy, display_name, extension):
    cs = None
    while True:
        try:
            if cs is None:
                cs = ClientSocket(proxy, 5060)
                network = cs.connect()
                if network != "Not connected":
                    rr = RegisterRequest(proxy, network[0][0], network[0][1], display_name, extension, 1)
                    req = rr.create()
                    cs.send(rr.create())
            else:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("Kbd interrupt handled")
            if cs is not None:
                cs.stop()
                cs.close()
            break

    
