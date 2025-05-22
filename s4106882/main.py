import pyhtml
import page_1

pyhtml.MyRequestHandler.pages["/"]=page_1; #Page to show when someone accesses "http://localhost/"

pyhtml.host_site()