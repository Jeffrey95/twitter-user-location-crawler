## Introduction

It's a simple twitter user location crawler. It gets user's location from user's profile. It doesn't use twitter API because of the rate limit.

It mainly use:
* threading
* requests
* bs4

The performance of this code is mainly depended on your CPU's computing ability. You can adjust the number of threads according to CPU usage.

I am considering using multiprocessing, celery and redis to refactor this project.

## Usage

0. (optional) Create a new virtualenv
    ```bash
    $ python3 -m venv venv
    ```

1. Install dependency.
    ```bash
    $ pip install -r requirements.txt
    ```

2. Put target user's screen_name in `names.txt`.

3. Start crawl data
    ```bash
    $ python run.py
    ```

4. Get the Result from `locations.csv`.

## Appendix

### 1. Time performance

If you want to calculate the code's time performance, you can use `time` command in *nix platform.

For example:

```bash
$ time python run.server
# 1 threads
real    6m51.867s
user    3m44.582s
sys     0m3.561s

$ time python run.server
# 5 threads
real    3m4.755s
user    3m0.816s
sys     0m2.839s
```

As we can see above, when `real time` is approximately equal to the `user time`, it means the time are mainly used on parsing the data rather than waiting for IO block.
On the contrary, you can add the number of threads to take full advantage of the CPU.