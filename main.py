import slackclient
import urlprobe


def main():
    log = urlprobe.getlist()
    if log:
        slackclient.notify(log.lower())


if __name__ == "__main__":
    main()
