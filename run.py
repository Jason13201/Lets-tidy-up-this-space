from website import startDebugServer
from website.bot import runBot
from multiprocessing import Process, Manager


def main():
    sharedQueue = Manager().Queue()
    botProcess = Process(target=runBot, args=(sharedQueue,))
    botProcess.start()
    startDebugServer(sharedQueue)


if __name__ == "__main__":
    main()
