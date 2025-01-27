#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  clavier.py
#  clavier version 1.0
#  Created by Ingenuity i/o on 2025/01/08
#
# "no description"
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Clavier(metaclass=Singleton):
    def __init__(self):
        # inputs

        pass


    # services
    def sendNotes(self, sender_agent_name, sender_agent_uuid):
        """
        Service pour envoyer le texte au Whiteboard
        Args:
            sender_agent_name (str): Nom de l'agent appelant
            sender_agent_uuid (str): UUID de l'agent appelant
        """
        try:
            # Envoi du message au Whiteboard
            igs.service_call("whiteboard", "addText",{"test",1,1,"black"}, "")

        except Exception as e:
            igs.error(f"Erreur lors de l'envoi du message: {str(e)}")

