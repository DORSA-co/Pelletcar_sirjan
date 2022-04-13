import cv2
import numpy as np
#from matplotlib import pyplot as plt
import os
import time


MIN_AREA0 = 200
MIN_W1=7
MAX_W1 = 16

MIN_W2 = 20
MAX_W2 = 32


GRADE_BOX_MIN_AREA=100000
GRADE_BOX_MAX_AREA = 500000 
GRADE_BOX_MIN_RATIO = 8
DEBUG = False
DEBUG_LVL2 = False  
path = 'before process pic'
#path = 'bad'

def find_defects(gray,grade_box_min_area=GRADE_BOX_MIN_AREA,
                     grade_box_max_area=GRADE_BOX_MAX_AREA,
                     grade_box_min_ration=GRADE_BOX_MIN_RATIO,
                     min_w1=MIN_W1,
                     max_w1=MAX_W1,
                     min_w2=MIN_W2,
                     max_w2=MAX_W2,
                     min_area0=MIN_AREA0,
                     min_pellet_box_count=4 ):

    gray = np.array(gray).astype(np.uint8)
    blur = cv2.blur(gray, (21,21))


    if DEBUG:
        cv2.imshow('gray', cv2.resize(gray, None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)


    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    if DEBUG:
        cv2.imshow('gray', cv2.resize(gray, None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)




    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 11)
    if DEBUG:
        cv2.imshow('thresh', cv2.resize(thresh , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)

    morph = cv2.erode(thresh, np.ones((1,31)) , iterations=3 )
    if DEBUG:
        cv2.imshow('morhp', cv2.resize(morph , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)
        
    morph = cv2.dilate(morph, np.ones((3,3)) , iterations=30 )
    if DEBUG:
        cv2.imshow('morhp', cv2.resize(morph , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)
        
    morph = cv2.erode(morph, np.ones((3,3)) , iterations=10 )
    if DEBUG:
        cv2.imshow('morhp', cv2.resize(morph , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)

    res_morph = np.copy(morph)

    #--------------SUM Filter-----------------------------
    h,w = res_morph.shape[:2]
    sum_cols = np.sum(res_morph, axis=1)
    sum_cols = sum_cols/255
    thresh_rows = np.where(sum_cols>w*0.5)[0]
    res_morph[thresh_rows,:]=255
    #--------------SUM Filter-----------------------------

    if DEBUG:
        cv2.imshow('fill soton', cv2.resize(res_morph , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)


    #--------------SUM Filter-----------------------------
    h,w = res_morph.shape[:2]
    sum_rows = np.sum(res_morph, axis=0)
    sum_rows = sum_rows/255
    thresh_cols = np.where(sum_rows>w*0.75)[0]
    res_morph[:,thresh_cols]=255
    #--------------SUM Filter-----------------------------

    if DEBUG:
        cv2.imshow('col filter', cv2.resize(res_morph , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)


    #--------------SUM Filter-----------------------------
    h,w = res_morph.shape[:2]
    sum_cols = np.sum(res_morph, axis=1)
    sum_cols = sum_cols/255
    thresh_rows = np.where(sum_cols<w*0.5)[0]
    res_morph[thresh_rows,:]=0
    res_morph[:,1]=255
    res_morph[:,-1]=255
    #--------------SUM Filter-----------------------------

    
    if DEBUG:
        cv2.imshow('set black row of box', cv2.resize(res_morph , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)

    cnts,_= cv2.findContours(res_morph, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    grade_box_mask = np.zeros_like(gray)
    grade_box_cnts = []
    grade_box_count=0
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        _,(w,h),_= rect
        if DEBUG_LVL2:
            debug_mask = np.zeros_like(gray)
            cv2.drawContours(debug_mask, [box], 0, 255, thickness=-1)
            print('area',area)
            print('aspect_ratio(h/w)=', h/w,'   aspect_ratio(h/w)=', w/h)
            print('-'*20)
            cv2.imshow('debug_GradeBox_mask', cv2.resize(debug_mask, None, fx=0.4,fy=0.4))
            cv2.waitKey(0)
        
        if grade_box_min_area<area<grade_box_max_area and (h/w>grade_box_min_ration or w/h>grade_box_min_ration):
            cv2.drawContours(grade_box_mask, [box], 0, 255, thickness=-1)
            grade_box_cnts.append(box)
            grade_box_count+=1
    
    valid = 0
    with_preson_area = 310000
    #____________________________________________Check count of Grade Box_______________________________________________________
    if grade_box_count>=min_pellet_box_count:
    
        _temp_ = np.copy( morph)
        mask = np.zeros_like( _temp_)
        mask = cv2.drawContours(mask,grade_box_cnts, -1, 255,-1)
        _temp_ = cv2.bitwise_and( _temp_, _temp_, mask=mask)
        _temp_ = cv2.erode(_temp_, np.ones((3,3)), iterations=7)
        _temp_ = cv2.dilate(_temp_, np.ones((3,3)), iterations=15)                
        
        
        if (np.sum(_temp_) / 255 )<with_preson_area:
            valid = 1
            
        if DEBUG:
            print( 'SUM:',_temp_.sum()/255 )
            cv2.imshow('false',cv2.resize( _temp_, None, fx=0.4, fy=0.4 ))
            cv2.waitKey(0)

    
            
    es = cv2.erode(grade_box_mask, np.ones((3,3)) , iterations=1 )      



    if DEBUG:
        cv2.imshow('grade_box_mask', cv2.resize(grade_box_mask , None, fx=0.4, fy=0.4) )
        cv2.waitKey(0)


    pellet_car_gray = cv2.bitwise_and(gray, gray, mask = grade_box_mask)
    pellet_car_gray = cv2.equalizeHist(pellet_car_gray)

    thresh2 = cv2.adaptiveThreshold(pellet_car_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 11)
    res = cv2.bitwise_and(thresh2, cv2.bitwise_not(res_morph))
    res = cv2.erode(res, np.ones((5,1)) , iterations=1 )
    res = cv2.dilate(res, np.ones((5,1)) , iterations=2 )
    res = cv2.erode(res, np.ones((5,1)) , iterations=1 )
    res = cv2.dilate(res, np.ones((5,1)) , iterations=2 )
    #plt.imshow(res)
    #plt.show()
    #cv2.imshow('res', cv2.resize(res,None,fx=0.5,fy=0.5))
    #cv2.waitKey(0)
    if DEBUG:
        cv2.imshow('res', cv2.resize(res , None, fx=0.5, fy=0.5) )
        cv2.imshow('pellet_car_gray', cv2.resize(pellet_car_gray , None, fx=0.2, fy=0.2) )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #res = np.zeros_like(gray)
    result_defects=[[-1,-1,-1,-1,valid]]
    
    count_grade=0
    
    all_box_h = []
    for grade_box in grade_box_cnts:
        _,_,box_w, box_h = cv2.boundingRect(grade_box)
        box_w, box_h = max(box_w,box_h), min(box_w, box_h)
        all_box_h.append( box_h )
    mean_box_h = np.array(all_box_h).mean()    
    
    for grade_box in grade_box_cnts:
        
        _,_,box_w, box_h = cv2.boundingRect(grade_box)
        box_w, box_h = max(box_w,box_h), min(box_w, box_h)
        _only_one_box_ = np.copy(res)

        mask = np.zeros_like(_only_one_box_)
        cv2.drawContours(mask, [grade_box], 0, 255, thickness=-1)
        _only_one_box_ = cv2.bitwise_and( _only_one_box_, _only_one_box_, mask=mask )
        cnts,_ = cv2.findContours(_only_one_box_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if DEBUG:
            cv2.imshow('_only_one_mask', cv2.resize(_only_one_box_ , None, fx=0.5, fy=0.5))
            cv2.waitKey(0)
        
        for cnt in cnts:
            _,(w,h),_ = cv2.minAreaRect(cnt)
            area = w*h
            area = cv2.contourArea(cnt)
            M = cv2.moments(cnt)
            cx = int(M['m10']/(M['m00']+0.001))
            cy = int(M['m01']/(M['m00']+0.001))
            if area>300:
                count_grade+=1
                
            if DEBUG_LVL2 and area>250:
                debug_grade = np.copy(gray)
                cv2.drawContours(debug_grade, [cnt], 0, 255, thickness=-1)
                print(area)
                cv2.imshow('debug_grade_hofre', cv2.resize(debug_grade, None, fx=0.4, fy=0.4) )
                cv2.waitKey(0)
                
                
            alpha = 0.7  * box_h/mean_box_h
            #print(alpha)
            if min_w1*box_h*alpha<=area<max_w1*box_h*alpha:
                result_defects.append([cx, cy,int(min(h,w)),1,valid])
            
            elif min_w2*box_h*alpha<=area<max_w2*box_h*alpha:
                result_defects.append([cx, cy,int(min(h,w)),2,valid])
    #print('ALL:',
    result_defects = np.array(result_defects, dtype=np.int32)
    result_defects[0,-2]=count_grade
    return result_defects             








'''

for i,file in enumerate (os.listdir(path)):
    print('the image is ', file)
    #if '183' in file:
    #    DEBUG = False  

        #DEBUG_LVL2=True
    img = cv2.imread(os.path.join(path,file))
    #img  = cv2.imread('pallet pics/00.bmp')
    t = time.time()
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    defects = find_defects(gr)

    print('validation:', defects[0,-1], 'ALL:', defects[0,3])
    for defect in defects[1:]:
        #print(defect)
        if defect[-2]==1:
            cv2.circle(img, (defect[0],defect[1]), 5, (255,0,0), thickness=-1)
        
        if defect[-2]==2:
            cv2.circle(img, (defect[0],defect[1]), 7, (0,0,255), thickness=-1)
    t = time.time() - t
    print(t)
    #ccv2.imshow('res', cv2.resize(res, None, fx=0.4, fy=0.4) )
    cv2.imshow('img', cv2.resize(img, None, fx=0.4, fy=0.4) )
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''