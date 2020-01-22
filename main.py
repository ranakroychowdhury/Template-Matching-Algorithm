# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 21:45:26 2018

@author: Ranakrc
"""

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
import numpy as np
import time



def ExhaustiveSearch(t, I, J, r, M, N):

    file = open("out1.txt","w") 
    minD = np.inf
    test = t.astype(int)
    test = test[0 : I, 0 : J, 0 : 3]
    ref = r.astype(int)
    ref = ref[0 : M, 0 : N, 0 : 3]
    for m in range(I - M + 1):
        for n in range(J - N + 1):
            tmp = test[m : m + M, n : n + N]
            D = sum(sum(sum(np.absolute(ref - tmp))))     
            file.write(str(m) + "\t" + str(n) + "\t" + str(D) + "\t" + "\t")
            if D < minD:
                minD = D
                globalM = m
                globalN = n    
        file.write("\n")
        
    file.close()
    return globalM, globalN



def TwoDLogarithmicSearchV1(t, I, J, r, M, N):
    
    file = open("out2.txt","w") 
    p = np.ceil((I - 1) / 2)
    q = np.ceil((J - 1) / 2)
    m = np.ceil((M - 1) / 2)
    n = np.ceil((N - 1) / 2)
    iter = 1
    k = np.round(np.log2(p))
    l = np.round(np.log2(q))
    dp = np.power(2, k - iter)
    dq = np.power(2, l - iter)
    Oy = np.ceil((I - 1) / 2)
    Ox = np.ceil((J - 1) / 2)
    test = t.astype(int)
    test = test[0 : I, 0 : J, 0 : 3]
    ref = r.astype(int)
    ref = ref[0 : M, 0 : N, 0 : 3]
    print(I, J, M, N)
    
    while(dp >= 1 and dq >= 1):
    
        minD = np.inf
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = (int)(Oy + i * dp - m)
                x = (int)(Ox + j * dq - n)
                if(y + M >= I):
                    y = I - M
                if(y < 0):
                    y = 0
                if(x + N >= J):
                    x = J - N
                if(x < 0):
                    x = 0
                tmp = test[y : y + M, x : x + N]
                D = sum(sum(sum(np.absolute(ref - tmp))))
                file.write(str(Oy + i * dp) + "\t" + str(Ox + j * dq) + "\t" + str(D) + "\t" + "\t")
                if D < minD:
                    minD = D
                    minOy = Oy + i * dp
                    minOx = Ox + j * dq
        file.write("\n")
        Oy = minOy
        Ox = minOx
        iter = iter + 1
        dp = np.power(2, k - iter)
        dq = np.power(2, l - iter)
    
    file.close()
    print(Oy - m, Ox - n)
    return Oy - m, Ox - n



def TwoDLogarithmicSearchV2(t, I, J, r, M, N, startY, startX):
    
    m = np.ceil((M - 1) / 2)
    n = np.ceil((N - 1) / 2)
    Oy = startY
    Ox = startX
    test = t.astype(int)
    test = test[0 : I, 0 : J, 0 : 3]
    ref = r.astype(int)
    ref = ref[0 : M, 0 : N, 0 : 3]

    minD = np.inf
    for i in range(-1, 2):
        for j in range(-1, 2):
            y = (int)(Oy + i - m)
            x = (int)(Ox + j - n)
            if(y + M >= I):
                y = I - M
            if(y < 0):
                y = 0
            if(x + N >= J):
                x = J - N
            if(x < 0):
                x = 0
            tmp = test[y : y + M, x : x + N]
            #print(y+M, x+N)
            D = sum(sum(sum(np.absolute(ref - tmp))))
            if D < minD:
                minD = D
                minOy = Oy + i
                minOx = Ox + j
    
    return minOy - m, minOx - n
    


def HierarchialSearch(test, ref, level):
    
    l = 0;
    testList = []
    refList = []
    
    #test image
    arrTest = np.array(test)
    testList.append(arrTest)
    
    #reference image
    arrRef = np.array(ref)
    refList.append(arrRef)
    
    
    while(l < level):
        
        #test image
        test = test.filter(ImageFilter.BLUR)
        ct, rt = test.size
        test = test.resize((int(np.ceil(ct / 2)), int(np.ceil(rt / 2))))
        arrTest = np.array(test)
        testList.append(arrTest)
        
        #reference image
        ref = ref.filter(ImageFilter.BLUR)
        cr, rr = ref.size
        ref = ref.resize((int(np.ceil(cr / 2)), int(np.ceil(rr / 2))))
        arrRef = np.array(ref)
        refList.append(arrRef)
        
        l = l + 1
       
    
    while(l >= 0):
        
        arrT = testList.pop()
        I, J, K = arrT.shape
        
        arrR = refList.pop()
        M, N, O = arrR.shape
    
        if(l == level):
            y, x = ExhaustiveSearch(arrT, I, J, arrR, M, N)
        else:
            y, x = TwoDLogarithmicSearchV2(arrT, I, J, arrR, M, N, 2*y + int(np.ceil(M/2)), 2*x + int(np.ceil(N/2)))
        
        l = l - 1
        
        
    return y, x



def main():
    
    #test image properties
    test = Image.open('Image2.jpg')
    arrTest = np.array(test)
    I, J, K = arrTest.shape
    print(I, J, K)
    
    #reference image properties
    ref = Image.open('Image1.jpg')
    arrRef = np.array(ref)
    M, N, O = arrRef.shape
    print(M, N, O)
    
    m, n = TwoDLogarithmicSearchV1(arrTest, I, J, arrRef, M, N)
    print(m, n)
    
    #m, n = HierarchialSearch(test, ref, 2)
    #print(m, n)
    
    draw = ImageDraw.Draw(test)
    draw.rectangle(((n, m), (n + N, m + M)), outline = "black")
    draw.rectangle(((n - 50, m), (n - 30, m + 20)), outline = "black", fill = "white")
    draw.text((n - 40, m + 5), "P", fill = "black")
    draw.line((n - 30, m, n, m), fill = "black")
    draw.line((n, m, n - 5, m - 5), fill = "black")
    draw.line((n, m, n - 5, m + 5), fill = "black")
    test.save('Image3.png')
    
    print("--- %s seconds ---" % (time.time() - start_time))
    
if __name__== "__main__":
    start_time = time.time()
    main()
  
