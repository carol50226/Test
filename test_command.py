# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 16:24:24 2019

@author: User
"""

import sys
 
def main():
    #intValue = int(sys.argv[1])#如果要將變數搞成數字的話可以使用 int()來轉
    print (sys.argv[1])
    #print (sys.argv[2])
    #print (sys.argv[3])
    print ("===============")
    print (len(sys.argv))#參數一共有幾個
    print ("===============")
    for x in sys.argv:
        print (x)
 
if __name__ == "__main__":
    main()