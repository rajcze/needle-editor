#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:46:48 2018

@author: Lukáš Růžička (lruzicka@redhat.com)
"""

import tkinter as tk
from PIL import Image
import os
import json
from tkinter import filedialog, messagebox

class Application:
    """ Holds the GUI part and widgets """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.grid()
        self.buildWidgets()
        self.images = []
        self.needleCoordinates = [0, 0, 100, 50]
        self.directory = ""
        self.rectangle = None
        self.needle = jsonRecord("empty")
        
    def buildWidgets(self):
        """Construct GUI"""
        self.buttonFrame = tk.Frame(self.frame)
        self.buttonFrame.grid(row=0, column=0, rowspan=2, sticky="news")

        self.openDirButton = tk.Button(self.buttonFrame, text="Select image directory", width=15, command=self.readimages)
        self.openDirButton.grid(row=0, column=0, sticky="nesw")

        self.quitButton = tk.Button(self.buttonFrame, text="Quit", fg="red", command=self.frame.quit)
        self.quitButton.grid(row=12, column=0, sticky="nesw")
        
        self.nextButton = tk.Button(self.buttonFrame, text="Next image (n)", command=lambda: self.nextImage(None))
        self.nextButton.grid(row=1,  column=0, sticky="nesw")
        
        self.prevButton = tk.Button(self.buttonFrame, text="Previous image (p)", command=lambda: self.prevImage(None))
        self.prevButton.grid(row=2,  column=0, sticky="nesw")
        
        self.createButton = tk.Button(self.buttonFrame, text="Show next area (s)", command=lambda: self.showArea(None))
        self.createButton.grid(row=3,  column=0, sticky="nesw")
        
        self.modifyButton = tk.Button(self.buttonFrame, text="Modify active area (m)", command=lambda: self.modifyArea(None))
        self.modifyButton.grid(row=4, column=0, sticky="nesw")
        
        self.hideButton = tk.Button(self.buttonFrame, text="Delete active area (d)", command=lambda: self.hideArea(None))
        self.hideButton.grid(row=5, column=0, sticky="news")
        
        self.addButton = tk.Button(self.buttonFrame, text="Add area to needle (a)", command=lambda: self.addAreaToNeedle(None))
        self.addButton.grid(row=6, column=0, sticky="news")
        
        self.deleteButton = tk.Button(self.buttonFrame, text="Remove area from needle (r)")
        self.deleteButton.grid(row=7, column=0, sticky="news")
        
        self.loadButton = tk.Button(self.buttonFrame, text="Load needle (l)", command=lambda: self.loadNeedle(None))
        self.loadButton.grid(row=8,  column=0, sticky="nesw")
        
        self.saveButton = tk.Button(self.buttonFrame, text="Create needle (c)")
        self.saveButton.grid(row=9,  column=0, sticky="nesw")
        
        self.picFrame = tk.Frame(self.frame)
        self.picFrame.grid(row=0, column=1)
                
        self.xscroll = tk.Scrollbar(self.picFrame, orient='horizontal')
        self.xscroll.grid(row=1, column=0, sticky="we")
        
        self.yscroll = tk.Scrollbar(self.picFrame, orient='vertical')
        self.yscroll.grid(row=0, column=1, columnspan=2, sticky="ns")

        self.pictureField = tk.Canvas(self.picFrame, height=800, width=1200, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.pictureField.grid(row=0, column=0)
        self.pictureField.config(scrollregion=self.pictureField.bbox('ALL'))
        self.pictureField.bind("<Button 1>", self.startArea)
        self.pictureField.bind("<B1-Motion>", self.redrawArea)
        self.pictureField.bind("<ButtonRelease-1>", self.endArea)
        self.pictureField.bind("m", self.modifyArea)
        self.pictureField.bind("s", self.showArea)
        self.pictureField.bind("n", self.nextImage)
        self.pictureField.bind("p", self.prevImage)
        self.pictureField.bind("d", self.hideArea)
       # self.pictureField.bind("c", self.saveNeedle)
        #self.pictureField.bind("m", lambda: self.modifyNeedle())
        
        self.xscroll.config(command=self.pictureField.xview)
        self.yscroll.config(command=self.pictureField.yview)
        
        self.jsonFrame = tk.Frame(self.frame)
        self.jsonFrame.grid(row=0, column=2, sticky="news")
        
        self.nameLabel = tk.Label(self.jsonFrame, text="Filename:")
        self.nameLabel.grid(row=0, column=0, sticky="w")
        
        self.nameEntry = tk.Entry(self.jsonFrame)
        self.nameEntry.grid(row=1, column=0, sticky="ew")
        
        self.propLabel = tk.Label(self.jsonFrame, text="Properties:")
        self.propLabel.grid(row=2, column=0, sticky="w")
        
        self.propText = tk.Text(self.jsonFrame, width=50, height=5)
        self.propText.grid(row=3, column=0, sticky="ew")
        
        self.needleUL = tk.Label(self.jsonFrame, text="Needle Upper Left Coordinates:")
        self.needleUL.grid(row=4, column=0, sticky="w")
        
        self.ulEntry = tk.Entry(self.jsonFrame)
        self.ulEntry.grid(row=5, column=0, sticky="ew")
        
        self.needleLR = tk.Label(self.jsonFrame, text="Needle Lower Right Coordinates:")
        self.needleLR.grid(row=6, column=0, sticky="w")
        
        self.lrEntry = tk.Entry(self.jsonFrame)
        self.lrEntry.grid(row=7, column=0, sticky="ew")
        
        self.listLabel = tk.Label(self.jsonFrame, text="Area type:")
        self.listLabel.grid(row=8, column=0, sticky="w")
        
        self.typeList = tk.Spinbox(self.jsonFrame, values=["match","ocr","someother"])
        self.typeList.grid(row=9, column=0, sticky="ew")
        
        self.textLabel = tk.Label(self.jsonFrame, text="Tags:")
        self.textLabel.grid(row=10, column=0, sticky="w")
        
        self.textField = tk.Text(self.jsonFrame, width=50, height=15)
        self.textField.grid(row=11, column=0, sticky="ew")
        
        self.jsonLabel = tk.Label(self.jsonFrame, text="Json Data:")
        self.jsonLabel.grid(row=12, column=0, sticky="w")
        
        self.textJson = tk.Text(self.jsonFrame, width=50, height=15)
        self.textJson.grid(row=13, column=0, sticky="ew")
        

    def returnPath(self, image):
        """Create a full path from working directory and image name."""
        return os.path.join(self.directory, image)
    
    def readimages(self):
        """Read png images from the given directory and return a list of their names."""
        self.images = []
        self.directory = filedialog.askdirectory()
        for file in os.listdir(self.directory):
            if file.endswith(".png"):
                self.images.append(file)
        print("Found {} images.".format(len(self.images)))
        self.imageCount = 0
        self.imageName = self.images[0]
        self.displayImage(self.returnPath(self.imageName))

    def displayImage(self, path):
        """Display image on the canvas."""
        print(path)
        self.picture = Image.open(path)
        #width = self.picture.width
        #height = self.picture.height
        self.picsize = (self.picture.width,self.picture.height)
        self.image = tk.PhotoImage(file=path)
        self.background = self.pictureField.create_image((1, 1), image=self.image, anchor='nw')
        self.nameEntry.delete(0, "end")
        self.nameEntry.insert("end", self.imageName)
               
    def nextImage(self, arg):
        """Display next image on the list."""
        self.imageCount += 1
        try:
            self.imageName = self.images[self.imageCount]
        except IndexError:
            self.imageName = self.images[0]
            self.imageCount = 0
        self.displayImage(self.returnPath(self.imageName))

    def prevImage(self, arg):
        """Display previous image on the list."""
        self.imageCount -= 1
        try:
            self.imageName = self.images[self.imageCount]
        except IndexError:
            self.imageName = self.images[-1]
            self.imageCount = len(self.images)
        self.displayImage(self.returnPath(self.imageName))
        
    
    def getCoordinates(self):
        """Read coordinates from the coordinate windows."""
        x = self.ulEntry.get().split(" ")
        y = self.lrEntry.get().split(" ")
        if not x:
            self.needleCoordinates = [0, 0, 100, 200]
        else:
            self.needleCoordinates = x + y
            
    def showArea(self, arg):
        """Load area and draw a rectangle around it."""
        #self.getCoordinates()
        self.area = self.needle.provideNextArea()
        self.needleCoordinates = [self.area[0], self.area[1], self.area[2], self.area[3]]
        typ = self.area[4]
        self.rectangle = self.pictureField.create_rectangle(self.needleCoordinates, outline="red")
        self.ulEntry.delete(0, "end")
        self.ulEntry.insert("end", "{} {}".format(self.needleCoordinates[0], self.needleCoordinates[1]))
        self.lrEntry.delete(0, "end")
        self.lrEntry.insert("end", "{} {}".format(self.needleCoordinates[2], self.needleCoordinates[3]))
        self.typeList.delete(0, "end")
        self.typeList.insert("end", typ)
        
        
    def modifyArea(self, arg):
        """Update the needle area."""
        self.getCoordinates()
        xpos = self.needleCoordinates[0]
        ypos = self.needleCoordinates[1]
        apos = self.needleCoordinates[2]
        bpos = self.needleCoordinates[3]
        typ = self.typeList.get()
        props = self.propText.get("1.0", "end")
        if "\n" in props:
            props = props.split("\n")
            if props[0] == "":
                props = []
                    
        tags = self.textField.get("1.0", "end")
        if "\n" in tags:
            tags = tags.split("\n")
            if tags[0] == "":
                tags = []
        coordinates = [xpos, ypos, apos, bpos, typ]
        self.needle.update(coordinates, tags, props)
        self.textJson.delete("1.0", "end")
        json = self.needle.provideJson()
        self.textJson.insert("end", json)
        
    def addAreaToNeedle(self, arg):
        """Add new area to needle."""
        self.needle.addArea()
        self.modifyArea(None)
        
    def startArea(self, event):
        xpos = event.x
        ypos = event.y
        self.startPoint = [xpos, ypos]
        if self.rectangle == None:
            self.rectangle = self.pictureField.create_rectangle(self.needleCoordinates, outline="red")
            
    def redrawArea(self, event):
        apos = event.x
        bpos = event.y
        self.endPoint = [apos, bpos]
        self.needleCoordinates = self.startPoint + self.endPoint
        self.pictureField.coords(self.rectangle, self.needleCoordinates)
        
    def endArea(self, event):
        xpos = self.needleCoordinates[0]
        ypos = self.needleCoordinates[1]
        apos = self.needleCoordinates[2]
        bpos = self.needleCoordinates[3]
        
        if xpos < apos and ypos < bpos:
            self.ulEntry.delete(0, "end")
            self.ulEntry.insert("end", "{} {}".format(xpos, ypos))
            self.lrEntry.delete(0, "end")
            self.lrEntry.insert("end", "{} {}".format(apos, bpos))
        elif xpos > apos and ypos > bpos:
            self.ulEntry.delete(0, "end")
            self.ulEntry.insert("end", "{} {}".format(apos, bpos))
            self.lrEntry.delete(0, "end")
            self.lrEntry.insert("end", "{} {}".format(xpos, ypos))
        elif xpos < apos and ypos > bpos:
            self.ulEntry.delete(0, "end")
            self.ulEntry.insert("end", "{} {}".format(xpos, bpos))
            self.lrEntry.delete(0, "end")
            self.lrEntry.insert("end", "{} {}".format(apos, ypos))
        elif xpos > apos and ypos < bpos:
            self.ulEntry.delete(0, "end")
            self.ulEntry.insert("end", "{} {}".format(apos, ypos))
            self.lrEntry.delete(0, "end")
            self.lrEntry.insert("end", "{} {}".format(xpos, bpos))
            
        
    def hideArea(self, arg):
        """Delete the needle area."""
        self.pictureField.delete(self.rectangle)
        self.rectangle = None
    
    def getSCoordinates(self,event):
        """Get upper left coordinates on left mouse click."""
        self.needleCoordinates[0] = (event.x,event.y)
        self.ulEntry.delete(0,"end")
        self.ulEntry.insert("end",self.needleCoordinates[0])
        self.pictureField.focus_set()
             
    def getECoordinates(self,event):
        """Get lower right coordinates on right mouse click."""
        self.needleCoordinates[1] = (event.x,event.y)
        self.lrEntry.delete(0,"end")
        self.lrEntry.insert("end",self.needleCoordinates[1])
        self.pictureField.focus_set()
        
    def loadNeedle(self, arg):
        """Load existing needle into the window."""
        image = self.returnPath(self.imageName).split("/")[-1]
        jSon = image.split(".")[0] + ".json"
        jSon = self.directory + "/" + jSon
        self.needle = jsonRecord(jSon)
        properties = self.needle.provideProperties()
        self.propText.delete("1.0", "end")
        self.propText.insert("end", properties)
        tags = self.needle.provideTags()
        self.textField.delete("1.0", "end")
        self.textField.insert("end", tags)
        json = self.needle.provideJson()
        self.textJson.delete("1.0", "end")
        self.textJson.insert("end", json)
        
#         area = data["area"][0]
#         coordinates = self.calculateCoordinates(int(area["xpos"]), int(area["ypos"]), int(area["width"]), int(area["height"]))
#         self.lrEntry.delete(0, "end")
#         self.lrEntry.insert("end", "{} {}".format(coordinates[2], coordinates[3]))
#         self.ulEntry.delete(0, "end")
#         self.ulEntry.insert("end", "{} {}".format(coordinates[0], coordinates[1]))
#         ntype = area["type"]
#         self.typeList.delete(0, "end")
#         self.typeList.insert("end", ntype)
        
        #data = needle.provideData()    
        #self.parseData(data)
        


#-----------------------------------------------------------------------------------------------
class jsonRecord:
    def __init__(self, jsonfile):
        self.areaPos = 0
        
        try:
            with open(jsonfile, "r") as inFile:
                self.jsonData = json.load(inFile)
    
        except FileNotFoundError:
            self.jsonData = {"properties":[],
                             "tags":[],
                             "area":[]}
            if jsonfile != "empty":
                messagebox.showerror("Error", "No needle exists. Create one.")
        self.areas = self.jsonData["area"]
                   
    def provideJson(self):
        return self.jsonData
            
    
    def provideAreaNumber(self):
        return len(self.jsonData["area"])
    
    def provideProperties(self):
        properties = "\n".join(self.jsonData["properties"])
        return properties
    
    def provideTags(self):
        tags = "\n".join(self.jsonData["tags"])
        return tags
    
    def provideNextArea(self):
        try:
            area = self.areas[self.areaPos]
        except IndexError:
            messagebox.showerror("Error", "No more area in the needle.")
        xpos = area["xpos"]
        ypos = area["ypos"]
        wide = area["width"]
        high = area["height"]
        typ = area["type"]
        apos = xpos + wide
        bpos = ypos + high
        areaData = [xpos, ypos, apos, bpos, typ]
        self.areaPos += 1
        return areaData
    
    def update(self, coordinates, tags, props):
        xpos = coordinates[0]
        ypos = coordinates[1]
        apos = coordinates[2]
        bpos = coordinates[3]
        typ = coordinates[4]
        wide = int(apos) - int(xpos)
        high = int(bpos) - int(ypos)
        area = {"xpos":xpos, "ypos":ypos, "width":wide, "height":high, "type":typ}
        self.jsonData["properties"] = props
        self.jsonData["tags"] = tags
        
        try:
            self.areas[self.areaPos-1] = area
        except IndexError:
            messagebox.showerror("Error", "Cannot modify non-existent area. Add area first!")
        self.jsonData["area"] = self.areas
            
    def addArea(self):
        self.areas.append("newarea")
        self.areaPos = len(self.areas)
        
        
        

#-----------------------------------------------------------------------------------------------

root = tk.Tk()
root.title("Python Needle Editor for OpenQA (Draft Version)")

app = Application(root)

root.mainloop()
root.destroy() # optional; see description below

