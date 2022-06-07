from tkinter import *
from tkinter.colorchooser import askcolor
#needed because tkinter only suports .gif files
from PIL import ImageTk, Image

window = Tk()

#all default settings
action = False
frameBG = "#3d677a"
winWidth, winHeight = 1000, 600
sideBarWidth, sideBarHeight = 200, 600
buttonWidth, buttonHeight = 50, 50
pencilColor = "black"
backgroundColor = "white"
Cords = []
erazeCircleList = []
RulerLineList = []
figureList = []

allDrawnObj = []
allSavedObjParts = []
allObjType = []
ObjDiff = []
diffVar = 0
lineThickness = []

#change pencil color after the button had been clicked and a person has chosen a color
def changePenColor():
    global pencilColor
    chosenColor = askcolor(title = "Color Picker for pencil")
    pencilColor = chosenColor[1]
    
#change backgroundcolor and erazercolor after the button had been clicked and a person has chosen a color
def changeBackgroundColor():
    global backgroundColor
    chosenColor = askcolor(title = "Color Picker for background")
    backgroundColor = chosenColor[1]
    drawingCanv.configure(bg = backgroundColor)
    for ECircle in erazeCircleList:
        drawingCanv.itemconfig(ECircle, fill = backgroundColor) 

def changeValues():
    global pencilRadius
    pencilRadius = ScalePencilRadius.get()
    window.after(100, changeValues)
    
def changeAction(arg):
    global action, ErazeCircle
    action = arg
    if action == "draw":
        drawingCanv.config(cursor = "pencil")
    elif action == "MakeCircle" or action == "MakeSquare" or action == "MakeTriangle" or action == "MakeStraightTriangle":
        drawingCanv.config(cursor = "cross")
    else:
        drawingCanv.config(cursor = "left_ptr")
    
    if action == "eraze":
        ErazeCircle = drawingCanv.create_oval(-1000, -1000, -1000, -1000)
    else:
        drawingCanv.delete(ErazeCircle)

def clickDraw(event):
    global PenPosX, PenPosY, Color, diffVar, ColorChange
    PenPosX, PenPosY = event.x, event.y
    diffVar = len(allDrawnObj) 

    if action == "draw" or action == "Ruler" or action == "eraze":
        if action == "eraze": 
            Color = backgroundColor
        else: 
            Color = pencilColor
        x0, y0 = PenPosX - pencilRadius, PenPosY - pencilRadius
        x1, y1 = PenPosX + pencilRadius, PenPosY + pencilRadius
        circle = drawingCanv.create_oval(x0, y0, x1, y1, fill = Color, outline = "")
        if action == "eraze":
            erazeCircleList.append(circle)
        allDrawnObj.append(circle)
        allObjType.append("circle")
    elif action == "MousePointer":
        for obj in allDrawnObj:
            x0, y0, x1, y1, *args = drawingCanv.coords(obj)
            if x0 <= PenPosX <= x1 and y0 <= PenPosY <= y1:
                ColorChange = drawingCanv.itemcget(obj, "fill")
                break
            else:
                ColorChange = backgroundColor

