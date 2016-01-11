import urllib2, time, os, sys, random

website='http://glastonbury.seetickets.com/'
#website="http://people.bath.ac.uk/nm268"

response = urllib2.urlopen(website)
html0 = response.read()
        
#html0=file("seetickets.html").read()
    
tic=time.time()
while True:
#for i in range(100):
    try: 
        response = urllib2.urlopen(website, timeout=10)
        html = response.read()
        if html.split("\n")[58:60]!=html0.split("\n")[58:60]:
            os.system("google-chrome "+website)
            break
        else: 
            sys.stdout.write('o')
    except: sys.stdout.write('x')
    sys.stdout.flush()
    #time.sleep(0.5+random.random())
print time.time()-tic
