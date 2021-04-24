import tkinter as tk
import math
from pathlib import Path


import numpy
from main import activate

windowWidth = 750
windowHeight = 400

canvasWidth = 950
canvasHeight = 800

titleStyle = ("Times", 20, "bold")

def getInstructionsText(block):
    text = ""
    for instr in block.get_instructions():
        text += str(instr)
        text += '\n'
    return text

def createNode(x, y, r, nodeText, canvasName):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    text = canvasName.create_text((x, y), text=nodeText)
    canvasName.create_oval(x0, y0, x1, y1, fill='red')
    return canvasName.tag_raise(text)

def createLink(begining, end, weigth, canvasName, putWeigths = True):
    Ax,Ay = begining
    Bx, By = end
    d = math.sqrt((Bx-Ax)**2 + (By-Ay)**2)    
    newx1 = Ax + 20/d*(Bx-Ax)
    newy1 = Ay + 20/d*(By-Ay)

    newx2 = Ax + (d-20)/d*(Bx-Ax)
    newy2 = Ay + (d-20)/d*(By-Ay)
   
    if(putWeigths):
        textX = Ax + 1/2*(Bx-Ax)
        textY = Ay + 1/2*(By-Ay)
        text = canvasName.create_text((textX, textY), text=str(weigth))

    return canvasName.create_line(newx1, newy1, newx2, newy2, arrow=tk.LAST)

def drawGraph(canvas, graph):

    positions = {}
    heightFromTop = 60
    for k,v in graph.items():
        size = 20
        if(k in [1,2]):
            currentX = canvasWidth/2
            currentY =  heightFromTop * int(k)
        elif (k in [3,4]):
            currentY = heightFromTop * 3 - (k-3)*20
            currentX = float(canvasWidth)/7 * k
        elif(k in [5,6]):
            currentY = heightFromTop * 4
            currentX = float(canvasWidth)/7 * (k-2)
        elif(k in [7,8]):
            currentY = heightFromTop * 5
            currentX = float(canvasWidth)/7 * (k-4)
        elif(k in [9,10]):
            currentY = heightFromTop * 6
            currentX = float(canvasWidth)/7 * (k-6)
        elif(k == 11):
            currentY = heightFromTop * 7
            currentX = canvasWidth/2 
        elif(k in [12,13]):
            currentY = heightFromTop * 8
            currentX = float(canvasWidth)/7 * (k-9)
        elif(k in [14,15]):
            currentY = heightFromTop * 9
            currentX = float(canvasWidth)/7 * (k-11)
        elif(k in [16,17]):
            currentY = heightFromTop * 10 + 20*(k-16)
            currentX = float(canvasWidth)/7 * (k-13)
        elif(k =='START'):
            currentX = 50
            currentY =  heightFromTop
        elif(k =='EXIT'):
            currentX = 50
            currentY = 600 + heightFromTop
        else: 
            currentX = heightFromTop * 11
            currentY = float(canvasWidth)/20 * k-17

        createNode(currentX, currentY, size, k, canvas)
        positions[k] = (currentX, currentY)
    
    return positions
        
def drawLinks(canvas, positions, graph, drawWeights=True):
    links = []
    for k,v in graph.items():
        try: 
            startDimesions = positions[k]
            for item in v:
                endDimensions = positions[item[0]]
                links.append(createLink(startDimesions, endDimensions,item[1], canvas, drawWeights))
        except:
            print("Not found")
    return links

def deleteAllLinks(canvas, links):
    for line in links:
        canvas.delete(line)

