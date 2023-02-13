Transparent Proxy Server with Python.

This Proxy Server listen 9091 port and log to file.

Dependencies:twisted,fastapi,getmac
pip install twisted
pip install --no-cache fastapi
pip install getmac

Setup:
1.Change "C:/Users/wwPHP/Desktop/" directory path.
2.Add nat rule on your firewall or router.
3.Forward tcp traffic from port 80 to proxy server port 9091.
4.Run to "python server.py" command on your command line.

Log Format:
Time----ClientIPAdress----ClientMACAdress----Host:URL

http://wwphp.com