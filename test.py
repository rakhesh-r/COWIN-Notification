import sched
import time
import imgkit


s = sched.scheduler(time.time, time.sleep)


def do_something(sc):
    print("Doing stuff...")
    # do your stuff
    s.enter(5, 1, do_something, (sc,))

imgkit.from_string("<h1>Hello</h1>", 'out.png')

#s.enter(5, 1, do_something, (s,))
#s.run()
