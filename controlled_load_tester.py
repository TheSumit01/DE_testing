#!/usr/bin/env python3
"""
Controlled Load Testing Script - FOR EDUCATIONAL PURPOSES ONLY

This script demonstrates how concurrent requests work for educational purposes.
It includes safety measures to prevent accidental misuse.

WARNING: Only use against servers you own or have explicit permission to test.
"""

import requests
import concurrent.futures
import time
import argparse
import sys
from urllib.parse import urlparse

# Safety limits
MAX_REQUESTS = 100  # Maximum number of requests allowed
MAX_THREADS = 10    # Maximum number of concurrent threads
MIN_DELAY = 0.1     # Minimum delay between thread creation (seconds)
WHITELIST = ["127.0.0.1", "localhost"]  # Only allow local testing by default

def send_request(url, timeout=2, headers=None):
    """Send a single HTTP request and return the status code"""
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return str(e)

def is_safe_target(url):
    """Check if the target URL is in the whitelist"""
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc.split(':')[0]  # Remove port if present
    return hostname in WHITELIST

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Controlled Load Testing Script - FOR EDUCATIONAL PURPOSES ONLY",
        epilog="WARNING: Only use against servers you own or have explicit permission to test."
    )
    parser.add_argument("--url", required=True, help="Target URL (must be a server you own or have permission to test)")
    parser.add_argument("--requests", type=int, default=50, help=f"Number of requests (default: 50, max: {MAX_REQUESTS})")
    parser.add_argument("--threads", type=int, default=5, help=f"Number of concurrent threads (default: 5, max: {MAX_THREADS})")
    parser.add_argument("--timeout", type=float, default=2.0, help="Request timeout in seconds (default: 2.0)")
    parser.add_argument("--delay", type=float, default=0.2, help=f"Delay between thread creation in seconds (default: 0.2, min: {MIN_DELAY})")
    parser.add_argument("--bypass-whitelist", action="store_true", help="Bypass the whitelist check (use with caution)")
    
    args = parser.parse_args()
    
    # Apply safety limits
    total_requests = min(args.requests, MAX_REQUESTS)
    threads = min(args.threads, MAX_THREADS)
    delay = max(args.delay, MIN_DELAY)
    
    # Display educational disclaimer
    print("\n" + "*"*80)
    print("*" + " "*78 + "*")
    print("*  CONTROLLED LOAD TESTING SCRIPT - FOR EDUCATIONAL PURPOSES ONLY" + " "*17 + "*")
    print("*" + " "*78 + "*")
    print("*  WARNING: This tool should only be used in controlled environments" + " "*19 + "*")
    print("*  against targets you own or have explicit permission to test." + " "*23 + "*")
    print("*" + " "*78 + "*")
    print("*  By default, this script only allows connections to localhost (127.0.0.1)." + " "*10 + "*")
    print("*" + " "*78 + "*")
    print("*"*80 + "\n")
    
    # Safety check for target
    if not args.bypass_whitelist and not is_safe_target(args.url):
        print(f"\033[91mERROR: Target {args.url} is not in the whitelist.\033[0m")
        print(f"For educational purposes, this script only allows connections to: {', '.join(WHITELIST)}")
        print("If you're testing against a server you own or have permission to test, use --bypass-whitelist")
        print("IMPORTANT: Unauthorized testing against servers you don't own is illegal and unethical.")
        sys.exit(1)
    
    if args.bypass_whitelist:
        print("\033[93mWARNING: Whitelist check bypassed. Ensure you have permission to test this target.\033[0m")
        confirmation = input("Do you confirm you have permission to test this target? (yes/no): ")
        if confirmation.lower() != "yes":
            print("Test aborted.")
            sys.exit(0)
    
    # Educational information
    print("\nEDUCATIONAL INFORMATION:")
    print("1. This script demonstrates how concurrent HTTP requests work")
    print("2. It uses Python's ThreadPoolExecutor for parallel execution")
    print("3. In a production environment, proper rate limiting and error handling would be implemented")
    print("4. Load testing should always be performed with permission and care\n")
    
    # Display test parameters
    print(f"Target URL: {args.url}")
    print(f"Number of requests: {total_requests}")
    print(f"Concurrent threads: {threads}")
    print(f"Request timeout: {args.timeout} seconds")
    print(f"Thread creation delay: {delay} seconds\n")
    
    # Confirmation
    confirmation = input("Proceed with the test? (yes/no): ")
    if confirmation.lower() != "yes":
        print("Test aborted.")
        sys.exit(0)
    
    print(f"\nSending {total_requests} requests to {args.url}...")
    
    # Add a custom user agent to identify educational testing
    headers = {
        "User-Agent": "Educational-Load-Tester/1.0",
        "X-Testing-Purpose": "Educational"
    }
    
    start = time.time()
    success_count = 0
    error_count = 0
    status_codes = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # Submit tasks with a delay to prevent instant flooding
        futures = []
        for i in range(total_requests):
            futures.append(executor.submit(send_request, args.url, args.timeout, headers))
            if i < total_requests - 1:  # Don't sleep after the last request
                time.sleep(delay)
        
        # Process results as they complete
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            status = future.result()
            print(f"[{i}/{total_requests}] Response: {status}")
            
            # Count successes and errors
            if isinstance(status, int) and 200 <= status < 400:
                success_count += 1
            else:
                error_count += 1
            
            # Track status code distribution
            status_str = str(status)
            status_codes[status_str] = status_codes.get(status_str, 0) + 1
    
    end = time.time()
    duration = end - start
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print(f"Total requests: {total_requests}")
    print(f"Successful responses: {success_count}")
    print(f"Error responses: {error_count}")
    print(f"Success rate: {(success_count/total_requests)*100:.2f}%")
    print(f"Total duration: {duration:.2f} seconds")
    print(f"Requests per second: {total_requests/duration:.2f}")
    
    print("\nResponse code distribution:")
    for status, count in status_codes.items():
        print(f"  {status}: {count} ({count/total_requests*100:.2f}%)")
    
    print("\nEDUCATIONAL NOTES:")
    print("1. This script demonstrates basic concurrent request handling")
    print("2. The ThreadPoolExecutor manages a pool of worker threads")
    print("3. Real-world load testing tools like Apache JMeter or Locust offer more features")
    print("4. Always monitor server resources during testing to prevent unintended impact")
    print("5. Consider gradual ramp-up and cool-down periods in professional load tests")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("\nTest complete. Thank you for using this educational tool responsibly.")