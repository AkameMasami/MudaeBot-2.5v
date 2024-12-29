import datetime as dt
from tkinter import Tk
import tkinter as tk
import pyautogui as pyag
import pyperclip
import os
from PIL import Image, ImageTk
import time as tm

root = Tk()

#default var
divorce_list = []
claim = False
alredy_claim = False
manual_claim = False
double_tab = False

pos_y = int(569) 
pos_x = int(404)

time_to_claim = "45"
rolls = 10
what_tab = "-"

first_tab = False
second_tab = False

delay_roll = 875 # recommended not to put lower than this 

imageb = Image.open(".gitignore/image.png") # background img here
imageb = imageb.resize((1500, 900)) # size background 
bg_image = ImageTk.PhotoImage(imageb) # processing to the tkinter photo image

# root config related:
def rootConfig():
    root.title("Mudae Auto")
    root.config(bg="#D9EAFD")

    width = 1500
    height = 850
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f"{width}x{height}+{x}+{y}")

def minizeTab():
    root.iconify()

# changing,adding or removing var related:
def changeClaimStatus():
    global claim
    claim = not claim

def changeTime():
    global time_to_claim
    time_get_len = len((changeTimeEntry.get()))
    time_get = (changeTimeEntry.get())
    if time_get and time_get_len <= 2 and time_get_len > 0  and time_get.isnumeric():
        time_to_claim = changeTimeEntry.get()
        changeTimeLabel.config(text=f"set to: {time_to_claim}m")
    else:
        changeTimeLabel.config(text=f"value error")
def changeRolls():
    global rolls
    if not (rollEntry.get()).isnumeric() :
        rollLabel.config(text=f"please insert a int number")
    else:
        rolls = rollEntry.get()
        rollLabel.config(text=f"actual: {rolls}")

def changeDelay():
    global delay_roll
    if not delayEntry.get():
        delayLabel.config(text="insert the delay")
    elif not (delayEntry.get()).isnumeric():   
        delayLabel.config(text="insert a number")
    else:
        delay_roll = delayEntry.get()
        delayLabel.config(text=f"delay:{delay_roll} sec")
        delay_roll = int(delayEntry.get()) * 1000
        

def addCharacter():
    pyperclip.copy("")
    root.withdraw()
    root.after(2000)
    pyag.hotkey("ctrl","c")
    new_char = pyperclip.paste()
    if new_char and not new_char.isnumeric():
        divorce_list.append(new_char)
        divorceLabelItems.config(text=str(len(divorce_list))+" ✓") 
    else:
        divorceLabelItems.config(text=str(len(divorce_list))+" ❌")
    root.deiconify()
    print(' '.join(divorce_list))

def removeCharacter():
    global divorce_list
    if len(divorce_list) > 0:
        divorce_list.pop()
        divorceLabelItems.config(text=str(len(divorce_list))+" ✓💣")
    print(' '.join(divorce_list))

# executing related:
def executeDivorce():
    global divorce_list
    root.withdraw()
    pyag.click(1061, 557)
    pyag.hotkey("ctrl","a")
    pyag.hotkey("delete") 
    for i in divorce_list:
        pyag.write("$divorce " + i)
        pyag.hotkey("Enter")
        root.after(750)
        pyag.write("y")
        pyag.hotkey("Enter")
        root.after(750)

    divorce_list.clear()
    divorceLabelItems.config(text=str(len(divorce_list)))
    root.deiconify()

def deleteData():
    with open("data.txt", "w") as f:
        f.write("[Registration Rolls Price]")

def getNewPos():
    global pos_x,pos_y
    root.withdraw()
    pyag.alert("Put the cursor on the new pos\nthem press enter to close the alert")
    hard_pos_x,hard_pos_y = pyag.position()
    pos_x,pos_y = hard_pos_x,hard_pos_y

    posLabel.config(text=f"x:{pos_x}, y: {pos_y}")

    frameLeftBottomB.config(padx=13)
    root.deiconify()

def updateManual():
    global manual_claim
    if manual_claim == True:
        manual_claim = False
    else:
        manual_claim = True


def doubleTabStatus():
    global double_tab
    double_tab = not double_tab
    doubleTabButton.config(bg="green",text="ON") if double_tab else doubleTabButton.config(bg="#801515",text="OFF")
    rollLabelFirst.grid(column=0,row=0) if double_tab else rollLabelFirst.grid_forget()

def sendData(data):
    data = str(data)
    data = data + "\n"
    with open("data.txt", "a") as f:
        f.write(data)

