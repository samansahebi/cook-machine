import socket
import json


class POSRequest:
    def __init__(self):
        self.ip = "192.168.1.134"
        self.port = 1362

    def send_request(self, amount: int) -> dict:
        data = {
            "cmd": 10,
            "amount": amount,
            "service": "000000",
            "sign": "899|123456789",
            "mti": 200,
            "pin": "1",
            "swipe": "1"
        }

        json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=True)
        json_bytes = json_str.encode('utf-8')
        length = f"{len(json_bytes):04d}".encode('ascii')
        payload = length + json_bytes

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.settimeout(30)
        sock.connect((self.ip, self.port))
        sock.sendall(payload)

        try:
            resp_bytes = sock.recv(4096)
            length = int(resp_bytes[:4].decode('ascii'))
            json_bytes = resp_bytes[4:4 + length]
            data = json.loads(json_bytes.decode('utf-8'))
            sock.close()
            return data
        except socket.timeout:
            sock.close()
            return {"resp": "timeout"}


if __name__ == "__main__":
    pos = POSRequest()
    res = pos.send_request(15000)
    print(res)