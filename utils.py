from datetime import date

def getDateNow():
    d = date.today()
    return "%02d-%02d-%04d" % (d.day, d.month, d.year)

#print(getDateNow())