def separate(text=None):
    sendData("-----") if text is None else sendData(text)
    

def getPrice(rolls,what_tab):
    global pos_x,pos_y,first_tab,second_tab,first_status
    now_time = dt.datetime.now() 
    time = now_time.strftime("%H:%M")
    rolls = int(rolls)
    rolls_get = 0

    root.withdraw()

    pyag.click(1061,557)
    pyag.hotkey("ctrl","a")
    root.after(500)

    for i in range(0,rolls):
        rolls_get += 1
        print("Process roll number: ",rolls_get)

        pyperclip.copy("")

        pyag.write("$w")
        pyag.hotkey("Enter")

        root.after(1500)

        pyag.doubleClick(pos_x,pos_y)
        pyag.hotkey("ctrl","c")

        price = pyperclip.paste()
        root.after(100)

        if not price.isnumeric():
            new_pos_y = pos_y
            new_pos_x = pos_x
            for t in range(0,10+1):
                pyag.hotkey("ctrl","c")
                pyag.doubleClick(new_pos_x,new_pos_y)
                
                price = pyperclip.paste()
                if price.isnumeric():
                    break
                root.after(delay_roll)
                new_pos_y -= 5

            price = pyperclip.paste()
            new_pos_y = pos_y # reset the new_pos_y var

            if not price.isnumeric():
                for x in range(0,10+1):
                    if price.isnumeric():
                        break
                    root.after(delay_roll)
                    pyag.hotkey("ctrl","c")
                    pyag.doubleClick(new_pos_x,new_pos_y)
                    price = pyperclip.paste()
                    if price.isnumeric():
                        break
                    pos_y += 5

            if not price.isnumeric():
                rolls_get -= 1
                if what_tab == 0:
                    statusClaim.config(text=f"Status: Error on getting rolls\nrolls get: {rolls_get}", fg="red")
                elif what_tab == 1:
                    first_tab = f"1 Tab: Error on getting rolls\nrolls get: {rolls_get}"
                    first_status = False
                    statusClaim.config(text=f"{first_tab}", fg="red")
                else:
                    second_tab = f"\n2 Tab: Error on getting rolls\nrolls get: {rolls_get}"
                    if not first_status:
                        statusClaim.config(text=f"{first_tab}{second_tab}", fg="blue")
                    else:
                        statusClaim.config(text=f"{first_tab}{second_tab}", fg="red")
                break
        else:
            price = int(price)

        data_with_time = time + f" [Auto Claim] - {what_tab}\n" +  str(price) if not manual_claim else time + " [Manual Claim]\n" +  str(price)
        data = data_with_time if i == 1 else price
                
               
        
        
        sendData(data)
        if int(price) > 100:
            pyag.click(414,933)
            statusClaim.config(text=f"Status: Claimed a character\nrolls get: {rolls_get}\nprice get: {price}", fg="green")
            separate("=-#-=")
            data = f"{price} - Claimed"
            separate("=-#-=")
            sendData(data)
            break

        root.after(1000)

    separate(None)
    if rolls_get != rolls:
        statusClaim.config(text=f"Status: Error on getting rolls\nrolls get: {rolls_get}", fg="red")
    else:
        if what_tab == 0:
            statusClaim.config(text=f"Status: Rolls successfully completed\nrolls get: {rolls_get}", fg="green")
        elif what_tab == 1:
            first_tab = f"1 Tab: Rolls successfully completed\nrolls get: {rolls_get}"
            first_status = True
            statusClaim.config(text=f"{first_tab}", fg="green")
        else:
            second_tab = f"\n2 Tab: Rolls successfully completed\nrolls get: {rolls_get}"
            if not first_status:
                statusClaim.config(text=f"{first_tab}{second_tab}", fg="blue")
            else:
                statusClaim.config(text=f"{first_tab}{second_tab}", fg="green")

        
rootConfig()

bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

labelTime = tk.Label(root, text="", bg="#D9EAFD", fg="#9AA6B2")
labelTime.pack(pady=50)

statusClaim = tk.Label(root, text="Status: waiting...",font=("Fira Code Light",10))
statusClaim.pack(pady=10)

buttonClaim = tk.Button(root, text='', command=changeClaimStatus)
buttonClaim.pack()

frame = tk.LabelFrame(root, text="options",font=("Fira Code Light",10,"bold"),pady=50,padx=50)
frame.pack(pady=(30,0)) 
#change time R
frameRight  = tk.LabelFrame(frame, text="Change Time",font=("Fira Code Light",7,"bold"),pady=13,padx=20,bg="gray")
frameRight.grid(row=0,column=2,padx=(5,0),pady=(0,15))

