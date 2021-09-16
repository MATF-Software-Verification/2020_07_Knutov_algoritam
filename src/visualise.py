# runnable class

import tkinter as tk
import math
from pathlib import Path
from main import activate



windowWidth = 800
windowHeight = 400

canvasWidth = 950
canvasHeight = 800

bgCanvasColor = "gray"
bgTopLevelColor = "white"
linesGraphColor = "black"
linesTreeColor = "red"
linesInvColor = "orange"
nodeColor = "blue"
textColor = "black"
bgTextColor = "white"
weigthTextColor = "black"
nodeBorderColor = "black"
lineActiveColor = "white"


titleStyle = ("Times", 20, "bold")

def onWeightClick(event, arg):
    canvas = arg[0]
    id = arg[1]
    num = canvas.itemcget(id,'text')
    num = int(num) +1
    canvas.itemconfigure(id, text= num )





# not used, makes string with forwarded block instructions
def getInstructionsText(block):
    text = ""
    for instr in block.get_instructions():
        text += str(instr)
        text += '\n'
    return text

# draws node
def createNode(x, y, r, nodeText, canvasName):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    text = canvasName.create_text((x, y), text=nodeText)
    canvasName.create_oval(x0, y0, x1, y1, fill=nodeColor, outline=nodeBorderColor, width=2)
    return canvasName.tag_raise(text)

# draws a branch from the beginning to the end with a weigth "weigth" by canvas
def createLink(begining, end, weigth, canvasName, color, putWeigths = True):

    Ax,Ay = begining
    Bx, By = end
    d = math.sqrt((Bx-Ax)**2 + (By-Ay)**2)    
    newx1 = Ax + 20/d*(Bx-Ax)
    newy1 = Ay + 20/d*(By-Ay)

    newx2 = Ax + (d-20)/d*(Bx-Ax)
    newy2 = Ay + (d-20)/d*(By-Ay)


    if(putWeigths):
        # move text above line
        # textX, TextY represent middle of a line
        # computes line that is normal to our line then computes coordinates on that line
        # 1 + k1*k2 = 0 lines are normal
        textX = Ax + 1 / 2 * (Bx - Ax)
        textY = Ay + 1 / 2 * (By - Ay)
        if Ay == By:
            textY = textY + 8
        elif Ax == Bx:
            textX = textX - 8
        else:
            k1 = (Ax-Bx)/(Ay-By)
            k2 = -1/k1
            n2 = textY - k2*textX
            textY = textY - 5
            textX = (textY-n2)/k2

        weightObj = canvasName.create_text((textX, textY), text=str(weigth), fill=weigthTextColor)
        canvasName.tag_bind(weightObj, '<Double-1>', lambda event, arg=[canvasName,weightObj]: onWeightClick(event,arg))

    return canvasName.create_line(newx1, newy1, newx2, newy2, arrow=tk.LAST, fill=color, activefill=lineActiveColor)

# draws nodes and returns their positions
def drawGraph(canvas, graph):

    positions = {}
    heightFromTop = 60
    # gives positions of nodes
    for k,v in graph.items():
        # size of node
        size = 20
        if(k in [1,2]):
            currentX = canvasWidth/2
            currentY =  heightFromTop * (1.5*k-0.5)
        elif (k in [3,4]):
            currentY = heightFromTop * 4 - (k-3)*18
            currentX = float(canvasWidth)/7 * (7-k)
        elif(k in [5,6]):
            currentY = heightFromTop * 5.5
            currentX = float(canvasWidth)/7 * (k-2)
        elif(k in [7,8]):
            currentY = heightFromTop * 7
            currentX = float(canvasWidth)/7 * (k-4)
        elif(k in [9,10]):
            currentY = heightFromTop * 9
            currentX = float(canvasWidth)/7 * (k-6)
        elif(k == 11):
            currentY = heightFromTop * 10.5
            currentX = canvasWidth/2 
        elif(k in [12,13]):
            currentY = heightFromTop * 11
            currentX = float(canvasWidth)/7 * (k-9)
        elif(k in [14,15]):
            currentY = heightFromTop * 12.5
            currentX = float(canvasWidth)/7 * (k-11)
        elif(k in [16,17]):
            currentY = heightFromTop * 12 + 20*(k-16)
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

        # draws a node
        createNode(currentX, currentY, size, k, canvas)
        positions[k] = (currentX, currentY)
    
    return positions

# returns a branch between nodes
def drawLinks(canvas, positions, graph, color ,drawWeights=True):

    links = []
    for k,v in graph.items():
        try:
            # node from the begin of the branch (1(initial node) : [2 (end node),10 (weigth)])
            startDimesions = positions[k]
            for item in v:
                # branch enters into this node
                endDimensions = positions[item[0]]
                links.append(createLink(startDimesions, endDimensions,item[1], canvas, color, drawWeights))
        except:
            print("Not found")
    return links

