import os
os.system("python -m PyQt5.uic.pyuic -x UI/client.ui -o UI/client.py")
os.system("move UI\client.py GUI\client.py")