#num rolls R
frameRightBottom = tk.LabelFrame(frame, text="Change Num Rolls",font=("Fira Code Light",7,"bold"),pady=10,padx=20,bg="gray")
frameRightBottom.grid(row=1,column=2,padx=(5,0),pady=(0,15))

#divorce R
frameRightBottomB = tk.LabelFrame(frame, text="Multiple Divorce",font=("Fira Code Light",7,"bold"),pady=10,padx=20,bg="gray")
frameRightBottomB.grid(row=2,column=2,padx=(5,0),pady=(0,15))

# change delay roll RR
frameRightR = tk.LabelFrame(frame, text="Change delay",font=("Fira Code Light",7,"bold"),pady=10,padx=20,bg="gray")
frameRightR.grid(row=0,column=3,padx=(5,0),pady=(0,15))

#manual activator L
frameLeft = tk.LabelFrame(frame, text="Manual Activator",font=("Fira Code Light",7,"bold"),pady=20,padx=20,bg="gray")
frameLeft.grid(row=0,column=0,padx=(0,5),pady=(0,15))

#double tab L 
frameLeftBottom = tk.LabelFrame(frame, text="Dis Double Tab",font=("Fira Code Light",7,"bold"),pady=25,padx=20,bg="gray")
frameLeftBottom.grid(row=1,column=0,padx=(0,5),pady=(0,15))

#new pos L
frameLeftBottomB= tk.LabelFrame(frame, text="New Position",font=("Fira Code Light",7,"bold"),pady=20,padx=20,bg="gray")
frameLeftBottomB.grid(row=2,column=0,padx=(0,5),pady=(0,15))

infoLabelTop = tk.Label(frame, text="<- Activate the \nmanual claimer\n\nChange the \ntime (only min) ->",font=("Fira Code Light",7,"bold"))
infoLabelTop.grid(row=0,column=1)

infoLabelBottom = tk.Label(frame, text="<- Activate the \ndouble tab \ndiscord claimer\n\nChange the \nnumber of rolls ->",font=("Fira Code Light",7,"bold"))
infoLabelBottom.grid(row=1,column=1)

# pyag.click(1061,557)

#double tab button
doubleTabButton = tk.Button(frameLeftBottom,text=" OFF ", command=doubleTabStatus,font=("Fira Code Light", 7,"bold"),width=10,bg="#801515")
doubleTabButton.pack()


