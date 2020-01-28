# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 06:33:28 2019

@author: MaheshDhaka
"""


import cv2
import numpy as np
from operator import itemgetter
import statistics
import pickle
import tkinter as tk
from tkinter import filedialog


############################## Begin Load an Image


window = tk.Tk()
window.geometry('800x600')
window.title("License Plate Recognition Portal")
window.configure(background = "#18ba28")
label1 = tk.Label(window,text="", foreground= "white", background = "#18ba28")
label1.place(relx=0.22,rely=0.30)
label1.config(font=('16', 16)) 
label2 = tk.Label(window,text="", foreground= "white", background = "#18ba28")
label2.place(relx=0.57,rely=0.30)
label2.config(font=('16', 16)) 

def BrowseIm():
    file_path = filedialog.askopenfilename()
    realimage = cv2.imread(file_path,1)
    LicensePlateRecognition(realimage)
    print(file_path)

button1 = tk.Button(window, text="Browse a Vehicle Image", command= BrowseIm, width = 18,height=2, padx=5, pady=5,foreground= "Blue", background = "#FBFBFB")
button1.place(rely=0.10,relx=0.39)


############################## End Load an Image


def LicensePlateRecognition(realimage):
    
    ############################## Preprocessing Begins Here 
    

    # Resize the Image
    dimension=(800,600)
    realimage = cv2.resize(realimage, dimension, interpolation = cv2.INTER_AREA)
    
    #Convert the Image To Gray Scale Formate
    myrealimage = cv2.cvtColor(realimage, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur and GAUSSIAN ADAPTIVE THRESHOLD to remove the noise
    myimage = cv2.medianBlur(myrealimage,5)
    
    mythreshedImage=cv2.adaptiveThreshold(myimage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
    
    
    ############################## Preprocessing Ends Here
    
    
    
    
    ############################## License Plate Detection Begins Here
    
    
    # Find Contours in the Image
    contours, hierarchy = cv2.findContours(mythreshedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Calculate the Height and Width of Image
    height, width= myrealimage.shape
    
    # Create an Image with same hight and width, but with no pixel values
    theZeroImage = np.zeros((height, width, 3), np.uint8)
    
    # Convert a List Containing Contours to an Array
    mycontoursarray=np.asarray(contours)
    
    # Calculate Size of Array
    theSizeOfArray=mycontoursarray.shape[0]
    
    # Total Number of Existing Contours.
    #print("Total Number of Existing Contours",theSizeOfArray)  # use this to find total number of contours
    
    # Lets find which of these contours have the properties of a character. 
    i=0
    possibleCharFromContour=[]
    while i<theSizeOfArray-1:
        cnt = contours[i]
        # Calculate x and y distance of a contour from top-left corner. Also find its Width and Height using inbuit CV function boundingRect
        x,y,w,h = cv2.boundingRect(cnt)
        if .25<(float(w)/h)<3 and cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<1000:
            # Store Possible Characters in a List
            possibleCharFromContour.append(cnt)
        i=i+1
    
           
    possibleCharFromContourtouse=possibleCharFromContour
    
    
    mycontim1=cv2.drawContours(theZeroImage, possibleCharFromContour, -1, (255,255,255), 1)
    possibleCharFromContour=np.asarray(possibleCharFromContour) 
    
    #Use this to print possibel characters
    ##print(possibleCharFromContour.shape[0])
       
    
    # Code to Calculate X,Y,W,H of all possble characters, obtained from the last step
    i=0
    anotheExperimentArray=[]
    heightArray=[]
    valueOfXArray=[]
    valueOfW=[]
    myContourProperties=[]
    while i<possibleCharFromContour.shape[0]-1:
        cnt = possibleCharFromContour[i]
        x,y,w,h = cv2.boundingRect(cnt) 
        
        # Store the possible character's properties such as x,y,w,h and its index in an array
        myContourProperties.append([x,y,w,h,i])
        
        # Store the vertical distance of possible characters by considering top-left corner as (0,0)
        anotheExperimentArray.append(y)
        
        # Store the height of possible characters in an array 
        heightArray.append(h)
        
        # Store the horizontal distance of possible characters by considering top-left corner as (0,0)
        valueOfXArray.append(x)
        valueOfW.append(w)
        i=i+1
    
    
    
    # Sort the possible characters in the increasing order of height
    myContourProperties = sorted(myContourProperties, key=itemgetter(3))
    
    # Sort the possible characters in the increasing order of vertical distance
    myContourProperties = sorted(myContourProperties, key=itemgetter(1))
    
    
    
    myContourProperties=np.asarray(myContourProperties)
    
    # Calculate The difference of each contour's Horizontial Distance, Vertical Distance, Height and Width with every other countour. 
    myfinalplate=[]
    i=0
    while i<myContourProperties.shape[0]-1:
        j=0
        while j<myContourProperties.shape[0]-1:
            if i!=j:
                
                # The Horizontal Distance Difference
                theXDiff=abs(myContourProperties[i][0]-myContourProperties[j][0])
                
                # The Vertical Distance Difference
                theYdiff=abs(myContourProperties[i][1]-myContourProperties[j][1])
                
                # The Difference of Width
                theWDiff=abs(myContourProperties[i][2]-myContourProperties[j][2])
                
                # The Difference of Height
                theHDiff=abs(myContourProperties[i][3]-myContourProperties[j][3])
                
                #Apply contstraints to remove characters which are not part of the Number Plate
                if 10<theXDiff<=100 and theYdiff<2 and theWDiff<2 and theHDiff<2:  
                    myfinalplate.append(myContourProperties[i])
                    myfinalplate.append(myContourProperties[j])
            j=j+1
        i=i+1
    
    *myfinalplate,=map(list,{*map(tuple,myfinalplate)})
    
    # Just to print the lenth of characters which may belong to the plate
    #print(len(myfinalplate))
    
    # To print the characters which belong to the plate
    #print(myfinalplate)
    
    
    
    
    
    
    
    i=0
    theindexofUsefulContours=[]
    while i<len(myfinalplate):
        theindexofUsefulContours.append(myfinalplate[i][4])
        i=i+1
    
    #To print the Index of useful Contours
    #print("The Index of Useful Contours",theindexofUsefulContours)
    
    
    
    
    updatedContourListto=[]
    i=0
    while i<len(theindexofUsefulContours):
        updatedContourListto.append(contours[theindexofUsefulContours[i]])
        i=i+1
    
    
    
    
    myfinalplate = sorted(myfinalplate, key=itemgetter(1),reverse=True)
    
    # print the possible characters after applying constraintas
    #print(myfinalplate)
    
    
    
    
    
    color = (255,255,255) 
      
    
    
    myfinalplate = myfinalplate[:len(myfinalplate)-2]
    
    storeValueOfX=[]
    storeValueOfY=[]
    storeValueOfW=[]
    storeValueOfH=[]
    i=0
    while i<len(myfinalplate):
        storeValueOfX.append(myfinalplate[i][0])
        storeValueOfY.append(myfinalplate[i][1])
        storeValueOfW.append(myfinalplate[i][2])
        storeValueOfH.append(myfinalplate[i][3])
        i=i+1
    
    themodeX=int(statistics.mean(np.asarray(storeValueOfX)))
    themodeY=int(statistics.mean(np.asarray(storeValueOfY)))
    themodeW=int(statistics.mean(np.asarray(storeValueOfW)))
    themodeH=int(statistics.mean(np.asarray(storeValueOfH)))
    
    # To print the average value of X,Y,W,H of possible contours
    #print("ValueOfX",storeValueOfX)
    #print("ValueOfY",storeValueOfY)
    #print("ValueOfW",storeValueOfW)
    #print("ValueOfH",storeValueOfH)
    
    theusefulnumber=len(myfinalplate)-1
    
    myfinalplate = sorted(myfinalplate, key=itemgetter(0),reverse=True)
    
    # To print possible characters which may belong to the plate
    #print(myfinalplate)
    
      
    # To print average Y and X values for the characters
    #print("The Approximated Plate Y Is:",themodeY)
    #print("The Approximated Plate  X Is:",themodeX)
    
    
    #Lets featch the points from contour which belongs to the number plate
    
    
    
    i=0
    charBelongsToPlate=[]
    while i<possibleCharFromContour.shape[0]-1:
        cnt = possibleCharFromContour[i]
        x,y,w,h = cv2.boundingRect(cnt)
        theYPlDiff=abs(themodeY-y)
        theWPlDiff=abs(themodeW-w)
        theHPlDiff=abs(themodeH-h)
        if (-3<=theYPlDiff<=3)  and (-3<=theHPlDiff<=3):
            charBelongsToPlate.append([x,y,w,h,i])
        i=i+1
        
    # To print the characters belongs to the plate
    #print("Char Belongs To Plate Are:\n",)
    #print(charBelongsToPlate)
    
    if len(charBelongsToPlate)==0:
        i=0
        themodeY=int(statistics.mode(np.asarray(storeValueOfY)))
        themodeH=int(statistics.mode(np.asarray(storeValueOfH)))
        charBelongsToPlate=[]
        while i<possibleCharFromContour.shape[0]-1:
            cnt = possibleCharFromContour[i]
            x,y,w,h = cv2.boundingRect(cnt)
            theYPlDiff=abs(themodeY-y)
            theWPlDiff=abs(themodeW-w)
            theHPlDiff=abs(themodeH-h)
            if (-3<=theYPlDiff<=3) and (-3<=theHPlDiff<=3):
                charBelongsToPlate.append([x,y,w,h,i])
            i=i+1
        
        # To print the characters belongs to the plate
        #print("Char Belongs To Plate Are:\n",)
        #print(charBelongsToPlate)
    
    
    
    sortedXbelongstoPlate=sorted(charBelongsToPlate, key=itemgetter(0))
    sortedYbelongstoPlate=sorted(charBelongsToPlate, key=itemgetter(1))
    theMinimumPlateX=sortedXbelongstoPlate[0][0]
    theMaximumPlateX=sortedXbelongstoPlate[-1][0]
    theMinimumPlateY=sortedYbelongstoPlate[0][1]
    theMaximumPlateY=sortedYbelongstoPlate[-1][1]
    
    # To print the maximum value of X,Y,W,H
#    print("The Max X:",theMaximumPlateX)
#    print("The Min X:",theMinimumPlateX)
#    print("The Max Y:",theMaximumPlateY)
#    print("The Min Y:",theMinimumPlateY)
    
    
    
    drawbeginX=theMinimumPlateX-30
    drawbeginY=theMinimumPlateY-5
    drawendX=theMaximumPlateX+themodeW+30
    drawendY=theMaximumPlateY+themodeH+5
    
    start_point = (drawbeginX,drawbeginY)
    end_point =(drawendX,drawendY)
    thickness = 3
    drawRect=cv2.rectangle(myrealimage, start_point, end_point, color, thickness)
    cv2.imshow("License Plate Detected:",drawRect)
    # End of Number Plate Detection
     
    # To print the detected location of License Plate
#    print("drawbeginX",drawbeginX)
#    print("drawbeginY",drawbeginY)
#    print("drawendX",drawendX)
#    print("drawendY",drawendY)
    
    ThePlateImage = realimage[drawbeginY:drawendY,drawbeginX:drawendX]
    
    
    cv2.imshow("The Plate Image",ThePlateImage)
    
    
    ############################## License Plate Detection Ends Here
    
    
    ############################## Beginning of Character Segementation
    
    ThePlateImage=cv2.cvtColor(ThePlateImage, cv2.COLOR_BGR2GRAY)
    height, width= ThePlateImage.shape
    TheBlurredPlateImage = cv2.medianBlur(ThePlateImage,5)
    
    TheThresedPlateImage=cv2.adaptiveThreshold(TheBlurredPlateImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
    
    ThePlatecontours, ThePlatehierarchy = cv2.findContours(TheThresedPlateImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    PossibleThePlatecontours=[]
    i=0
    while i<len(ThePlatecontours):
        cnt = ThePlatecontours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        
        # Segment the characters on the basis of their difference of height with respect to the themodeH
        thewePlDiff=abs(themodeH-h)
        if -4<thewePlDiff<4:
            PossibleThePlatecontours.append(cnt)
        i=i+1
    
    ThePlateZeroImage = np.zeros((height, width, 3), np.uint8)
    
    ThePlatetoShowCont=cv2.drawContours(ThePlateZeroImage, PossibleThePlatecontours, -1, (255,255,255), 1)
    
    cv2.imshow("The Plate Contours",ThePlatetoShowCont)
    
    
    ############################## End Of Character Segementation
    
    
    ##############################  Begin Optical Character Recognition
    
    
    # Calculate x,y,w,h of characters
    i=0
    ToReArrangeX=[]
    while i<len(PossibleThePlatecontours):
        
        # Calculate x,y,w,h of characters using boundingRect Method
        x,y,w,h=cv2.boundingRect(PossibleThePlatecontours[i])
        
        # Store the horizontal distance and index of characters in a List
        thepair=[x,i]
        ToReArrangeX.append(thepair)
        i=i+1
    
    # Arrange Characters in the increasing order of X Distance where (0,0) is Top_Left
    ToReArrangeX = sorted(ToReArrangeX, key=itemgetter(0))
    
    # To print the array of recognized characters
    #print(ToReArrangeX)
    
    i=0
    theRealCharsInPlateArr=[]
    while i<len(ToReArrangeX):
        
        # Store the characters in the Increaing Order of Horizontal Distance
        theRealCharsInPlateArr.append(PossibleThePlatecontours[ToReArrangeX[i][1]])
        
        i=i+1
    
    PossibleThePlatecontours=theRealCharsInPlateArr
    
    
    #### Begin the Code To View a Character at a particular index. It can be commented if you don't wish to see a character at a particular index
    
    cnnnn2=PossibleThePlatecontours[0]
    
    Theuseout=cv2.drawContours(np.zeros((1000, 1000, 3), np.uint8), [cnnnn2], -1, (255,255,255), 1)
    
    # To View A Particular Contour
    #cv2.imshow("A Particular Character",Theuseout)
    
    #### End the Code To View a Particular Character.
    
    
    
    MyData=[]
    with open('realme.pkl','rb') as f:
        while True:
            try:
                
                # Load Data from pickle file and 
                MyData.append(pickle.load(f))
                
            except EOFError:
                break
        
    
            
    with open('realme.pkl','wb') as f:
        k=0
        while k<len(MyData):
            
            # Add Data to pickle file
            pickle.dump(MyData[k],f)
            k=k+1
            
     
    
    
    
    
    
    ####  This code is used for training. I am commenting this code. Once training is done.       
            
            
            
#        entry1=['Z',PossibleThePlatecontours[0]]
#        pickle.dump(entry1, f)
#        entry2=['D',PossibleThePlatecontours[1]]
#        pickle.dump(entry2, f)
#        entry3=[1,PossibleThePlatecontours[2]]
#        pickle.dump(entry3, f)
#        entry4=[2,PossibleThePlatecontours[3]]
#        pickle.dump(entry4, f)
#        entry5=[5,PossibleThePlatecontours[4]]
#        pickle.dump(entry5, f)
#        entry6=['A',PossibleThePlatecontours[5]]
#        pickle.dump(entry6, f)
#        entry7=['M',PossibleThePlatecontours[6]]
#        pickle.dump(entry7, f)
#        entry8=[7,PossibleThePlatecontours[7]]
#        pickle.dump(entry8, f)
        
            
            
            
            
            
            
            
            
            
            
            
            
            
    #### End of trainging. The Above code should be commented if there is no training.
    
    
    
    
    
    
    
    
    theData=[]
    
    # Open the Pickle File and store all the Data in an array
    with open('realme.pkl','rb') as f:
        while True:
            try:
                theData.append(pickle.load(f))
            except EOFError:
                break
        
     
    
    lengthOfPickle=len(theData)
    lengthOfCharacters=len(PossibleThePlatecontours)
    
        
    
    i=0
    TheLincensePlateNum=[]
    while i<lengthOfCharacters:
        j=0
        diffShapesArr=[]
        while j<lengthOfPickle:
            
            # Find the percentage match of characters in the license plate with the Data in pickle File
            TheDiffBShapes=cv2.matchShapes(PossibleThePlatecontours[i],theData[j][1],1,0.0)
            
            # Store the disimilarity in an array
            diffShapesArr.append(TheDiffBShapes)
            
            j=j+1
        
        # Find the stored pickle value which has mimimal dissmilairy with the given characters in the license plate. And, store it in a list
        TheLincensePlateNum.append(theData[np.argmin(diffShapesArr)][0])
        i=i+1
    
    
    
    # The list contains the recognized license plate number
    print("The License Plate Number Is:",TheLincensePlateNum)
    label1.configure(text="The License Plate Number Is")
    label2.configure(text=TheLincensePlateNum)
    
    ############################## End Of Optical Character Recognition


cv2.waitKey(0)
window.mainloop()
cv2.distroyAllWindows()