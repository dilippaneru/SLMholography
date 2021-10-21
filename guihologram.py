#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:24:02 2021

@author: dilip
"""
import PySimpleGUI as sg
import os.path
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib import pyplot
import numpy as np
import cv2
from PIL import ImageGrab


# Window layout in 2 columns

Gx = 1.0 
Gy = 1.0
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    
    
    [
            sg.Radio("Gx", "Radio", size=(10, 1), key="-THRESH1-"),
            sg.Slider(
                (0, 255),
                1,
                0.5,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER1-",
            ),
        ],
    
    
    [
            sg.Radio("Gy", "Radio", size=(10, 1), key="-THRESH2-"),
            sg.Slider(
                (0, 255),
                1,
                0.5,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER2-",
            ),
        ],
    
    [
            sg.Radio("xoffset", "Radio", size=(10, 1), key="-offsetx-"),
            sg.Slider(
                (-200,200 ),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-offset sliderx-",
            ),
        ],
        
    [
            sg.Radio("yoffset", "Radio", size=(10, 1), key="-offsety-"),
            sg.Slider(
                (-200, 200),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-offset slidery-",
            ),
        ],

    
    [
            sg.Radio("Rescale", "Radio", size=(10, 1), key="-scale-"),
            sg.Slider(
                (10, 510),
                400,
                50,
                orientation="h",
                size=(40, 15),
                key="-scale slider-",
            ),
        ],
    
        
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    
    [
            sg.Radio("Pixel Threshold1", "Radio", size=(20, 1), key="-pixel threshold1-"),
            sg.Slider(
                (0, 255),
                127,
                0.5,
                orientation="h",
                size=(40, 15),
                key="-pixel threshold slider1-",
            ),
        ],
    
     [
            sg.Radio("Pixel Threshold2", "Radio", size=(20, 1), key="-pixel threshold2-"),
            sg.Slider(
                (0, 255),
                127,
                0.5,
                orientation="h",
                size=(40, 15),
                key="-pixel threshold slider2-",
            ),
        ],
     
    
    [
     sg.Button("Run",key="-Execute-")
     ],
    
    [
     sg.T('Source Folder'),
     sg.In(key='input'),
     sg.FolderBrowse(target='input'), sg.OK(),
     ],
    
    [
     sg.Button("Save Image", key="-save-")
     ],
]

# Only show the name of the file that was chosen

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
    ]
]

def hologramupdate(filename,Gx,Gy,xoffset,yoffset,imagesize):
     img = cv2.imread(filename,0)

     newimage = np.zeros((1000,1000))
     
     x = int(imagesize/2)
     a = int(xoffset)
     b = int(yoffset)
     
     res = cv2.resize(img, (2*x, 2*x), interpolation = cv2.INTER_AREA)
     print(np.shape(res))
     # just to create an additional rectangular window

     newimage[(500-x):(500+x),(500-x):(500+x)] = res
     final = np.zeros((newimage.shape[0], newimage.shape[1])) + 255.0
     
     xoffset = a
     yoffset = b
     Gx = Gx*np.pi/180.0
     Gy = Gy*np.pi/180.0
 
     M = np.float32([[1,0,a],[0,1,b]])
     translated = cv2.warpAffine(newimage,M,(newimage.shape[0],newimage.shape[1]))
 
 
     for j in range(translated.shape[0]):
         for k in range(translated.shape[1]):
             
             if translated[j,k] > values["-pixel threshold slider1-"]: 
                 final[j,k] = (255.0 + (np.mod(2*np.pi*(Gx*(j) + Gy*(k)),2*np.pi))*255.0/(2*np.pi))
                  
             elif (translated[j,k] > values["-pixel threshold slider1-"]) and (translated[j,k] < values["-pixel threshold slider2-"]):  
                 final[j,k] =  (255.0 + (np.mod(2*np.pi*(Gx*(j) + Gy*(k)),2*np.pi))*255.0/(2*np.pi))
                 
             else:
                 final[j,k] =  0.0
                
     final = 255.0*final/(np.amax(final)) 
     return(final)



layout1 = [[sg.Text('HOLOGRAM' )],
           [sg.Image(key="-IMAGE-")]
           ]
  

window1, window2  = sg.Window("Hologram Viewer", layout), sg.Window('Second Window', layout1, finalize=True, location = (1280,0),size = (800,600)).Finalize()
window2.maximize()
# Run the Event Loop
while True:
    event, values = window1.read()
    frame = np.zeros((1000,1000))
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
        
        
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window1["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            print(values["-FOLDER-"])
        except:
            pass

    elif event == "-THRESH1-":  # Slider for Gx 
          try:
            print(1)
          except:
              pass 
         
    elif event == "-THRESH2-":  # Slider for Gx 
          try:
              print(1)
          except:
              pass   
   
             
    elif event == "-Execute-":
         print("execute")
         frame = hologramupdate(filename,values["-THRESH SLIDER1-"],values["-THRESH SLIDER2-"],values["-offset sliderx-"],values["-offset slidery-"],values["-scale slider-"])
         imgbytes = cv2.imencode(".png",frame)[1].tobytes()
         window2["-IMAGE-"].update(data=imgbytes)      
         
    elif event == "-save-":
        frame = hologramupdate(filename,values["-THRESH SLIDER1-"],values["-THRESH SLIDER2-"],values["-offset sliderx-"],values["-offset slidery-"],values["-scale slider-"])
        filename = os.path.join(values["-FOLDER-"] , 'hologram.png')
        pyplot.imsave(filename, frame)

        #cv2.imwrite("/Users/dilip/Desktop/GhostImagesNew/hologram.png", frame)
        #cv2.waitKey(0)
         

window2.close()
window1.close()
