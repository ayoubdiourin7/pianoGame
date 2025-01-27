#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  clavier.py
#  clavier version 1.0
#  Created by Ingenuity i/o on 2025/01/08
#
# "no description"
#
import base64
import json
import ingescape as igs
from pynput import keyboard  # Added import
import time  # Added import
import os
from pathlib import Path
from PIL import Image  # Added import


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class clavier(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.New_InputI = None
        
        # Start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.elements_ids = []
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the project root
        project_dir = os.path.dirname(current_dir)
        
        # Update paths to be relative to project directory
        self.notes_images = {
            "f": os.path.join(project_dir, "src/note", "f.jpg"),
            "re": os.path.join(project_dir, "note", "re.png"),
            "mi": os.path.join(project_dir, "note", "mi.png"),
            "fa": os.path.join(project_dir, "note", "fa.png"),
            "sol": os.path.join(project_dir, "note", "sol.png"),
            "la": os.path.join(project_dir, "note", "la.png"),
            "si": os.path.join(project_dir, "note", "si.png")
        }
        self.last_id = None
        # position of the note
        self.center = (350, 100)

    def displayImage(self, note, image_path=None):
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    image_data = img_file.read()
                    
                with Image.open(image_path) as img:
                    width, height = img.size
                    print(f"W: {width}, H: {height}")
                
                # Encode l'image en base64
                image_b64 = base64.b64encode(image_data).decode('utf-8')

                # Envoi de l'image à la whiteboard
                arg = (image_b64, self.center[0], self.center[1], width, height)
                igs.service_call("Whiteboard", "addImage", arg, None)
            else:
                print(f"Image not found: {image_path}")
        except Exception as e:
            print(f"Error displaying image: {str(e)}")
            print(f"Attempted to open: {image_path}")

    def Sendnotes(self, sender_agent_name, sender_agent_uuid, key_pressed=None):
        if key_pressed:
            # Delete previous text if it exists
            if self.last_id is not None:
                print(f"Deleting text with ID: {self.last_id}")
                igs.service_call("Whiteboard", "remove", (self.last_id,), None)
            
            if key_pressed.lower() in self.notes_images:
                image_path = self.notes_images[key_pressed.lower()]
                print(f"Attempting to display image: {image_path}")
                self.displayImage(key_pressed.lower(), image_path)
            
        print(f"Key pressed: {key_pressed}")
   
            
    def registerElement(self, element_id):

        print(f"Element ID: {element_id}")
        self.last_id = element_id
    
    def on_press(self, key):
        try:
            key_str = str(key.char) if hasattr(key, 'char') and key.char else str(key)
            self.Sendnotes("clavier", igs.agent_uuid(), key_str)
        except:
            import traceback
            print(traceback.format_exc())