def moveDraw(event):
    global objType1, objType2, objType3
    if action == "eraze": 
        Color = backgroundColor
    else: 
        Color = pencilColor
    if action == "Ruler":
        lineWidth = 2 * pencilRadius +1
        straightLine = drawingCanv.create_line(PenPosX, PenPosY, event.x, event.y, fill = Color, width = lineWidth)
        x0, y0 = event.x-pencilRadius, event.y-pencilRadius
        x1, y1 = event.x+pencilRadius, event.y+pencilRadius
        RulerPoint = drawingCanv.create_oval(x0, y0, x1, y1, fill=Color, outline = "")
        RulerLineList.append(straightLine)
        RulerLineList.append(RulerPoint)
        objType1 = "line"
        objType2 = "circle"
        lineThickness.append(lineWidth)
        if len(RulerLineList) == 4:
            for _ in range(2):
                drawingCanv.delete(RulerLineList[0])
                del RulerLineList[0]
    elif action == "draw" or action == "eraze":

        x0, y0 = event.x-pencilRadius, event.y-pencilRadius
        x1, y1 = event.x+pencilRadius, event.y+pencilRadius
        circle = drawingCanv.create_oval(x0, y0, x1, y1, fill=Color, outline = "")
        allDrawnObj.append(circle)
        allObjType.append("circle")

        if action == "eraze":
            erazeCircleList.append(circle)

        Coordinate = (event.x, event.y)
        Cords.append(Coordinate)
        if len(Cords) == 2:
            Cord1 = Cords[0]
            Cord2 = Cords[1]
            # +1 because the middle of the circle also counts
            lineWidth = 2 * pencilRadius +1
            line = drawingCanv.create_line(Cord1[0], Cord1[1], Cord2[0], Cord2[1], fill=Color, width = lineWidth)
            lineThickness.append(lineWidth)
            allDrawnObj.append(line)
            allObjType.append("line")
            if action == "eraze":
                erazeCircleList.append(line)
            del Cords[0]

        x0, y0 = event.x - pencilRadius, event.y - pencilRadius
        x1, y1 = event.x + pencilRadius, event.y + pencilRadius
        drawingCanv.coords(ErazeCircle, x0, y0, x1, y1)
        
    elif action == "MakeCircle" or action == "MakeSquare" or action == "MakeTriangle" or action == "MakeStraightTriangle":
        x1, y1 = event.x, event.y
        if action == "MakeCircle":
            figure = drawingCanv.create_oval(PenPosX, PenPosY, x1, y1, fill = Color, outline = Color)
            objType3 = "circle"
        elif action == "MakeSquare":
            figure = drawingCanv.create_rectangle(PenPosX, PenPosY, x1, y1, fill = Color, outline = Color)
            objType3 = "rectangle"
        elif action == "MakeTriangle":
            figure = drawingCanv.create_polygon(PenPosX, y1, (x1-PenPosX)/2 + PenPosX, PenPosY, x1, y1, fill = Color)
            objType3 = "triangle"
        elif action == "MakeStraightTriangle":
            figure = drawingCanv.create_polygon(PenPosX, PenPosY, PenPosX, y1, x1, y1, fill = Color)
            objType3 = "straightTriangle"
        figureList.append(figure)
        
        if len(figureList) == 2:
            drawingCanv.delete(figureList[0])
            del figureList[0]   
            
    drawingCanv.tag_raise(ErazeCircle)

def drawErazeCircle(event):
    if action == "eraze":
        x0, y0 = event.x - pencilRadius, event.y - pencilRadius
        x1, y1 = event.x + pencilRadius, event.y + pencilRadius
        drawingCanv.coords(ErazeCircle, x0, y0, x1, y1)
    else:
        drawingCanv.coords(ErazeCircle, -1000, -1000, -1000, -1000)
    drawingCanv.tag_raise(ErazeCircle)

def buttonRelease(event):
    global pencilColor
    try:
        pencilColor = ColorChange
    except:
        pass
    Cords.clear()
    if len(RulerLineList) > 0:
        allDrawnObj.append(RulerLineList[-2])
        allObjType.append(objType1)
        allDrawnObj.append(RulerLineList[-1])
        allObjType.append(objType2)
    RulerLineList.clear()
    
    if len(figureList) > 0:
        allDrawnObj.append(figureList[-1])
        allObjType.append(objType3)
    figureList.clear()

    if len(allDrawnObj) > 0:
        ObjDiff.append(len(allDrawnObj) - diffVar)

def goBack():
    allSavedObj = []
    if len(allDrawnObj) > 0:
        for _ in range(ObjDiff[-1]):
            tempList = []
            for posValue in drawingCanv.coords(allDrawnObj[-1]):
                tempList.append(posValue)
            tempList.append(drawingCanv.itemcget(allDrawnObj[-1], "fill"))
            if allObjType[-1] == "line":
                tempList.append(lineThickness[-1])
                del lineThickness[-1]
            tempList.append(allObjType[-1])

            allSavedObj.append(tempList)
            drawingCanv.delete(allDrawnObj[-1])
            del allDrawnObj[-1]
            del allObjType[-1]

        allSavedObjParts.append(allSavedObj)
        del ObjDiff[-1]

