import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep



cap=cv2.VideoCapture(0) ## image object 
detector=HandDetector(detectionCon=0.8) ## hand object 

cap.set(3,1280)
cap.set(4,720)

finalText=""             # an empty string which conatin the alphabets enter 


keyList = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L",","],
    ["Z","X","C","V","B","N","M","ENTER"]
    
]


def draw(img,buttonlist):
       
       for button in buttonList: ## here button list is a list of button object created with the button class which contain all info about position text and size
       
            x,y=button.pos  ## initial pointof rectangle 
            w,h=button.size ## values added to the initial point

            
            cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED) ## to draw the reactangle 
            cv2.putText(img,button.text,(x+12,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4) # to put text on the screen 

 
# creating a class for buttons on the screen
class Button():
    ## initialisation for all buttons
    def __init__(self,pos,text,size=[60,60]):
        self.pos=pos
        self.text=text
        self.size=size

    
# list which contain all button objects 
buttonList=[]
for i in range(len(keyList)):
        for x,key in enumerate(keyList[i]):
            if key=="ENTER":
                buttonList.append(Button([70*x+10,80*i+20],key,[210,60])) 
            else:     
                buttonList.append(Button([70*x+10,80*i+20],key))

        
while True: 
   success,img= cap.read()
   hands, img=detector.findHands(img)   
   img = cv2.flip(img, 1)  # 1 = horizontal flip   

   lmList = []  # always exists

   ## note hands contain 4 parameters lmlist,bbox,center,type
   if hands:  # check if list is not empty
     lmList = hands[0]['lmList']

     imgWidth = 1280
     lmList[8][0] = imgWidth - lmList[8][0]  
     lmList[12][0] = imgWidth - lmList[12][0]
     # print(lmList)                  it will print the coordinate of all 21 point of a hand 
   draw(img,buttonList)
  
   if lmList:
        for button in buttonList:
             x,y=button.pos
             w,h=button.size


             if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                                      cv2.rectangle(img,button.pos,(x+w,y+h),(147, 20, 255),cv2.FILLED) ## to draw the reactangle  
                                      cv2.putText(img,button.text,(x+12,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4) # to put text on the screen 
                                      # Get coordinates from lmList
                                      p1 = lmList[8][:2]   # index fingertip
                                      p2 = lmList[12][:2]  # middle fingertip
                                      l, _, _ =detector.findDistance(p1,p2,img) 
                                      print(l)

                                    #when clicked 
                                      if l<28:
                                        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED) ## to draw the reactangle 
                                        cv2.putText(img,button.text,(x+12,y+50),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                                        finalText += button.text
                                        sleep(0.5) ## it will delay the pressing speed 

    
   cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED) ## to draw the reactangle 
   cv2.putText(img,finalText,(60,425),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)                                   
              



   

   cv2.imshow("image",img)   
   if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit { ord get the ascii value of the key}
        break
   

cap.release()
cv2.destroyAllWindows()