import cv2
import mediapipe as mp
import time
import os

from gestures.gesture_detector import detect_gesture
from wallpaper_controller import WallpaperController
from ui.dashboard import Dashboard


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PATH = "models/hand_landmarker.task"

GESTURE_COOLDOWN = 0.8

GESTURE_HOLD_TIME = 0.2


# ============================================================
# MEDIAPIPE SETUP
# ============================================================

BaseOptions = mp.tasks.BaseOptions

HandLandmarker = (
    mp.tasks.vision.HandLandmarker
)

HandLandmarkerOptions = (
    mp.tasks.vision.HandLandmarkerOptions
)

VisionRunningMode = (
    mp.tasks.vision.RunningMode
)


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)


# ============================================================
# WALLPAPER CONTROLLER
# ============================================================

controller = WallpaperController()


# ============================================================
# DASHBOARD
# ============================================================

dashboard = Dashboard(
    "AI Gesture Wallpaper"
)


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)


if not cap.isOpened():

    print(
        "ERROR: Could not open webcam."
    )

    exit()


# ============================================================
# APPLICATION STATE
# ============================================================

controls_active = False

last_gesture = None

stable_gesture = None

gesture_start_time = 0

last_action_time = 0

current_gesture = "NO_HAND"


# ============================================================
# WINDOW
# ============================================================

WINDOW_NAME = "AI Gesture Wallpaper"

cv2.namedWindow(
    WINDOW_NAME,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    WINDOW_NAME,
    1100,
    700
)


# ============================================================
# MEDIAPIPE
# ============================================================

