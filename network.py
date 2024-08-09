import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "13.53.147.13"  # Public IP AWS
        self.server = "192.168.56.1"  # Local IP Matthias
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.receive_data()
        except socket.error as e:
            print(f"Connection error: {str(e)}")
            return None

    def send(self, data):
        try:
            self.client.sendall(pickle.dumps(data))
            return self.receive_data()
        except socket.error as e:
            print(f"Connection error: {str(e)}")
            return None

    def receive_data(self):
        data = b""
        while True:
            try:
                packet = self.client.recv(2048)
                if not packet:
                    break
                data += packet
                try:
                    return pickle.loads(data)
                except pickle.UnpicklingError:
                    continue
            except socket.error as e:
                print(f"Receive error: {str(e)}")
                break
        return None
