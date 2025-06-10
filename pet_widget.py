from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import QTimer, Qt
import os
import random

class PetWidget(QWidget):
    def __init__(self, pet, base_dir):
        super().__init__()
        self.pet = pet
        self.base_dir = base_dir
        self.frame_index = 0
        self.animation_timer = QTimer(self)
        self.setFixedSize(300, 200)

        self.image = QLabel(self)
        self.image.setGeometry(100, 60, 100, 100)

        self.status = QLabel(self)
        self.status.setGeometry(10, 160, 280, 30)
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.animations = {
            "idle": {"file": "Idle.png", "frames": 4},
            "walk": {"file": "Walk.png", "frames": 6},
            "attack": {"file": "Attack.png", "frames": 4},
        }

        self.current_animation = "idle"
        self.sprite_sheet = None
        self.load_animation(self.current_animation)
        self.update_status()

        self.position_x = 100
        self.moving_right = True
        self.facing_right = True

        self.animation_timer.timeout.connect(self.update_frame)
        self.animation_timer.start(200)

        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self.random_idle_swap)
        self.idle_timer.start(8000)

    def load_animation(self, name, temporary=False):
        anim = self.animations.get(name)
        if not anim:
            return

        self.current_animation = name
        self.frame_index = 0
        self.sprite_sheet = None

        sheet_path = os.path.join(self.base_dir, "images", anim["file"])
        if os.path.exists(sheet_path):
            self.sprite_sheet = QPixmap(sheet_path)

        if temporary:
            frame_time = 200
            total_duration = frame_time * anim["frames"]
            QTimer.singleShot(total_duration, self.resume_idle_behavior)

    def update_frame(self):
        anim = self.animations[self.current_animation]
        frames = anim["frames"]
        if not self.sprite_sheet or self.sprite_sheet.isNull():
            return

        frame_width = self.sprite_sheet.width() // frames
        frame_height = self.sprite_sheet.height()
        x = self.frame_index * frame_width
        cropped = self.sprite_sheet.copy(x, 0, frame_width, frame_height)

        # Flip if facing left
        if not self.facing_right:
            transform = QTransform().scale(-1, 1)
            cropped = cropped.transformed(transform)

        self.image.setPixmap(
            cropped.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        )
        self.image.repaint()
        self.frame_index = (self.frame_index + 1) % frames

        # Only move when walking
        if self.current_animation == "walk":
            if self.moving_right:
                self.position_x += 4
                if self.position_x > 200:
                    self.moving_right = False
            else:
                self.position_x -= 4
                if self.position_x < 0:
                    self.moving_right = True
            self.facing_right = self.moving_right
            self.image.move(self.position_x, 60)

    def update_status(self):
        self.status.setText(
            f"Happiness: {self.pet.happiness}\n"
            f"Hunger: {self.pet.hunger}\n"
            f"Health: {self.pet.health}\n"
            f"Streak: {self.pet.streak}"
        )

    def resume_idle_behavior(self):
        next_anim = random.choice(["idle", "walk"])
        self.load_animation(next_anim)

    def random_idle_swap(self):
        if self.current_animation not in ["idle", "walk"]:
            return
        self.resume_idle_behavior()