with HandLandmarker.create_from_options(
    options
) as landmarker:

    print()
    print(
        "======================================"
    )
    print(
        "       AI GESTURE WALLPAPER"
    )
    print(
        "======================================"
    )
    print()
    print(
        "Professional dashboard enabled."
    )
    print()
    print("Controls:")
    print(
        "  OPEN PALM    -> Activate controls"
    )
    print(
        "  FIST         -> Pause controls"
    )
    print(
        "  ONE FINGER   -> Next wallpaper"
    )
    print(
        "  TWO FINGERS  -> Previous wallpaper"
    )
    print(
        "  THUMBS UP    -> Next category"
    )
    print(
        "  THUMBS DOWN  -> Previous category"
    )
    print()
    print(
        "Gesture stabilization enabled."
    )
    print("Press Q to quit.")
    print()

    while True:

        # ====================================================
        # CAMERA FRAME
        # ====================================================

        success, frame = cap.read()

        if not success:

            print(
                "ERROR: Could not read webcam frame."
            )

            break

        frame = cv2.flip(
            frame,
            1
        )

        height, width, _ = frame.shape


        # ====================================================
        # MEDIAPIPE PROCESSING
        # ====================================================

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = landmarker.detect(
            mp_image
        )


        # ====================================================
        # GESTURE DETECTION
        # ====================================================

        gesture = "NO_HAND"


        if result.hand_landmarks:

            hand_landmarks = (
                result.hand_landmarks[0]
            )

            gesture = detect_gesture(
                hand_landmarks
            )


            # =================================================
            # DRAW LANDMARKS
            # =================================================

            for landmark in hand_landmarks:

                x = int(
                    landmark.x
                    * width
                )

                y = int(
                    landmark.y
                    * height
                )

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (255, 255, 255),
                    -1
                )


            # =================================================
            # HAND CONNECTIONS
            # =================================================

            connections = [

                (0, 1),
                (1, 2),
                (2, 3),
                (3, 4),

                (0, 5),
                (5, 6),
                (6, 7),
                (7, 8),

                (0, 9),
                (9, 10),
                (10, 11),
                (11, 12),

                (0, 13),
                (13, 14),
                (14, 15),
                (15, 16),

                (0, 17),
                (17, 18),
                (18, 19),
                (19, 20),

                (5, 9),
                (9, 13),
                (13, 17)
            ]


            for start, end in connections:

                x1 = int(
                    hand_landmarks[start].x
                    * width
                )

                y1 = int(
                    hand_landmarks[start].y
                    * height
                )

                x2 = int(
                    hand_landmarks[end].x
                    * width
                )

                y2 = int(
                    hand_landmarks[end].y
                    * height
                )

                cv2.line(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 255, 255),
                    2
                )


        current_gesture = gesture


        # ====================================================
        # GESTURE STABILIZATION
        # ====================================================

        current_time = time.time()


        if gesture != last_gesture:

            stable_gesture = gesture

            gesture_start_time = (
                current_time
            )

            last_gesture = gesture


        gesture_held_time = (
            current_time
            - gesture_start_time
        )


        stability = min(
            gesture_held_time
            / GESTURE_HOLD_TIME,
            1.0
        )


        stability_percent = int(
            stability * 100
        )


        # ====================================================
        # GESTURE ACTIONS
        # ====================================================

        if (
            stable_gesture == gesture
            and gesture_held_time
            >= GESTURE_HOLD_TIME
            and current_time
            - last_action_time
            >= GESTURE_COOLDOWN
        ):


            # ------------------------------------------------
            # OPEN PALM
            # ------------------------------------------------

            if gesture == "OPEN_PALM":

                if not controls_active:

                    controls_active = True

                    print(
                        "Controls ACTIVATED"
                    )

                    dashboard.add_action(
                        "OPEN PALM",
                        "Controls Activated"
                    )

                    last_action_time = (
                        current_time
                    )


            # ------------------------------------------------
            # FIST
            # ------------------------------------------------

            elif gesture == "FIST":

                if controls_active:

                    controls_active = False

                    print(
                        "Controls PAUSED"
                    )

                    dashboard.add_action(
                        "FIST",
                        "Controls Paused"
                    )

                    last_action_time = (
                        current_time
                    )


            # ------------------------------------------------
            # OTHER CONTROLS
            # ------------------------------------------------

            elif controls_active:


                # =============================================
                # NEXT WALLPAPER
                # =============================================

                if gesture == "ONE_FINGER":

                    controller.next_wallpaper()

                    dashboard.add_action(
                        "ONE FINGER",
                        "Next Wallpaper"
                    )

                    last_action_time = (
                        current_time
                    )


                # =============================================
                # PREVIOUS WALLPAPER
                # =============================================

                elif gesture == "TWO_FINGERS":

                    controller.previous_wallpaper()

                    dashboard.add_action(
                        "TWO FINGERS",
                        "Previous Wallpaper"
                    )

                    last_action_time = (
                        current_time
                    )


                # =============================================
                # NEXT CATEGORY
                # =============================================

                elif gesture == "THUMBS_UP":

                    controller.next_category()

                    dashboard.add_action(
                        "THUMBS UP",
                        "Next Category"
                    )

                    last_action_time = (
                        current_time
                    )


                # =============================================
                # PREVIOUS CATEGORY
                # =============================================

                elif gesture == "THUMBS_DOWN":

                    controller.previous_category()

                    dashboard.add_action(
                        "THUMBS DOWN",
                        "Previous Category"
                    )

                    last_action_time = (
                        current_time
                    )


        # ====================================================
        # CURRENT WALLPAPER
        # ====================================================

        category = (
            controller.get_current_category()
            or "None"
        )

        wallpaper_path = None


        if category in controller.categories:

            wallpapers = (
                controller.categories[
                    category
                ]
            )

            if wallpapers:

                current_index = (
                    controller.current_index
                )

                if (
                    0 <= current_index
                    < len(wallpapers)
                ):

                    wallpaper_path = (
                        wallpapers[
                            current_index
                        ]
                    )


        # ====================================================
        # DASHBOARD
        # ====================================================

        frame = dashboard.draw(
    frame,
    current_gesture,
    stability_percent,
    controls_active,
    category,
    wallpaper_path
)


        # ====================================================
        # SHOW WINDOW
        # ====================================================

        cv2.imshow(
            WINDOW_NAME,
            frame
        )


        # ====================================================
        # KEYBOARD
        # ====================================================

        key = (
            cv2.waitKey(1)
            & 0xFF
        )


        if key == ord("q"):

            break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()

print()
print(
    "AI Gesture Wallpaper stopped."
)