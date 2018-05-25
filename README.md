# Python Needle Editor for creating OpenQA needles (Version 0.99)

The Needle Editor creates and modifies needles for the OpenQA tests. The advantage of the editor is
that it does not need OpenQA to be installed on the system. Only screenshots upon which the needles 
will be created are needed. With the editor, the needles can be made in advance and then only tested finally in the OpenQA 
instance. 

The editor only supports **png** screenshots. 

## Requirements

* Python 3
* Tkinter
* the Pillow library

## Using the editor

### Reading the images

1. Click the **Select image directory**.
2. Use the dialogue to select a directory where the screenshots are located.

**Note:** The editor reports number of images in the directory, when you have selected it.

### Navigating through images

You can navigate through the images back and forth in the loop. To navigate through the image loop:

1. Click the **Next picture** or the **Previous picture** buttons.
2. Use the **n** and **p** keys. 


### Working with needles

#### Loading the needle information

When you have navigated to the image you want to create a needle for, make sure you try loading an
existing needle. Not doing so, you could accidentally overwrite it. To load a needle:

1. Click the **Load needle** button or press the **l** key. The editor informs you, if there is no 
needle saved for the image.

**Note**: You can load the needle anytime and restore all the original information until the needle 
has been saved.

#### Reading the needle information.

When the needle is loaded, you can see all needle information in the right part of the program window.
Among others:

* the name of the active image
* needle properties
* needle tags
* active area coordinates
* number of areas in the needle
* the content of the needle json file

#### Updating the needle information
You can manually update the following fields:

* the coordinates
* the properties
* the tags
* the area type

The coordinates can also be update using the mouse, drawing a rectangle to set up the new area for 
needle. 

**Note**: When you manually update the informations, you have to click **Modify active area** button 
for them to take effect. The keyboard shortcuts do not work properly in this situation because of 
lost focus (known issue). To workaround this issue, update all information manually and use the mouse for updating the
coordinates. Then you will be able to use the keyboard shortcuts again.

#### Saving a needle

If you want to store the needle information permanently, you have to save it. To do so:

1. Click on the **Create needle** button to save the needle.

When saving, the editor creates a json file (the name of the file matches the name of the active 
image) and stores all needle information in that file. Next time, when you load the needle, all 
settings will be restored.

**Note**: The json file is a necessary part of the screenshot for the OpenQA.
 Without that, it cannot handle the needles and the tests will fail.

#### Creating a new needle from scratch

To create a new needle, you must provide the required needle information:

* needle tags
* needle area
* needle type (match, ocr, or exclude)
* needle properties (not compulsory)

1. Fill in the necessary information for the properties, type and tags.
2. Draw a rectangle around the area you want to add or update the coordinates manually.
3. Click **Add area to needle** button or press the **a** key to add the area to the needle. See 
*Updating the needle information* to learn about a known issue.
4. If you wish to add another area (the needle can have more areas), just draw a new area and use 
**Step 3** to add it to the needle.
5. If you change the properties, type or tags, the the whole needle will be affected by the change.
6. Click the **Create needle** button to save the needle permanently into a json file.

### Working with areas

#### Add an area to the needle

In order to have an area on the needle, you have to add it to it:

1. Press the **Add area to needle** button to add the area to the needle. 
2. Repeat for another area.

You can see the number of areas in the field in the lower right part of the window.

#### Removing an active area

When your area is still active (that means that you have not added a new area yet), it can be removed
from the needle again:

1. Click on the **Remove from needle** button to remove it from the needle. 

When removing the area from the needle, the active area falls back to the previous area 
(which becomes active) and the rectangle will show its current position. You can repeat the action,
until all areas are deleted.

#### Showing next area

When the needle has more than one area (you can see the number in the lower right part of the
program window), only the first area is shown. To see the next area:

1. Click on the **Show next area** button. 

This will show the next area in the needle and makes it active. You can update the area or remove it.

**Warning**: In this version, you cannot navigate in areas. You only can move to the next ones.
However, if you remove the area from the needle, the editor will fall back to the previous area and 
make it active again so you can update or remove it.




