import socket
import netifaces as neti

self_ip = socket.gethostbyname(socket.gethostname())
network_setting = None
for inter in neti.interfaces():
    if inter is not None:
        network_setting = neti.ifaddresses(inter).get(neti.AF_INET)
        if network_setting is not None:
            if network_setting[0].get('addr') == self_ip:
                network_setting = network_setting[0]
                break

print(self_ip)
print(network_setting)

form = input("Broadcasting(b) or Recieving(r): ")

test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

if form == "b":
    test_socket.sendto(b'This is a test', (network_setting['broadcast'], 8080))

elif form == "r":
    test_socket.bind((network_setting['broadcast'], 8080))
    print(test_socket.recv(len(b'This is a test')))

else:
    print("Please correct option")
