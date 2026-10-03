import cv2
import os
import time


class Dashboard:

    def __init__(self, title="AI Gesture Wallpaper"):

        self.title = title

        self.current_gesture = "NO_HAND"
        self.stability = 0
        self.active = False

        self.category = "None"
        self.wallpaper = "None"

        self.actions = []

        self.start_time = time.time()

    # ---------------------------------------------------------
    # UPDATE CURRENT STATUS
    # ---------------------------------------------------------

    def update_status(
        self,
        gesture="NO_HAND",
        stability=0,
        active=False,
        category="None",
        wallpaper="None"
    ):

        self.current_gesture = gesture
        self.stability = max(0, min(100, stability))
        self.active = active
        self.category = category
        self.wallpaper = wallpaper

    # ---------------------------------------------------------
    # ADD ACTION TO HISTORY
    # ---------------------------------------------------------

    def add_action(self, action, description=None):

        timestamp = time.strftime("%H:%M:%S")

        if description is not None:
            action_text = f"{action} - {description}"
        else:
            action_text = str(action)

        self.actions.insert(
            0,
            f"{timestamp}  {action_text}"
        )

        # Keep only latest 6 actions
        self.actions = self.actions[:6]

    # ---------------------------------------------------------
    # DRAW TEXT
    # ---------------------------------------------------------

    def draw_text(
        self,
        frame,
        text,
        position,
        scale=0.6,
        thickness=1
    ):

        cv2.putText(
            frame,
            str(text),
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            (235, 235, 235),
            thickness,
            cv2.LINE_AA
        )

    # ---------------------------------------------------------
    # DRAW RECTANGLE
    # ---------------------------------------------------------

    def draw_box(
        self,
        frame,
        x1,
        y1,
        x2,
        y2,
        thickness=1
    ):

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (80, 80, 80),
            thickness
        )

    # ---------------------------------------------------------
    # DRAW STABILITY BAR
    # ---------------------------------------------------------

    def draw_stability_bar(
        self,
        frame,
        x,
        y,
        width,
        height
    ):

        # Background
        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (45, 45, 45),
            -1
        )

        filled_width = int(
            width * self.stability / 100
        )

        if filled_width > 0:

            cv2.rectangle(
                frame,
                (x, y),
                (x + filled_width, y + height),
                (80, 200, 120),
                -1
            )

        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (100, 100, 100),
            1
        )

    # ---------------------------------------------------------
    # DRAW DASHBOARD
    # ---------------------------------------------------------

    def draw(
        self,
        frame,
        gesture=None,
        stability=None,
        active=None,
        category=None,
        wallpaper=None
    ):

        if gesture is not None:
            self.current_gesture = gesture

        if stability is not None:
            self.stability = max(0, min(100, stability))

        if active is not None:
            self.active = active

        if category is not None:
            self.category = category

        if wallpaper is not None:
            self.wallpaper = wallpaper

        height, width = frame.shape[:2]

        # -----------------------------------------------------
        # DARK OVERLAY
        # -----------------------------------------------------

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (width, height),
            (25, 25, 25),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.82,
            frame,
            0.18,
            0,
            frame
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        self.draw_text(
            frame,
            self.title,
            (30, 40),
            0.9,
            2
        )

        self.draw_text(
            frame,
            "AI-powered Windows Wallpaper Controller",
            (30, 68),
            0.48,
            1
        )

        status_text = "ACTIVE" if self.active else "PAUSED"

        cv2.circle(
            frame,
            (width - 100, 38),
            7,
            (80, 200, 120) if self.active else (100, 100, 100),
            -1
        )

        self.draw_text(
            frame,
            status_text,
            (width - 85, 44),
            0.5,
            1
        )

        cv2.line(
            frame,
            (30, 85),
            (width - 30, 85),
            (70, 70, 70),
            1
        )

        # -----------------------------------------------------
        # MAIN PANELS
        # -----------------------------------------------------

        left_x = 30
        left_y = 110

        left_w = int(width * 0.47)

        panel_h = height - 175

        right_x = left_x + left_w + 20
        right_w = width - right_x - 30

        # Left panel
        self.draw_box(
            frame,
            left_x,
            left_y,
            left_x + left_w,
            left_y + panel_h
        )

        # Right panel
        self.draw_box(
            frame,
            right_x,
            left_y,
            right_x + right_w,
            left_y + panel_h
        )

        # -----------------------------------------------------
        # LEFT PANEL - GESTURE CONTROL
        # -----------------------------------------------------

        self.draw_text(
            frame,
            "GESTURE CONTROL",
            (left_x + 20, left_y + 35),
            0.65,
            2
        )

        self.draw_text(
            frame,
            "Current Gesture",
            (left_x + 20, left_y + 75),
            0.48,
            1
        )

        self.draw_text(
            frame,
            self.current_gesture,
            (left_x + 20, left_y + 110),
            0.85,
            2
        )

        self.draw_text(
            frame,
            f"Gesture Stability: {self.stability}%",
            (left_x + 20, left_y + 150),
            0.5,
            1
        )

        self.draw_stability_bar(
            frame,
            left_x + 20,
            left_y + 165,
            left_w - 40,
            15
        )

        # -----------------------------------------------------
        # WALLPAPER INFORMATION
        # -----------------------------------------------------

        info_y = left_y + 205

        self.draw_text(
            frame,
            "WALLPAPER",
            (left_x + 20, info_y),
            0.58,
            2
        )

        self.draw_text(
            frame,
            "Category:",
            (left_x + 20, info_y + 35),
            0.45,
            1
        )

        self.draw_text(
            frame,
            self.category,
            (left_x + 115, info_y + 35),
            0.45,
            1
        )

        self.draw_text(
            frame,
            "Wallpaper:",
            (left_x + 20, info_y + 65),
            0.45,
            1
        )

        wallpaper_name = os.path.basename(
            str(self.wallpaper)
        )

        self.draw_text(
            frame,
            wallpaper_name[:22],
            (left_x + 115, info_y + 65),
            0.42,
            1
        )

        # -----------------------------------------------------
        # GESTURE MAPPINGS
        # -----------------------------------------------------
                
       

        controls_y = info_y + 100

        self.draw_text(
            frame,
            "GESTURE MAPPINGS",
            (left_x + 20, controls_y),
            0.50,
            2
        )

        controls = [
            ("OPEN PALM", "Activate"),
            ("FIST", "Pause"),
            ("ONE FINGER", "Next"),
            ("TWO FINGERS", "Previous"),
            ("THUMBS UP", "Next category"),
            ("THUMBS DOWN", "Previous category"),
        ]

        column_width = int((left_w - 50) / 2)

        row_y = controls_y + 32

        for index, (gesture_name, action) in enumerate(controls):

            column = index % 2
            row = index // 2

            x = left_x + 20 + (column * column_width)
            y = row_y + (row * 48)

            self.draw_text(
                frame,
                f"{gesture_name} -> {action}",
                (x, y),
                0.45,
                1
            )

        # -----------------------------------------------------
        # RIGHT PANEL - RECENT ACTIONS
        # -----------------------------------------------------

        self.draw_text(
            frame,
            "RECENT ACTIONS",
            (right_x + 20, left_y + 35),
            0.65,
            2
        )

        history_y = left_y + 75

        if not self.actions:

            self.draw_text(
                frame,
                "No actions yet",
                (right_x + 20, history_y),
                0.5,
                1
            )

        else:

            for action in self.actions:

                self.draw_text(
                    frame,
                    action[:42],
                    (right_x + 20, history_y),
                    0.40,
                    1
                )

                history_y += 27

        # -----------------------------------------------------
        # SESSION
        # -----------------------------------------------------

        session_y = left_y + panel_h - 95

        self.draw_text(
            frame,
            "SESSION",
            (right_x + 20, session_y),
            0.58,
            2
        )

        elapsed = int(
            time.time() - self.start_time
        )

        minutes = elapsed // 60
        seconds = elapsed % 60

        self.draw_text(
            frame,
            f"Running Time: {minutes:02d}:{seconds:02d}",
            (right_x + 20, session_y + 30),
            0.45,
            1
        )

        self.draw_text(
            frame,
            "Press Q to quit",
            (right_x + 20, session_y + 55),
            0.45,
            1
        )

        # -----------------------------------------------------
        # FOOTER
        # -----------------------------------------------------

        self.draw_text(
            frame,
            "AI Gesture Wallpaper Controller",
            (30, height - 15),
            0.36,
            1
        )

        self.draw_text(
            frame,
            "MediaPipe + OpenCV",
            (width - 165, height - 15),
            0.36,
            1
        )

        return frame