def goForward():
    global diffVar
    if len(allSavedObjParts) > 0:
        templist = []
        for figObj in allSavedObjParts[-1]:
            if figObj[-1] == "circle":
                figure = drawingCanv.create_oval(figObj[0], figObj[1], figObj[2], figObj[3], fill = figObj[4], outline = figObj[4])
                allObjType.append("circle")
            elif figObj[-1] == "rectangle":
                figure = drawingCanv.create_rectangle(figObj[0], figObj[1], figObj[2], figObj[3], fill = figObj[4], outline = figObj[4])
                allObjType.append("rectangle")
            elif figObj[-1] == "line":
                figure = drawingCanv.create_line(figObj[0], figObj[1], figObj[2], figObj[3], fill = figObj[4], width = figObj[5])
                lineThickness.append(figObj[5])
                allObjType.append("line")
            elif figObj[-1] == "triangle":
                figure = drawingCanv.create_polygon(figObj[0], figObj[1], figObj[2], figObj[3], figObj[4], figObj[5], fill = figObj[6], outline = figObj[6])
                allObjType.append("triangle")
            elif figObj[-1] == "straightTriangle":
                figure = drawingCanv.create_polygon(figObj[0], figObj[1], figObj[2], figObj[3], figObj[4], figObj[5], fill = figObj[6], outline = figObj[6])
                allObjType.append("straightTriangle")

            templist.append(figure)
            allDrawnObj.append(figure)
        ObjDiff.append(len(templist))
        del allSavedObjParts[-1]

def clearCanvWarning():
    def clearCanv(popup, EntryBox):
        answer = EntryBox.get()
        answer = answer.lower()
        popup.destroy()
        if answer == "yes":
            drawingCanv.delete("all")

    popup = Toplevel(window)
    popup.title("Are you sure")
    AreYourSureLabel = Label(popup, text = "Are you sure that you want to delete this peace of art?")
    AreYourSureLabel.pack()
    AreYourSureLabel2 = Label(popup, text = "If you are type yes if not type no:")
    AreYourSureLabel2.pack()
    EntryBox = Entry(popup, width = 15)
    EntryBox.pack()
    subitButton = Button(popup, text = "Submit your choice", command = lambda: clearCanv(popup, EntryBox)).pack()

FrameWidget = Frame(window, width = sideBarWidth, height = sideBarHeight, bg = frameBG, highlightthickness = 0)
FrameWidget.pack(side = LEFT)

drawingCanv = Canvas(window, width = winWidth - sideBarWidth, height = winHeight, bg = "white", highlightthickness = 0)
drawingCanv.pack(side = RIGHT)

ErazeCircle = drawingCanv.create_oval(-1000, -1000, -1000, -1000)

#import all images 
PencilButtonImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/Pencil5.png").resize((buttonWidth, buttonHeight))
PencilButtonImg = PencilButtonImg.transpose(Image.FLIP_TOP_BOTTOM)
PencilButtonImg = PencilButtonImg.transpose(Image.FLIP_LEFT_RIGHT)
PencilButtonImg = ImageTk.PhotoImage(PencilButtonImg) 
EraserButtonImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/eraserFoto.png").resize((buttonWidth, buttonHeight))
EraserButtonImg = ImageTk.PhotoImage(EraserButtonImg) 
RulerButtonImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/liniaal.png").resize((buttonWidth, buttonHeight))
RulerButtonImg = ImageTk.PhotoImage(RulerButtonImg) 
mousePointerImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/mousePointer.png").resize((buttonWidth, buttonHeight))
mousePointerImg = ImageTk.PhotoImage(mousePointerImg) 
CircleImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/CircleIcon.png").resize((buttonWidth, buttonHeight))
CircleImg = ImageTk.PhotoImage(CircleImg) 
SquareImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/squareIcon.png").resize((buttonWidth, buttonHeight))
SquareImg = ImageTk.PhotoImage(SquareImg) 
TriangleImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/triangleIcon.png").resize((buttonWidth, buttonHeight))
TriangleImg = ImageTk.PhotoImage(TriangleImg) 
straightTriangleImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/straightTriangle.png").resize((buttonWidth, buttonHeight))
straightTriangleImg = ImageTk.PhotoImage(straightTriangleImg) 
goBackImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/goBackButton.png").resize((buttonWidth, buttonHeight))
goBackImg = ImageTk.PhotoImage(goBackImg) 
goForwardImg = Image.open("/Users/maxrijkers/Documents/Programs/PaintGUI.zip/goBackButton.png").resize((buttonWidth, buttonHeight))
goForwardImg = goForwardImg.transpose(Image.FLIP_LEFT_RIGHT)
goForwardImg = ImageTk.PhotoImage(goForwardImg) 

