import pyhtml
import page_1
import page_2
import page_3

pyhtml.MyRequestHandler.pages["/"]=page_1;
pyhtml.MyRequestHandler.pages["/page2"]=page_2;
pyhtml.MyRequestHandler.pages["/page3"]=page_3;

pyhtml.host_site()