#manual activator 
manualButton = tk.Button(frameLeft, text="Activate", command=updateManual,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
manualButton.grid(row=1,column=0)

#change time
changeTimeEntry = tk.Entry(frameRight,font=("Fira Code Light", 7,"bold"),width=10)
changeTimeEntry.grid(row=0,column=0)

changeTimeButton = tk.Button(frameRight, text="Change", command=changeTime,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
changeTimeButton.grid(row=1,column=0) 

changeTimeLabel = tk.Label(frameRight, text=f"set to: {time_to_claim}m", bg="gray",font=("Fira Code Light", 7,))
changeTimeLabel.grid(row=2,column=0)

#change delay
delayEntry = tk.Entry(frameRightR,font=("Fira Code Light", 7,"bold"),width=10)
delayEntry.pack()

delayButton = tk.Button(frameRightR, text="Change", command=changeDelay,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
delayButton.pack()

delayLabel = tk.Label(frameRightR,text=f"use secounds",bg="gray",font=("Fira Code Light", 7,))
delayLabel.pack()

#num roll change
rollLabelFirst = tk.Label(frameRightBottom,text=f"First Tab",bg="gray",font=("Fira Code Light", 7,))
rollLabelFirst.grid(column=0,row=0)
rollLabelFirst.grid_forget()

rollEntry = tk.Entry(frameRightBottom,font=("Fira Code Light", 7,"bold"),width=10)
rollEntry.grid(column=0,row=1)

roolButton = tk.Button(frameRightBottom, text="Change", command=changeRolls,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
roolButton.grid(column=0,row=2)

rollLabel = tk.Label(frameRightBottom,text=f"actual : {rolls}",bg="gray",font=("Fira Code Light", 7,))
rollLabel.grid(column=0,row=3)

rollLabelFirst = tk.Label(frameRightBottom,text=f"First Tab",bg="gray",font=("Fira Code Light", 7,))
rollLabelFirst.grid(column=0,row=0)
rollLabelFirst.grid_forget()

rollEntry = tk.Entry(frameRightBottom,font=("Fira Code Light", 7,"bold"),width=10)
rollEntry.grid(column=0,row=1)

roolButton = tk.Button(frameRightBottom, text="Change", command=changeRolls,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
roolButton.grid(column=0,row=2)

rollLabel = tk.Label(frameRightBottom,text=f"actual : {rolls}",bg="gray",font=("Fira Code Light", 7,))
rollLabel.grid(column=0,row=3)


#multiple divorce
divorceButtonAdd = tk.Button(frameRightBottomB, text="Add", command=addCharacter,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
divorceButtonAdd.pack()

divorceButtonRemove = tk.Button(frameRightBottomB, text="Remove", command=removeCharacter,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
divorceButtonRemove.pack(pady=5)


divorceButtonDone = tk.Button(frameRightBottomB, text="Done", command=executeDivorce,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
divorceButtonDone.pack()

divorceLabelItems = tk.Label(frameRightBottomB, text=len(divorce_list),bg="gray",font=("Fira Code Light", 7,))
divorceLabelItems.pack()  

#get new pos
posLabel = tk.Label(frameLeftBottomB, text=f"x:{pos_x}, y: {pos_y}",font=("Fira Code Light", 6),width=15)
posLabel.pack()

getNewPosButton = tk.Button(frameLeftBottomB, text="Start Track", command=getNewPos,font=("Fira Code Light", 7,"bold"), bg="#090F18",width=10,fg="#B6B9BD")
getNewPosButton.pack()

exitButton = tk.Button(frame, text="Minimize", font=("Fira Code Light", 7,"bold"), command=minizeTab, bg="#9AA6B2",width=10)
exitButton.grid(row=4,column=1,pady=(5,0))
#exit button
exitButton = tk.Button(frame, text="Exit", font=("Fira Code Light", 7,"bold"), command=root.destroy, bg="#9AA6B2",width=10)
exitButton.grid(row=5,column=1,pady=(5,0))

timeLabel = tk.Label(frame, text="",font=("Fira Code Light",10))
timeLabel.grid(row=6,column=1)

timeMinLabel = tk.Label(frame, text="",font=("Fira Code Light",10))
timeMinLabel.grid(row=7,column=1)

def updateLabel(text, font, size, eff):
    labelTime.config(text=text, font=(font, size, eff)) 

def mainLoopFunctions():
    global alredy_claim,claim
    now_time = dt.datetime.now() 
    time = now_time.strftime("%H:%M")
    time_as_min = now_time.strftime("%M")

    if claim:
        buttonClaim.config(text="ACTIVATED", bg="#85A98F", font=("Monocraft", 15,"bold"),fg="#D9EAFD",bd=4) # button on
        if time_as_min == time_to_claim or manual_claim:
            updateLabel("CLAIM ACTIVATED", "Monocraft", 40, "bold",) # claim label activated
            root.after(1000)
            if not alredy_claim:
                if not double_tab: 
                    getPrice(rolls,0)
                    
                    
                else:
                    getPrice(rolls,1)
                    pyag.hotkey("alt","tab")
                    getPrice(rolls,2)
                    pyag.hotkey("alt","tab")
                    print(first_tab,second_tab,what_tab)
                    
                root.deiconify()
                alredy_claim = True

                # change the window to mudae


                if manual_claim:
                    updateManual()
        else:
            alredy_claim = False
            updateLabel("WAITING CLAIM", "Monocraft", 30, "italic") # waiting claim
    else:
        updateLabel("CLAIM DEACTIVATED", "Monocraft", 30, "normal") # claim label deactivated
        buttonClaim.config(text="DEACTIVATED", bg="#AB4459", font=("Monocraft", 15,"bold"),fg="#D9EAFD",bd=4) # button off

    time_until_claim = str(int(time_to_claim) - int(time_as_min))
    time_passed_claim = str(60+int(time_until_claim))

    if int(time_until_claim) < 0:
        time_show = time_passed_claim
    else:
        time_show = time_until_claim
        
    timeLabel.config(text=time)
    timeMinLabel.config(text=time_show + "m Until claim")
    root.after(100, mainLoopFunctions) 

mainLoopFunctions()  # Initial call to start the time updates
root.mainloop()  # Start the Tkinter event loop

os.system('cls')

if __name__ == '__main__':
    try:
        print("error exit 0")
    except ValueError:
        print("error exit 1")
    except RuntimeError:
        print("error exit 7")
    except Exception as e:  # Catch any other exceptions
        print(f"An unexpected error occurred: {e}")