import socket
import threading

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.settimeout(1)
        
        s.connect((target, port))
        
        print(f"Port {port} is open")
        
        s.close()
    except:
        pass 

def port_scan(target, start_port, end_port):
    print(f"Scanning target {target} for ports {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        threading.Thread(target=scan_port, args=(target, port)).start()

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    port_scan(target_ip, start_port, end_port)