class mainWindow:
    def __init__(self, root):
        self.root = root
        self.codeText= self.setCodeText()
        self.errorLabel = tk.Label(root, fg='red', justify=tk.LEFT)

        self.codeText.update()
        codeTextWidth = self.codeText.winfo_width()
        
        btn = tk.Button(root, text="Submit code", command=(lambda: self.submitData()))
        btn.place(x=20+codeTextWidth, rely=10/windowHeight)

        # Set clear button
        btn = tk.Button(root, text="Clear code", command=(lambda: self.clear()))
        btn.place(x=20+codeTextWidth, rely=50/windowHeight)

        btn = tk.Button(root, text="Generate canvas", command=(lambda: self.openNewWindow()))
        btn.place(x=20+codeTextWidth, rely=90/windowHeight)

    def clear(self):
        self.codeText.delete('1.0', tk.END)
        self.errorLabel.place_forget()
    
    def setCodeText(self):
        # setup the text input
        numOfLines = 80
        codeText = tk.Text(self.root, width=numOfLines)
        scroll = tk.Scrollbar(self.root, command=codeText.yview)
        codeText.configure(yscrollcommand=scroll.set)
        codeText.place(relx=10/windowWidth, rely=10/windowHeight)
        test_file = open(Path("test_input.py"), 'r')
        codeText.insert(tk.END, test_file.read())
        return codeText

    def changeGrapthTextTitle(self, text, title):
        self.graphTitle['text'] = title
        self.graphDescription.delete(1.0, tk.END)
        self.graphDescription.insert(1.0, text)

    def drawGraphTextAndTitle(self, text, title):
        self.graphDescription =  tk.Text(self.graphWindow, width=32, wrap=tk.WORD)
        self.graphTitle = tk.Label(self.graphWindow,font=titleStyle, text=title)
        self.graphDescription.place(x=canvasWidth+10, y=150)
        self.graphTitle.place(x=canvasWidth+ 10, y = 50)
        self.graphDescription.insert(tk.END, text)
        #self.graphDescription.configure(state='disabled')


    def drawControlFlowGraph(self):
        cfgDesc = "Od generisanih blokova u kodu konstruiše se Graf kontrole toka. Dodaju se START i EXIT čvorovi da bi dobijen graf bio povezan"
        self.drawGraphTextAndTitle(cfgDesc, "Graf kontrole toka")
        self.lines = drawLinks(self.canvas, self.positions, self.graph, False)
        self.nextBtn = tk.Button(self.graphWindow, text="Generiši razapinjujuće stablo", command=(lambda: self.drawSpanningTree()))
        self.nextBtn.place(x=canvasWidth+20, y=650)


    def drawSpanningTree(self):
        sptDesc = "Razapinjuće stablo grafa kontrole toka. Dobija se primenom DFS algoritma gde je kao početni čvor izabran EXIT."
        self.changeGrapthTextTitle(sptDesc, "Razapinjuće stablo")
        deleteAllLinks(self.canvas, self.lines)
        self.lines = drawLinks(self.canvas, self.positions, self.spanning_tree, False)
        self.nextBtn.place_forget()
        self.nextBtn = tk.Button(self.graphWindow, text="Generiši inverz stabla", command=(lambda: self.drawInverseSpaningTreeNoWeights()))
        self.nextBtn.place(x=canvasWidth+20, y=650)

    def drawInverseSpaningTreeNoWeights(self):
        sptDesc = "Sve grane koje se nalaze u razapinjućem stablu se uklanjaju. Na osnovu preostalih grana i njihovih težina će se izračunati težine uklonjenih grana. Na mesto preostalih grana se u kodu postavljaju brojači."
        self.changeGrapthTextTitle(sptDesc, "Uklanjanje stabla")
        deleteAllLinks(self.canvas, self.lines)
        self.lines = drawLinks(self.canvas, self.positions, self.inv_spanning_tree, False)
        self.nextBtn.place_forget()
        self.nextBtn = tk.Button(self.graphWindow, text="Dodaj težine", command=(lambda: self.drawInverseSpaningTree()))
        self.nextBtn.place(x=canvasWidth+20, y=650)
        
    def drawInverseSpaningTree(self):
        sptDesc = "Izvršavanje koda sa brojačima. Vrednost brojača se postavlja kao težina grane i predstavlja broj puta koliko je ta grana izvršena u izvršavanja programa."
        self.changeGrapthTextTitle(sptDesc, "Dodavanje težina granama")
        deleteAllLinks(self.canvas, self.lines)
        self.lines = drawLinks(self.canvas, self.positions, self.inv_spanning_tree, True)
        self.nextBtn.place_forget()
        self.nextBtn = tk.Button(self.graphWindow, text="Dodaj težine za ostale grane", command=(lambda: self.drawList(0)))
        self.nextBtn.place(x=canvasWidth+20, y=650)

    def drawList(self, i):
        sptDesc = "Poslednji korak u kome se dodeljuju težine svim granama u grafu u odnosu na težine grana koje ne pripadaju razapinjucem stablu."
        self.changeGrapthTextTitle(sptDesc, "Dodavanje težina ostalim \n granama")
        numOfSteps = len(self.list)
        if(i < numOfSteps):
            deleteAllLinks(self.canvas, self.lines)
            self.lines = drawLinks(self.canvas, self.positions, self.list[i], True)
            self.nextBtn.place_forget()
            self.nextBtn = tk.Button(self.graphWindow, text="Dodaj težinu za sledeću granu" , command=(lambda: self.drawList(i+1)))
            self.nextBtn.place(x=canvasWidth+20, y=650)
        else:
            self.nextBtn.place_forget()


    def openNewWindow(self): 
        newWindow = tk.Toplevel() 
        newWindow.title("Vizuelizacija knutovog algoritma") 
        newWindow.geometry("1280x700")
        self.graphWindow = newWindow 


        self.canvas = tk.Canvas(self.graphWindow, bg="gray", height=canvasHeight, width=canvasWidth)
        self.positions = drawGraph(self.canvas, self.graph)
        
        # draw graph
        self.drawControlFlowGraph()
        self.canvas.pack(side=tk.LEFT)
  

    def submitData(self):
        input = self.codeText.get("1.0",'end-1c')
        codeTextWidth = self.codeText.winfo_width()
        try:
            blocks, graph, spanning_tree, inv_spanning_tree, calculate_weights_steps = activate(input)
        except Exception as e:
            self.errorLabel['text'] = "Syntax error: \n" + str(e)
            self.errorLabel.place(x=20+codeTextWidth, rely=100/windowHeight)
            return

        self.codeText.delete('1.0', tk.END)
        for block in blocks:
            self.codeText.insert(tk.END, block.stringify_block())
            self.codeText.insert(tk.END, "\n")
        self.errorLabel.place_forget()

        self.blocks = blocks
        self.graph = graph
        self.spanning_tree = spanning_tree
        self.inv_spanning_tree = inv_spanning_tree
        self.list = calculate_weights_steps


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(str(windowWidth) + 'x' + str(windowHeight))
    app = mainWindow(root)
    app.root.title("Knutov algoritam")
    root.mainloop()

