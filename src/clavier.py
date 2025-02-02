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
from playsound import playsound  # Replace musicalbeeps import


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
        print("clavier init")


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
            "q": os.path.join(project_dir, "src/note", "do.png"),
            "s": os.path.join(project_dir, "src/note", "re.png"),
            "d": os.path.join(project_dir, "src/note", "mi.png"),
            "f": os.path.join(project_dir, "src/note", "fa.png"),
            "g": os.path.join(project_dir, "src/note", "sol.png"),
            "h": os.path.join(project_dir, "src/note", "la.png"),
            "j": os.path.join(project_dir, "src/note", "si.png"),
            "k": os.path.join(project_dir, "src/note", "do2.png"),
            "l": os.path.join(project_dir, "src/note", "re2.png"),
            "m": os.path.join(project_dir, "src/note", "mi2.png"),
        }
        self.last_id = None
        # position of the note
        self.center = (566, 400)
        
        # Remove the player initialization
        # self.player = musicalbeeps.Player(volume=0.3, mute_output=False)
        
        # Replace notes_mapping with sound files mapping
        self.notes_sounds = {
            "q": os.path.join(project_dir, "src/sounds", "C.wav"),
            "s": os.path.join(project_dir, "src/sounds", "D.wav"),
            "d": os.path.join(project_dir, "src/sounds", "E.wav"),
            "f": os.path.join(project_dir, "src/sounds", "F.wav"),
            "g": os.path.join(project_dir, "src/sounds", "G.wav"),
            "h": os.path.join(project_dir, "src/sounds", "A.wav"),
            "j": os.path.join(project_dir, "src/sounds", "B.wav"),
            "k": os.path.join(project_dir, "src/sounds", "C1.wav"),
            "l": os.path.join(project_dir, "src/sounds", "D1.wav"),
            "m": os.path.join(project_dir, "src/sounds", "E1.wav"),
        }


    def displayImage(self, note, image_path=None):
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    image_data = img_file.read()
                    
                with Image.open(image_path) as img:
                    # Resize the image to the desired dimensions (e.g., 100x100)
                    new_size = (300, 300)  # Change this to your desired size
                    resized_img = img.resize(new_size)
                    width, height = resized_img.size
                    print(f"W: {width}, H: {height}")
                    
                    # Save the resized image to a temporary file
                    temp_image_path = os.path.join(os.path.dirname(image_path), "temp_resized_image.png")
                    resized_img.save(temp_image_path)
                    
                    # Read the resized image data
                    with open(temp_image_path, 'rb') as resized_img_file:
                        resized_image_data = resized_img_file.read()
                    
                    # Encode the resized image in base64
                    image_b64 = base64.b64encode(resized_image_data).decode('utf-8')

                    # Send the resized image to the whiteboard
                    arg = (image_b64, self.center[0], self.center[1], width, height)
                    igs.service_call("Whiteboard", "addImage", arg, None)
                    
                    # Optionally, delete the temporary resized image file
                    os.remove(temp_image_path)
            else:
                print(f"Image not found: {image_path}")
        except Exception as e:
            print(f"Error displaying image: {str(e)}")
            print(f"Attempted to open: {image_path}")

    def play_sound(self, key):
        try:
            if key.lower() in self.notes_sounds:
                sound_path = self.notes_sounds[key.lower()]
                if os.path.exists(sound_path):
                    playsound(sound_path, block=False)  # Non-blocking sound playback
                else:
                    print(f"Sound file not found: {sound_path}")
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

    def Sendnotes(self, sender_agent_name, sender_agent_uuid, key_pressed=None):
        # print a rectangle line on the whiteboard
        print("Sendnotes")
        
        if key_pressed:
            igs.service_call("Whiteboard", "addShap", ("ellipse", 350, 350, 1400, 1, "green", "black", 3), None)
            # Delete previous text if it exists
            if self.last_id is not None:
                print(f"Deleting text with ID: {self.last_id}")
                igs.service_call("Whiteboard", "remove", (self.last_id,), None)
            
            if key_pressed.lower() in self.notes_images:
                image_path = self.notes_images[key_pressed.lower()]
                print(f"Attempting to display image: {image_path}")
                self.displayImage(key_pressed.lower(), image_path)
                # Play sound instead of musical note
                self.play_sound(key_pressed)
            
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

