
from .pet import AnkiPet
from .pet_widget import PetWidget
from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
from datetime import datetime
from PyQt6.QtWidgets import QDockWidget
from PyQt6.QtCore import Qt
import os

pet = None
pet_widget = None


def init_pet() -> None:
    """Initialize the pet after a profile has been opened."""
    global pet
    pet = AnkiPet()

def on_card_review(reviewer, card, ease):
    if pet is None:
        return
    today = datetime.now().date()
    if ease > 1:
        pet.feed()
        pet.play()
        if pet_widget:
            pet_widget.load_animation("attack", temporary=True)
    else:
        pet.neglect()
    pet.check_streak(today)
    if pet_widget:
        pet_widget.update_status()

def show_pet():
    global pet_widget
    if pet is None:
        return
    today = datetime.now().date()
    pet.check_streak(today)
    pet_widget = PetWidget(pet, os.path.dirname(__file__))
    dock = QDockWidget("AnkiPet", parent=mw)
    dock.setWidget(pet_widget)
    mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
 
gui_hooks.profile_did_open.append(init_pet)
gui_hooks.main_window_did_init.append(show_pet)
gui_hooks.reviewer_did_answer_card.append(on_card_review)