#creating all the widgets 
PencilButton = Button(FrameWidget, image = PencilButtonImg, command = lambda: changeAction("draw"), cursor = "hand2")
PencilButton.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 25)

ErazerButton = Button(FrameWidget, image = EraserButtonImg, command = lambda: changeAction("eraze"), cursor = "hand2")
ErazerButton.place(x = (sideBarWidth - 2*buttonWidth)/3*2 + buttonWidth, y = 25)

RulerButton = Button(FrameWidget, image = RulerButtonImg, command = lambda: changeAction("Ruler"), cursor = "hand2")
RulerButton.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 100)

mousePointerButton = Button(FrameWidget, image = mousePointerImg, command = lambda: changeAction("MousePointer"), cursor = "hand2")
mousePointerButton.place(x = (sideBarWidth - 2*buttonWidth)/3*2 + buttonWidth, y = 100)

CircleButton = Button(FrameWidget, image = CircleImg, command = lambda: changeAction("MakeCircle"), cursor = "hand2")
CircleButton.place(x = (sideBarWidth - 2*buttonWidth)/3*2 + buttonWidth, y = 175)

SquareButton = Button(FrameWidget, image = SquareImg, command = lambda: changeAction("MakeSquare"), cursor = "hand2")
SquareButton.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 175)

TriangleButton = Button(FrameWidget, image = TriangleImg, command = lambda: changeAction("MakeTriangle"), cursor = "hand2")
TriangleButton.place(x = (sideBarWidth - 2*buttonWidth)/3*2 + buttonWidth, y = 250)

StraightTriangleButton = Button(FrameWidget, image = straightTriangleImg, command = lambda: changeAction("MakeStraightTriangle"), cursor = "hand2")
StraightTriangleButton.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 250)

goBackButton = Button(FrameWidget, image = goBackImg, command = lambda: goBack(), cursor = "hand2")
goBackButton.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 325)

goForwardButton = Button(FrameWidget, image = goForwardImg, command = lambda: goForward(), cursor = "hand2")
goForwardButton.place(x = (sideBarWidth - 2*buttonWidth)/3*2 + buttonWidth, y = 325)

ChooseColor = Button(FrameWidget, text = 'Pen Color', cursor = "hand2", width = 15, height = 2, command = changePenColor)
ChooseColor.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 400)

ChooseBackgroundColor = Button(FrameWidget, text = 'Canvas Color', cursor = "hand2", width = 15, height = 2, command = changeBackgroundColor)
ChooseBackgroundColor.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 450)

clearCanvasButton = Button(FrameWidget, text = "Clear Canvas", cursor = "hand2", width = 15, height = 2, command = lambda: clearCanvWarning())
clearCanvasButton.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 500)

ScalePencilRadius = Scale(FrameWidget, from_ = 1, to = 100, orient = HORIZONTAL)
ScalePencilRadius.place(x = (sideBarWidth - 2*buttonWidth)/3, y = 550)

#get actions with .bind 
drawingCanv.bind("<Motion>", drawErazeCircle)
drawingCanv.bind("<Button-1>", clickDraw)
drawingCanv.bind('<B1-Motion>', moveDraw)
drawingCanv.bind('<ButtonRelease-1>', buttonRelease)

changeValues()

#other default values 
window.minsize(winWidth, winHeight)
window.maxsize(winWidth, winHeight)
window.title("Drawing Pallet")
window.mainloop()