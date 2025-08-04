#!/usr/bin/env python3
"""
Network Protocol Educational Simulator

This script is for EDUCATIONAL PURPOSES ONLY. It demonstrates how different network
protocols work by sending legitimate requests at a controlled rate.

WARNING: Using this script against any target without explicit permission is illegal
and unethical. Only use against your own servers or in controlled lab environments.

This script is designed with built-in rate limiting and safety features to prevent
accidental misuse.

Usage:
    python network_protocol_simulator.py --target 127.0.0.1 --port 8080 --protocol http --requests 5 --delay 1
"""

import argparse
import socket
import ssl
import time
import sys
import random
import requests
from datetime import datetime

# SAFETY FEATURES
MAX_REQUESTS = 20  # Maximum number of requests allowed
MIN_DELAY = 1.0    # Minimum delay between requests in seconds
WHITELIST = ["127.0.0.1", "localhost"]  # Only allow local testing by default

class ProtocolSimulator:
    def __init__(self, target, port, protocol, num_requests, delay, path="/"):
        self.target = target
        self.port = port
        self.protocol = protocol.lower()
        self.num_requests = min(num_requests, MAX_REQUESTS)  # Safety limit
        self.delay = max(delay, MIN_DELAY)  # Safety limit
        self.path = path
        self.sent_requests = 0
        self.successful_requests = 0
        
        # Safety check for target
        if target not in WHITELIST:
            print(f"\033[91mERROR: Target {target} is not in the whitelist.\033[0m")
            print(f"For educational purposes, this script only allows connections to: {', '.join(WHITELIST)}")
            print("Edit the WHITELIST in the script if you need to test against other targets you control.")
            sys.exit(1)
    
    def run_simulation(self):
        """Run the protocol simulation"""
        print(f"\n{'='*60}")
        print(f"NETWORK PROTOCOL SIMULATOR - EDUCATIONAL USE ONLY")
        print(f"{'='*60}")
        print(f"Target: {self.target}:{self.port}")
        print(f"Protocol: {self.protocol.upper()}")
        print(f"Requests: {self.num_requests}")
        print(f"Delay: {self.delay} seconds")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        if self.protocol == "http":
            self.simulate_http()
        elif self.protocol == "https":
            self.simulate_https()
        elif self.protocol == "icmp":
            self.simulate_icmp()
        else:
            print(f"Unsupported protocol: {self.protocol}")
            return
        
        self.print_summary()
    
    def simulate_http(self):
        """Simulate HTTP requests"""
        print("Simulating HTTP protocol...\n")
        
        for i in range(self.num_requests):
            try:
                start_time = time.time()
                url = f"http://{self.target}:{self.port}{self.path}"
                
                print(f"Request {i+1}/{self.num_requests} to {url}")
                
                # Send the request with a random user agent for educational demonstration
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                response = requests.get(url, headers=headers, timeout=5)
                
                elapsed = time.time() - start_time
                self.sent_requests += 1
                
                # Process response
                print(f"  Status: {response.status_code}")
                print(f"  Time: {elapsed:.4f} seconds")
                print(f"  Size: {len(response.content)} bytes")
                
                if 200 <= response.status_code < 400:
                    self.successful_requests += 1
                
                # Educational output - show headers
                print("  Headers sent:")
                for key, value in headers.items():
                    print(f"    {key}: {value}")
                
                print("  Headers received:")
                for key, value in response.headers.items():
                    print(f"    {key}: {value}")
                
                print("\n")
                
                # Respect the delay between requests
                if i < self.num_requests - 1:
                    print(f"Waiting {self.delay} seconds before next request...")
                    time.sleep(self.delay)
                    
            except requests.exceptions.RequestException as e:
                print(f"  Error: {e}\n")
    
    def simulate_https(self):
        """Simulate HTTPS requests"""
        print("Simulating HTTPS protocol...\n")
        
        for i in range(self.num_requests):
            try:
                start_time = time.time()
                url = f"https://{self.target}:{self.port}{self.path}"
                
                print(f"Request {i+1}/{self.num_requests} to {url}")
                
                # Send the request with a random user agent
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                response = requests.get(url, headers=headers, timeout=5, verify=False)
                
                elapsed = time.time() - start_time
                self.sent_requests += 1
                
                # Process response
                print(f"  Status: {response.status_code}")
                print(f"  Time: {elapsed:.4f} seconds")
                print(f"  Size: {len(response.content)} bytes")
                
                if 200 <= response.status_code < 400:
                    self.successful_requests += 1
                
                # Educational output - show SSL/TLS information
                print("  TLS Info:")
                print(f"    Protocol: {response.raw.connection.sock.version() if hasattr(response.raw, 'connection') and hasattr(response.raw.connection, 'sock') else 'Unknown'}")
                
                print("  Headers sent:")
                for key, value in headers.items():
                    print(f"    {key}: {value}")
                
                print("  Headers received:")
                for key, value in response.headers.items():
                    print(f"    {key}: {value}")
                
                print("\n")
                
                # Respect the delay between requests
                if i < self.num_requests - 1:
                    print(f"Waiting {self.delay} seconds before next request...")
                    time.sleep(self.delay)
                    
            except requests.exceptions.RequestException as e:
                print(f"  Error: {e}\n")
    
    def simulate_icmp(self):
        """Simulate ICMP (ping) requests using socket"""
        print("Simulating ICMP protocol...\n")
        print("Note: This is a simplified ICMP simulation for educational purposes.")
        print("For a real ICMP implementation, you would need raw socket access (requires root/admin).\n")
        
        for i in range(self.num_requests):
            try:
                start_time = time.time()
                
                print(f"Request {i+1}/{self.num_requests} to {self.target}")
                
                # Create a simple socket connection to simulate network activity
                # This doesn't actually send ICMP packets but demonstrates the concept
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                
                # Try to connect to port 7 (echo) or the specified port
                connect_port = 7 if self.port == 0 else self.port
                result = s.connect_ex((self.target, connect_port))
                
                elapsed = time.time() - start_time
                self.sent_requests += 1
                
                if result == 0:
                    status = "Port open (connection successful)"
                    self.successful_requests += 1
                else:
                    status = f"Port closed or filtered (error code: {result})"
                
                print(f"  Status: {status}")
                print(f"  Time: {elapsed:.4f} seconds")
                
                # Educational output - explain what's happening
                print("  Note: This is simulating the concept of ICMP by checking port connectivity.")
                print("  A real ICMP ping would use raw sockets to send ICMP echo request packets.")
                print("  For a true ICMP implementation, use the built-in 'ping' command.")
                
                s.close()
                print("\n")
                
                # Respect the delay between requests
                if i < self.num_requests - 1:
                    print(f"Waiting {self.delay} seconds before next request...")
                    time.sleep(self.delay)
                    
            except socket.error as e:
                print(f"  Error: {e}\n")
    
    def print_summary(self):
        """Print a summary of the simulation"""
        print(f"\n{'='*60}")
        print("SIMULATION SUMMARY")
        print(f"{'='*60}")
        print(f"Protocol: {self.protocol.upper()}")
        print(f"Target: {self.target}:{self.port}")
        print(f"Requests sent: {self.sent_requests}")
        print(f"Successful requests: {self.successful_requests}")
        print(f"Success rate: {(self.successful_requests/self.sent_requests)*100 if self.sent_requests > 0 else 0:.2f}%")
        print(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        print("EDUCATIONAL NOTES:")
        print("1. This script demonstrates basic network protocol behavior.")
        print("2. For HTTP/HTTPS, it shows how headers, status codes, and content work.")
        print("3. For ICMP, it simulates the concept of checking host availability.")
        print("4. Real-world applications would implement proper error handling and retries.")
        print("5. Network diagnostics should always be performed with permission and care.")
        print(f"{'='*60}\n")

# List of common user agents for educational demonstration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def main():
    # Display educational disclaimer
    print("\n" + "*"*80)
    print("*" + " "*78 + "*")
    print("*  NETWORK PROTOCOL SIMULATOR - FOR EDUCATIONAL PURPOSES ONLY" + " "*22 + "*")
    print("*" + " "*78 + "*")
    print("*  WARNING: This tool should only be used in controlled environments" + " "*19 + "*")
    print("*  against targets you own or have explicit permission to test." + " "*23 + "*")
    print("*" + " "*78 + "*")
    print("*  By default, this script only allows connections to localhost (127.0.0.1)." + " "*10 + "*")
    print("*" + " "*78 + "*")
    print("*"*80 + "\n")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Network Protocol Educational Simulator")
    parser.add_argument("--target", default="127.0.0.1", help="Target host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--protocol", default="http", choices=["http", "https", "icmp"], 
                        help="Protocol to simulate (default: http)")
    parser.add_argument("--requests", type=int, default=5, 
                        help=f"Number of requests to send (default: 5, max: {MAX_REQUESTS})")
    parser.add_argument("--delay", type=float, default=1.0, 
                        help=f"Delay between requests in seconds (default: 1.0, min: {MIN_DELAY})")
    parser.add_argument("--path", default="/", help="Path for HTTP/HTTPS requests (default: /)")
    
    args = parser.parse_args()
    
    # Create and run the simulator
    simulator = ProtocolSimulator(
        target=args.target,
        port=args.port,
        protocol=args.protocol,
        num_requests=args.requests,
        delay=args.delay,
        path=args.path
    )
    
    simulator.run_simulation()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("\nSimulation complete. Thank you for using this educational tool responsibly.")