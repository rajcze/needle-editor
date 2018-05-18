#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 08:46:48 2018

@author: Lukáš Růžička (lruzicka@redhat.com)
"""

import tkinter as tk
import os
from tkinter import filedialog



class Application:
    """ Holds the GUI part and widgets """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.grid()
        self.buildWidgets()
        self.images = []

    def buildWidgets(self):
        self.buttonFrame = tk.Frame(self.frame)
        self.buttonFrame.grid(row=0, column=0, rowspan=2, sticky="news")
        
        self.openDirButton = tk.Button(self.buttonFrame, text="Select image directory", width=15,  command=self.readimages)
        self.openDirButton.grid(row=0, column=0, sticky="nesw")

        self.quitButton = tk.Button(self.buttonFrame, text="Quit", fg="red", command=self.frame.quit)
        self.quitButton.grid(row=10, column=0, sticky="nesw")
        
        self.nextButton = tk.Button(self.buttonFrame, text="Next image", command=self.nextImage)
        self.nextButton.grid(row=1,  column=0, sticky="nesw")
        
        self.prevButton = tk.Button(self.buttonFrame, text="Previous image", command=self.prevImage)
        self.prevButton.grid(row=2,  column=0, sticky="nesw")
        
        self.createButton = tk.Button(self.buttonFrame, text="Create needle")
        self.createButton.grid(row=3,  column=0, sticky="nesw")
        
        self.loadButton = tk.Button(self.buttonFrame, text="Load needle")
        self.loadButton.grid(row=4,  column=0, sticky="nesw")
        
        self.saveButton = tk.Button(self.buttonFrame, text="Save needle")
        self.saveButton.grid(row=5,  column=0, sticky="nesw")
        
        self.picFrame = tk.Frame(self.frame)
        self.picFrame.grid(row=0, column=1)
        
        self.xscroll = tk.Scrollbar(self.picFrame, orient='horizontal')
        self.xscroll.grid(row=1, column=0, sticky="we")
        
        self.yscroll = tk.Scrollbar(self.picFrame, orient='vertical')
        self.yscroll.grid(row=0, column=1, columnspan=2, sticky="ns")

        self.pictureField = tk.Canvas(self.picFrame, height=800, width=1200, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.pictureField.grid(row=0, column=0)
        self.pictureField.config(scrollregion=self.pictureField.bbox('ALL'))
        
        self.xscroll.config(command=self.pictureField.xview)
        self.yscroll.config(command=self.pictureField.yview)
        
        self.jsonFrame = tk.Frame(self.frame)
        self.jsonFrame.grid(row=0, column=2, sticky="news")
        
        self.jsonLabel = tk.Label(self.jsonFrame, text="Needle JSON data:")
        self.jsonLabel.grid(row=0, column=0)
        self.jsonText = tk.Text(self.jsonFrame, width=30)
        self.jsonText.grid(row=1, column=0)
        

    def returnPath(self, image):
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
        self.displayImage(self.returnPath(self.images[0]))

    def displayImage(self, path):
        """Display image on the canvas."""
        print(path)
        self.image = tk.PhotoImage(file=path)
        self.pictureField.create_image((1, 1), image=self.image, anchor='nw')
        
    def nextImage(self):
        """Display next image on the list."""
        self.imageCount += 1
        try:
            self.image = self.images[self.imageCount]
        except IndexError:
            self.image = self.images[0]
            self.imageCount = 0
        self.displayImage(self.returnPath(self.image))

    def prevImage(self):
        """Display previous image on the list."""
        self.imageCount -= 1
        try:
            self.image = self.images[self.imageCount]
        except IndexError:
            self.image = self.images[-1]
            self.imageCount = len(self.images)
        self.displayImage(self.returnPath(self.image))
            
        

#-----------------------------------------------------------------------------------------------

root = tk.Tk()
root.title("Python Needle Editor for OpenQA (Draft Version)")

app = Application(root)

root.mainloop()
root.destroy() # optional; see description below

