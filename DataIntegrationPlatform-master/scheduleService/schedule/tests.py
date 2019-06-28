from django.test import TestCase
from threading import Event, Thread
# Create your tests here.

if __name__ == '__main__':
    start_evt = Event()
    print("is_set:" + str(start_evt.is_set()))
    start_evt.set()
    print("is_set:" + str(start_evt.is_set()))
