from datetime import datetime

start = datetime.now()

f = open("train_v2.txt")
line_count = 0

try:
    for line in f:
        line_count += 1
        if line_count % 1000000 == 0:
            print ".",
except KeyboardInterrupt:
    pass

print

f.close()

stop = datetime.now()

print "Total time %s" % (stop - start)
print "Total number of lines %s." % (line_count)
