import logging
import random
import threading
from queue import Queue

from pandas import DataFrame

from user import User

HEADER_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

proxies = {'http': 'http://127.0.0.1:1087',
           'https': 'http://127.0.0.1:1087'}
q = Queue()
threads = []
locations = []
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
                    filename='output.log')

# Read screen_names from names.txt
with open('names.txt', 'r') as f:
    names = f.readlines()
    names = [name.strip() for name in names]
    for name in names:
        q.put(name.strip())


def job():
    while not q.empty():
        username = q.get()
        # Use user's screen_name to initialize a user
        # Note that screen_name is not equal to nickname.
        # For example, the juliamilazzo in the word '@juliamilazzo' is what we need.
        # See more in https://twitter.com/juliamilazzo and names.txt
        user = User(username)
        headers = {'User-Agent': random.choice(HEADER_LIST)}
        # Print(user.url)
        try:
            # Custom your work here.
            location = user.location(headers=headers)
            print('{0}--->{1}'.format(username, location))
            locations.append(location)
        except Exception as e:
            logging.error(e)
            q.put(username)


# Start 10 thread to crawl the users' data.
# You can adjust the number of the number of thread according to the CPU usage.
# For IO-intensive task, the more threads means you can take more advantage of a single CPU's calculate ability.
# After a single CPU's useage achieve 100%, consider using Multiprocessing.
for i in range(10):
    t = threading.Thread(target=job)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Save data.
df = DataFrame({"names": names,
                "locations": locations})
df.to_csv('locations.csv')