# delete all branches
def deleteAllLinks(canvas, links):
    for line in links:
        canvas.delete(line)

class mainWindow:
    def __init__(self, root):
        self.root = root

        # this list contains names of all test files available
        # if you write new test file you need to include its name into this list
        # and then you will be able to choose that file to test
        testFilesAvailable = ["block_test.py", "if_test.py", "test_input.py", "for_test.py", "write example"]

        # error label (pressing on clear code button than on submit button -> syntax error ...)
        self.errorLabel = tk.Label(root, fg='red', justify=tk.CENTER)

        codeTextWidth = 625
        i=1
        for fileName in testFilesAvailable:
                if fileName == "write example":
                    # write your own example
                    btnFile = tk.Button(root, text=fileName, width=12, command=(lambda text=fileName: self.chooseFile("")))
                else:
                    btnFile = tk.Button(root, text = fileName, width=12,
                                 command = (lambda text=fileName: self.chooseFile(text)))

                btnFile.place(x=20+codeTextWidth , rely =(10+60*i)/windowWidth)
                i+=1

        # submit button, press to execute submitData()
        btn = tk.Button(root, text="Submit code", width=12, command=(lambda: self.submitData()))
        btn.place(x=20+codeTextWidth, rely=(280)/windowHeight)

        # Set clear button
        # clear button, press to execute clear()
        btn = tk.Button(root, text="Clear code", width=12, command=(lambda: self.clear()))
        btn.place(x=20+codeTextWidth, rely=(310)/windowHeight)

        # generate button, press to execute openNewWindow()
        btn = tk.Button(root, text="Generate canvas", width=12, command=(lambda: self.openNewWindow()))
        btn.place(x=20+codeTextWidth, rely=(340)/windowHeight)


    # delete text from code label and error label
    def clear(self):
        self.codeText.delete('1.0', tk.END)
        self.errorLabel.place_forget()


    def chooseFile(self, fileName):
        self.codeText = self.setCodeText(fileName)
        self.codeText.update()

    # read an example code from "fileName"
    def setCodeText(self, fileName):
        # setup the text input
        # hard-coded a number of window lines
        numOfLines = 80
        codeText = tk.Text(self.root, width=numOfLines)

        scroll = tk.Scrollbar(self.root, command=codeText.yview)
        codeText.configure(yscrollcommand=scroll.set)
        # proportion of a window for text
        codeText.place(height = 400-windowHeight/10, width = 600, relx=10/windowWidth, rely=10/windowHeight)
        # hard-coded example for submitting
        if fileName != "":
            test_file = open(Path(fileName), 'r')
            # at the end of the text window writes an example
            codeText.insert(tk.END, test_file.read())
        else:
            # if file isnt sent then you should write you own example
            codeText.insert(tk.END, "")
        return codeText

    # modifies a description and a title of the graph
    def changeGrapthTextTitle(self, text, title):
        self.graphTitle['text'] = title
        self.graphDescription.delete(1.0, tk.END)
        self.graphDescription.insert(1.0, text)

    # description and title initialization
    def drawGraphTextAndTitle(self, text, title):
        self.graphDescription = tk.Text(self.graphWindow, width=32, wrap=tk.WORD, bg=bgTextColor)
        self.graphTitle = tk.Label(self.graphWindow,font=titleStyle, text=title, bg=bgTextColor)
        self.graphDescription.place(x=canvasWidth+10, y=150)
        self.graphTitle.place(x=canvasWidth+ 10, y = 50)
        self.graphDescription.insert(tk.END, text)
        # self.graphDescription.configure(state='disabled')

    # draws a graph
    def drawControlFlowGraph(self):
        cfgDesc = "Od generisanih blokova u kodu konstruiše se Graf kontrole toka. Dodaju se START i EXIT čvorovi da bi dobijen graf bio povezan"
        # description and title
        self.drawGraphTextAndTitle(cfgDesc, "Graf kontrole toka")
        # draws links of the control flow graph (false means draw witout weights)
        self.lines = drawLinks(self.canvas, self.positions, self.graph, linesGraphColor , False)
        # button for generating spanning tree , pressing executes drawSpanningTree()
        self.nextBtn = tk.Button(self.graphWindow, text="Generiši razapinjujuće stablo", command=(lambda: self.drawSpanningTree()))
        self.nextBtn.place(x=canvasWidth+20, y=650)

    # draws spanning tree
    def drawSpanningTree(self):
        sptDesc = "Razapinjuće stablo grafa kontrole toka. Dobija se primenom DFS algoritma gde je kao početni čvor izabran EXIT."
        # description and title
        self.changeGrapthTextTitle(sptDesc, "Razapinjuće stablo")
        # delete all branches
        deleteAllLinks(self.canvas, self.lines)

        # draws links of spanning tree (false means don't add and draw weights)
        self.lines = drawLinks(self.canvas, self.positions, self.spanning_tree, linesTreeColor, False)
        # delete configuration for nextBtn and set new, pressing nextBtn executes self.drawInverseSpaningTreeNoWeights()
        self.nextBtn.place_forget()
        self.nextBtn = tk.Button(self.graphWindow, text="Generiši inverz stabla", command=(lambda: self.drawInverseSpaningTreeNoWeights()))
        self.nextBtn.place(x=canvasWidth+20, y=650)

    # draw inverse graph without weights
    def drawInverseSpaningTreeNoWeights(self):
        sptDesc = "Sve grane koje se nalaze u razapinjućem stablu se uklanjaju. Na osnovu preostalih grana i njihovih težina će se izračunati težine uklonjenih grana. Na mesto preostalih grana se u kodu postavljaju brojači."
        # description and title
        self.changeGrapthTextTitle(sptDesc, "Uklanjanje stabla")
        # delete drawn links
        deleteAllLinks(self.canvas, self.lines)
        # draw inverse graph without weights
        self.lines = drawLinks(self.canvas, self.positions, self.inv_spanning_tree, linesInvColor, False)
        # delete configuration for button and set new, pressing button executes drawInverseSpaningTree()

        self.nextBtn.place_forget()
        self.nextBtn = tk.Button(self.graphWindow, text="Dodaj težine", command=(lambda: self.drawInverseSpaningTree()))
        self.nextBtn.place(x=canvasWidth+20, y=650)

    # draws inverse graph with weights
    def drawInverseSpaningTree(self):
        sptDesc = "Izvršavanje koda sa brojačima. Vrednost brojača se postavlja kao težina grane i predstavlja broj puta koliko je ta grana izvršena u izvršavanja programa."
        # description and title
        self.changeGrapthTextTitle(sptDesc, "Dodavanje težina granama")
        # delete drawn links
        deleteAllLinks(self.canvas, self.lines)
        # draws links with weights
        self.lines = drawLinks(self.canvas, self.positions, self.inv_spanning_tree, linesInvColor, True)
        #delete configuration for button and set new,  pressing button executes drawList(0) - adds weights for the other links
        self.nextBtn.place_forget()
        self.nextBtn = tk.Button(self.graphWindow, text="Dodaj težine za ostale grane", command=(lambda: self.drawList(0)))
        self.nextBtn.place(x=canvasWidth+20, y=650)

    def drawList(self, i):
        sptDesc = "Poslednji korak u kome se dodeljuju težine svim granama u grafu u odnosu na težine grana koje ne pripadaju razapinjucem stablu."
        self.changeGrapthTextTitle(sptDesc, "Dodavanje težina ostalim \n granama")
        # the number of weights to add
        numOfSteps = len(self.list)
        if(i < numOfSteps):

            deleteAllLinks(self.canvas, self.lines)
            self.lines = drawLinks(self.canvas, self.positions, self.list[i], linesInvColor ,True)
            self.nextBtn.place_forget()
            self.nextBtn = tk.Button(self.graphWindow, text="Dodaj težinu za sledeću granu" , command=(lambda: self.drawList(i+1)))
            self.nextBtn.place(x=canvasWidth+20, y=650)
        else:
            self.nextBtn.place_forget()


    # opens window for visualisation
    def openNewWindow(self): 
        self.newWindow = tk.Toplevel(bg=bgTopLevelColor)
        self.newWindow.title("Vizuelizacija knutovog algoritma")
        self.newWindow.geometry("1280x700")
        self.graphWindow = self.newWindow

        # set parameters for drawing: dimensions,color,drawing window
        self.canvas = tk.Canvas(self.graphWindow, bg=bgCanvasColor, height=canvasHeight, width=canvasWidth)
        # forwarded graph, returs positions of a control flow graph
        self.positions = drawGraph(self.canvas, self.graph)
        
        # draw graph
        self.drawControlFlowGraph()
        self.canvas.pack(side=tk.LEFT)
  

    # received from activate method: code blocks, graph, spanning tree, inverse, list of weights
    def submitData(self):
        # encoding code from the file
        input = self.codeText.get("1.0",'end-1c')
        codeTextWidth = self.codeText.winfo_width()
        try:
            # returns code blocks, graph, spanning tree, inverse, list of weights
            blocks, graph, spanning_tree, inv_spanning_tree, calculate_weights_steps = activate(input)
        except Exception as e:
            self.errorLabel['text'] = "Syntax error: \n" + str(e)
            self.errorLabel.place(x=30+codeTextWidth, y=100/windowHeight)
            return

        # when the code is submitted, delete code from the window and add comments for every block(at the beginning and at the end)
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


# START
if __name__ == '__main__':
    # root - constructor of tkinter
    root = tk.Tk()
    # set dimensions of the window
    root.geometry(str(windowWidth) + 'x' + str(windowHeight))
    # app is instance of mainWindow class, we forwarded root in constructor
    app = mainWindow(root)
    # title
    app.root.title("Knutov algoritam")
    # execute root
    root.mainloop()

