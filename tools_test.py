import time
from main import Chronometer

def main():
    test_cronometer()

def test_cronometer():
    test_init = time.time()

    chrono = Chronometer()
    chrono.start()
    print("read {:.2f}, should be 0.00".format(chrono.read()))

    time.sleep(1)
    print("read {:.2f}, should be 1.00".format(chrono.read()))
    
    chrono.pause()
    print("read {:.2f}, should be 1.00".format(chrono.read()))

    time.sleep(2)
    print("read {:.2f}, should be 1.00".format(chrono.read()))

    chrono.start()
    print("read {:.2f}, should be 1.00".format(chrono.read()))

    time.sleep(1)
    print("read {:.2f}, should be 2.00".format(chrono.read()))

    chrono.pause()
    print("read {:.2f}, should be 2.00".format(chrono.read()))
    
    chrono.reset()
    print("read {:.2f}, should be 0.00".format(chrono.read()))

    print("total time elapsed: {:.2f}, should be 4.00".format(time.time()-test_init))

if __name__ == "__main__":
    main()