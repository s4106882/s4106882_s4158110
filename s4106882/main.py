import pyhtml
import page_1
import page_2
import page_3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from s4158110 import page_4, page_5, page_6

pyhtml.MyRequestHandler.pages["/"] = page_1
pyhtml.MyRequestHandler.pages["/page2"] = page_2
pyhtml.MyRequestHandler.pages["/page3"] = page_3
pyhtml.MyRequestHandler.pages["/page4"] = page_4
pyhtml.MyRequestHandler.pages["/page5"] = page_5
pyhtml.MyRequestHandler.pages["/page6"] = page_6

pyhtml.host_site()