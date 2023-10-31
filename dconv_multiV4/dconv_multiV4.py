# ===================================

# Grenoble, 20/12/2022

# dconv_multiV2, versione 2

# Conversione dati trasmissione o fluorescenza 

# Prende la configurazione dal file dconv_config.txt 

# Author: Alessandro Puri

# ===================================
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *
import numpy as np
import pandas as pd 
import math
#import matplotlib.pyplot as plt
import sys
import os
import importlib.machinery
#from dconv_config import *

#load user paerameters from txt file

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
mydir = os.path.join(dirname, "dconv_configV4.txt")
print (mydir)

global myvars
myvars = importlib.machinery.SourceFileLoader('myvars', mydir).load_module()

xtal = myvars.xtal
th0 = myvars.th0
columnsXiaOn = myvars.columnsXiaOn
columnsXiaOFF = myvars.columnsXiaOFF

print (xtal)
print (th0)
print (columnsXiaOn)
print (columnsXiaOFF)

# *****************************************
# users parameters
#xtal=111
#th0 = -252336
a0 = 5.429445
#xtal, th0, = np.loadtxt(os.path.join(sys.path[0],"dconv_config.txt"))
print("xtal is: ", xtal) 
print("th0 is: ", th0) 
print("a0 is: ", a0) 
# *****************************************

def callback():
 myfiles = fd.askopenfilenames(title='Choose a file')
 global mypaths
 mypaths = list(myfiles)
 print(mypaths)
  #   errmsg = 'Error!'

factorArr =np.array([[311, 20560.4204], [111, 10737.3294], [333, 31122.9881 ]])
print(factorArr)
for i in range(len(factorArr)):
  if factorArr[i,0] == xtal:
    factor=factorArr[i,1]
print(factor)

def convert():
    for i in range(len(mypaths)):
        filepath = mypaths[i]
        print(filepath)
        data = pd.read_csv(filepath, delim_whitespace=True, header=None, comment='#')
        if len(data.columns) >= 40:
            data1 = pd.DataFrame(data, columns=columnsXiaOn)
            data1.columns = ["mono", "ebragg", "I0_EH2", "I1_EH2", "IX_EH2", "IR_EH2", "c8", 'fluo01', 'fluo02', 'fluo03', 'fluo04', 'fluo05', 'fluo06', 'fluo07', 'fluo08', 'fluo09', 'fluo10', 'fluo11', 'fluo12', 'fluo13', 'I0_EH1', 'I1_EH1', 'IX_EH1', 'c9']
            data1['#eBraggEnergy'] = factor/a0/np.sin(np.radians((data1['ebragg']+th0)/800000.0))
            outdata=pd.DataFrame(data1[['#eBraggEnergy', 'I0_EH2', 'I1_EH2', 'IX_EH2', 'IR_EH2', 'c8', 'c9', 'fluo01', 'fluo02', 'fluo03', 'fluo04', 'fluo05', 'fluo06', 'fluo07', 'fluo08', 'fluo09', 'fluo10', 'fluo11', 'fluo12', 'fluo13', 'I0_EH1', 'I1_EH1', 'IX_EH1']])
            print(outdata)
            outfilepath = filepath.replace('.', '_c.')
            outdata.to_csv(outfilepath, header=True, index=False, sep=' ')
        else:
            data1 = pd.DataFrame(data, columns=columnsXiaOFF)
            data1.columns = ["mono", "ebragg", "I0_EH2", "I1_EH2", "IX_EH2", "IR_EH2", "c8", 'I0_EH1', 'I1_EH1', 'IX_EH1', 'c9']
            data1['#eBraggEnergy'] = factor/a0/np.sin(np.radians((data1['ebragg']+th0)/800000.0))
            outdata=pd.DataFrame(data1[['#eBraggEnergy', 'I0_EH2', 'I1_EH2', 'IX_EH2', 'IR_EH2', 'c8', 'c9', 'I0_EH1', 'I1_EH1', 'IX_EH1']])
            print(outdata)
            outfilepath = filepath.replace('.', '_c.')
            outdata.to_csv(outfilepath, header=True, index=False, sep=' ')
def quit():
    sys.exit()                       
        #data['#eBraggEnergy'] = factor/a0/np.sin(np.radians((data['ebragg']+th0)/800000.0))
        #outdata = outdata[outdata.mu != 0]
        #print(outdata)
        #outfilepath = filepath.replace('.', '_c.')
        #outdata.to_csv(outfilepath, header=True, index=False, sep=' ')

window=Tk()
# add widgets here
lbl1 = Label(window, text='LISA data reduction', fg='blue', font=("Helvetica", 16))
lbl1.place(x=100, y=10)
lbl2 = Label(window, text='xtal =', fg='red', font=("Helvetica", 16))
lbl2.place(x=220, y=50)
lbl3 = Label(window, text=int(xtal), bg='orange', font=("Helvetica", 16))
lbl3.place(x=280, y=50)
lbl4 = Label(window, text='th0 =', fg='red', font=("Helvetica", 16))
lbl4.place(x=220, y=80)
lbl5 = Label(window, text=th0, bg='orange', font=("Helvetica", 16))
lbl5.place(x=280, y=80)
lbl6 = Label(window, text='a0 =', fg='red', font=("Helvetica", 16))
lbl6.place(x=220, y=110)
lbl7 = Label(window, text=a0, bg='orange', font=("Helvetica", 16))
lbl7.place(x=280, y=110)
lbl8 = Label(window, text= 'A.P. - J.O. 2023', fg='blue', font=("Helvetica", 10))
lbl8.place(x=40, y=260) 
btn1=Button(text='Click to Open File',font=("Helvetica", 12), command=callback)
btn1.place(x=40, y=80)
btn2=Button(text='Convert',font=("Helvetica", 12), fg='red', command=convert)
btn2.place(x=150, y=200)
#btn3=Button(text='Transm+fluo',font=("Helvetica", 12), command=convert_fluo)
#btn3.place(x=230, y=200)
btn4=Button(text='Quit',font=("Helvetica", 12), command=quit)
btn4.place(x=350, y=260)
window.title('Data converter')
window.geometry("400x300+10+20")
window.mainloop()	

