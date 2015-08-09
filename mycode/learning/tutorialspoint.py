
from __future__ import division;
from __future__ import print_function;
from __future__ import unicode_literals;
from __future__ import absolute_import;

import utils;
import threading;
import sys;
import time;

#reconcile differences between Python2 and Python3
if sys.version_info.major==2:
	try:
		import Queue as queue;
	except:
		print('Failed to import Queue');
		sys.exit();
		
elif sys.version_info.major==3:
	try:
		import queue as queue;
	except:
		print('Failed to import queue');
		sys.exit();
else:
	print('unknown python version');
	sys.exit(0);

#define a custom Thread class
class MyThread(threading.Thread):
	'''
	Define a custom thread class by subclassing threading.Thread.
	'''
	def __init__(self, threadName='', delay=1):
		threading.Thread.__init__(self);
		self.threadName = threadName;
		self.delay = delay;
		
	def run(self):
		#do I need self.xx always, like self.threadName? yes, 
		#otherwise 'NameError: global name 'threadName' is not defined'
		'''
		Found bug in Python2 when using print(...) as in
		'print('Starting {:s}'.format(self.threadName));'
		RESULT:
		vad@vad-MD2614u:~/challenges/mycode/learning$ python tutorialspoint.py
		Starting thread1
		Starting thread2
		thread1 consumed hat
		Starting thread3thread2 consumed cat

		thread3 consumed food
		Starting thread4
		thread4 consumed car
		thread1 consumed rhinosaurus
		thread4 consumed rabbit
		Exiting thread1
		Exiting thread3Exiting thread2
		Exiting thread4

		vad@vad-MD2614u:~/challenges/mycode/learning$ python3 tutorialspoint.py
		
		However, solution is to use 
		'sys.stdout.write('Starting {:s}\n'.format(self.threadName));'
		RESULT:
		vad@vad-MD2614u:~/challenges/mycode/learning$ python tutorialspoint.py
		Starting thread1
		Starting thread2
		thread2 consumed hat
		thread1 consumed cat
		Starting thread3
		thread3 consumed food
		Starting thread4
		thread4 consumed car
		thread2 consumed rhinosaurus
		thread1 consumed rabbit
		Exiting thread3
		Exiting thread4
		Exiting thread1
		Exiting thread2
		vad@vad-MD2614u:~/challenges/mycode/learning$ python3 tutorialspoint.py
		'''
		#print('Starting {:s}'.format(self.threadName));
		sys.stdout.write('Starting {:s}\n'.format(self.threadName));
		trial_run(self.threadName, self.delay);	
		sys.stdout.write('Exiting {:s}\n'.format(self.threadName));

#define function that will be executed inside threads
def trial_run(threadName, delay):
	'''
	Each thread will call this function.  So, proper locking is required
	to avoid thread contention.
	'''
	global exitFlag;
	global q;
	global lock;
	
	while exitFlag == 0:#check global variable for signal to exit loop
		lock.acquire(); #obtain lock, consume item, and release lock
		if not q.empty():#maybe, do q.get(), release(), and then print() ???
			print('{:s} consumed {:s}'.format(threadName, q.get()) );
		lock.release();
		time.sleep(delay);#reprieve to allow other threads to work

def test1():
	'''
	Testing multithreading queue access.
	'''
	global lock;
	global q;
	global exitFlag;
	
	stuffs = ['hat','cat','food','car','rhinosaurus','rabbit'];	
	lock.acquire();
	for stuff in stuffs: #produce items in Queue
		q.put(stuff);
	lock.release();

	#create thread object and start() to begin each thread's call to run()
	t1 = MyThread('thread1'); t1.start();
	t2 = MyThread('thread2'); t2.start();
	t3 = MyThread('thread3'); t3.start();
	t4 = MyThread('thread4'); t4.start();

	#loop until Queue is empty; items consumed by independent threads
	while True:
		#Is lock neccessary here since only read q.empty() and exitFlag
		# modified only by main thread ??? probably not
		lock.acquire();
		if q.empty(): #exit loop on Queue is empty
			exitFlag = 1;
			lock.release();
			break;
		lock.release();
		time.sleep(1);
	
	
exitFlag = 0; #signal to exit thread, 0 means False
lock = threading.Lock(); #create lock object, a singleton
q = queue.Queue();#create empty Queue object

test = test1;
test();


#utils.sendmail();
#utils.htmlemail();
