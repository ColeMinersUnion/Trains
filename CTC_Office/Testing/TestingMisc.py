import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Frontend')))

from delay import DelayedExecutor

def use_delay(seconds: int):
    delayed = DelayedExecutor()
    delayed.delayed = seconds
    start = time.time()
    @delayed.delay()
    def test():
        pass
    test()
    end = time.time()
    return end - start

def approx(expected, actual, tolerance=0.1):
    return abs(expected - actual) < tolerance

def test_delay():
    for i in range(0, 10):
        assert(approx(use_delay(i), i))
    

if __name__ == "__main__":
    print("Running tests")
    print(use_delay(1), 1)
    