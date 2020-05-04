import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Bad usage! Try: python sleep_n_seconds.py N (seconds to sleep)")
        exit()
    time.sleep(int(sys.argv[1]))