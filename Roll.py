#! /usr/bin/python3
import time
import threading
import random
rollnum = 0


class Roll(threading.Thread):
    """docstring for Roll"""

    def __init__(self, rollid, title, waittingtime):
        super(Roll, self).__init__()
        self.rollid = rollid
        self.title = title
        self.waittingtime = waittingtime
        self.closetime = 'Unknown'
        self.user = []
        self.winner = 'Nobody'

    def JoinRoll(arg):
        if(arg not in self.user):
            self.user.append(arg)

    def run(self):
        self.closetime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time() + self.waittingtime * 3600))
        time.sleep(self.waittingtime * 3600)
        usercache = list(set(self.user))
        usercache.sort(key = self.user.index)
        random.seed(random.random())
        self.winner = usercache[random.randint(0, len(usercache)-1)]
