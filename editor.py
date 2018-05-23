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
        
    def buildWidgets(self):
        """Construct GUI"""
        self.buttonFrame = tk.Frame(self.frame)
        self.buttonFrame.grid(row=0, column=0, rowspan=2, sticky="news")

        self.openDirButton = tk.Button(self.buttonFrame, text="Select image directory", width=15, command=self.readimages)
        self.openDirButton.grid(row=0, column=0, sticky="nesw")

        self.quitButton = tk.Button(self.buttonFrame, text="Quit", fg="red", command=self.frame.quit)
        self.quitButton.grid(row=10, column=0, sticky="nesw")
        
        self.nextButton = tk.Button(self.buttonFrame, text="Next image", command=self.nextImage)
        self.nextButton.grid(row=1,  column=0, sticky="nesw")
        
        self.prevButton = tk.Button(self.buttonFrame, text="Previous image", command=self.prevImage)
        self.prevButton.grid(row=2,  column=0, sticky="nesw")
        
        self.createButton = tk.Button(self.buttonFrame, text="Show needle", command=self.showNeedle)
        self.createButton.grid(row=3,  column=0, sticky="nesw")
        
        self.modifyButton = tk.Button(self.buttonFrame, text="Modify needle (m)", command=lambda: self.modifyNeedle(None))
        self.modifyButton.grid(row=4, column=0, sticky="nesw")
        
        self.hideButton = tk.Button(self.buttonFrame, text="Hide needle", command=self.hideNeedle)
        self.hideButton.grid(row=5, column=0, sticky="news")
        
        self.loadButton = tk.Button(self.buttonFrame, text="Load needle", command=self.loadNeedle)
        self.loadButton.grid(row=6,  column=0, sticky="nesw")
        
        self.saveButton = tk.Button(self.buttonFrame, text="Save needle")
        self.saveButton.grid(row=7,  column=0, sticky="nesw")
        
        self.picFrame = tk.Frame(self.frame)
        self.picFrame.grid(row=0, column=1)
                
        self.xscroll = tk.Scrollbar(self.picFrame, orient='horizontal')
        self.xscroll.grid(row=1, column=0, sticky="we")
        
        self.yscroll = tk.Scrollbar(self.picFrame, orient='vertical')
        self.yscroll.grid(row=0, column=1, columnspan=2, sticky="ns")

        self.pictureField = tk.Canvas(self.picFrame, height=800, width=1200, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.pictureField.grid(row=0, column=0)
        self.pictureField.config(scrollregion=self.pictureField.bbox('ALL'))
        self.pictureField.bind("<Button 1>", self.getSCoordinates)
        self.pictureField.bind("<Button 3>", self.getECoordinates)
        self.pictureField.bind("m", self.modifyNeedle)
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
        
        self.propText = tk.Text(self.jsonFrame, width=50, height=10)
        self.propText.grid(row=3, column=0, sticky="ew")
        
        self.needleUL = tk.Label(self.jsonFrame, text="Needle Upper Left Coordinates:")
        self.needleUL.grid(row=4, column=0, sticky="w")
        
        self.ulEntry = tk.Entry(self.jsonFrame)
        self.ulEntry.grid(row=5, column=0, sticky="ew")
        
        self.needleLR = tk.Label(self.jsonFrame, text="Needle Lower Right Coordinates:")
        self.needleLR.grid(row=6, column=0, sticky="w")
        
        self.lrEntry = tk.Entry(self.jsonFrame)
        self.lrEntry.grid(row=7, column=0, sticky="ew")
        
        self.listLabel = tk.Label(self.jsonFrame, text="Needle type:")
        self.listLabel.grid(row=8, column=0, sticky="w")
        
        self.typeList = tk.Spinbox(self.jsonFrame, values=["match","ocr","someother"])
        self.typeList.grid(row=9,column=0, sticky="ew")
        
        self.textLabel = tk.Label(self.jsonFrame, text="Tags:")
        self.textLabel.grid(row=10, column=0, sticky="w")
        
        self.textField = tk.Text(self.jsonFrame, width=50, height=15)
        self.textField.grid(row=11,column=0, sticky="ew")
        

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
        width = self.picture.width
        height = self.picture.height
        self.picsize = (self.picture.width,self.picture.height)
        self.image = tk.PhotoImage(file=path)
        self.background = self.pictureField.create_image((1, 1), image=self.image, anchor='nw')
        self.nameEntry.delete(0, "end")
        self.nameEntry.insert("end", self.imageName)
               
    def nextImage(self):
        """Display next image on the list."""
        self.imageCount += 1
        try:
            self.imageName = self.images[self.imageCount]
        except IndexError:
            self.imageName = self.images[0]
            self.imageCount = 0
        self.displayImage(self.returnPath(self.imageName))

    def prevImage(self):
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
            
    def showNeedle(self):
        """Draw a rectangle around the needle area."""
        self.getCoordinates()
        self.rectangle = self.pictureField.create_rectangle(self.needleCoordinates, outline="red")
        
    def modifyNeedle(self, arg):
        """Update the needle area."""
        self.getCoordinates()
        self.pictureField.coords(self.rectangle, self.needleCoordinates)
        
    def hideNeedle(self):
        """Delete the needle area."""
        self.pictureField.delete(self.rectangle)
    
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
        
    def loadNeedle(self):
        """Load existing needle into the window."""
        image = self.returnPath(self.imageName).split("/")[-1]
        jSon = image.split(".")[0] + ".json"
        jSon = self.directory + "/" + jSon
        try:
            with open(jSon,"r") as jsonFile:
                data = json.load(jsonFile)
        except FileNotFoundError:
            messagebox.showerror("Error", "No needle exists. Create one.")
            
        self.parseData(data)
        
    def parseData(self, data):
        """Read the json file and fill-in the fields."""
        properties = data["properties"]
        self.textField.delete("1.0", "end")
        for tag in data["tags"]:
            self.textField.insert("end", tag)
            self.textField.insert("end", "\n")
        area = data["area"][0]
        coordinates = self.calculateCoordinates(int(area["xpos"]), int(area["ypos"]), int(area["width"]), int(area["height"]))
        self.lrEntry.delete(0, "end")
        self.lrEntry.insert("end", "{} {}".format(coordinates[2], coordinates[3]))
        self.ulEntry.delete(0, "end")
        self.ulEntry.insert("end", "{} {}".format(coordinates[0], coordinates[1]))
        ntype = area["type"]
        self.typeList.delete(0, "end")
        self.typeList.insert("end", ntype)
        
        
    def calculateCoordinates(self, xpos, ypos, wide, high):
        """Calculate coordinates from position, width and height of needle."""
        apos = xpos + wide
        bpos = ypos + high
        coordinates = [xpos, ypos, apos, bpos]
        return coordinates
              

#-----------------------------------------------------------------------------------------------

root = tk.Tk()
root.title("Python Needle Editor for OpenQA (Draft Version)")

app = Application(root)

root.mainloop()
root.destroy() # optional; see description below

