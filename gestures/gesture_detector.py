
def detect_gesture(hand_landmarks):
    """
    Detect hand gestures using MediaPipe hand landmarks.

    Returns:
        str: Detected gesture name.
    """

    if not hand_landmarks:
        return "NO_HAND"

    # ============================================================
    # LANDMARKS
    # ============================================================

    wrist = hand_landmarks[0]

    thumb_tip = hand_landmarks[4]
    thumb_ip = hand_landmarks[3]

    index_tip = hand_landmarks[8]
    index_pip = hand_landmarks[6]

    middle_tip = hand_landmarks[12]
    middle_pip = hand_landmarks[10]

    ring_tip = hand_landmarks[16]
    ring_pip = hand_landmarks[14]

    pinky_tip = hand_landmarks[20]
    pinky_pip = hand_landmarks[18]

    # ============================================================
    # FINGER STATES
    # ============================================================

    index_extended = index_tip.y < index_pip.y

    middle_extended = middle_tip.y < middle_pip.y

    ring_extended = ring_tip.y < ring_pip.y

    pinky_extended = pinky_tip.y < pinky_pip.y

    # ============================================================
    # THUMB DETECTION
    # ============================================================

    thumb_up = (
        thumb_tip.y < thumb_ip.y
        and thumb_tip.y < index_pip.y
    )

    thumb_down = (
        thumb_tip.y > thumb_ip.y
        and thumb_tip.y > wrist.y
    )

    # ============================================================
    # THUMBS UP
    # ============================================================

    if (
        thumb_up
        and not index_extended
        and not middle_extended
        and not ring_extended
        and not pinky_extended
    ):
        return "THUMBS_UP"

    # ============================================================
    # THUMBS DOWN
    # ============================================================

    if (
        thumb_down
        and not index_extended
        and not middle_extended
        and not ring_extended
        and not pinky_extended
    ):
        return "THUMBS_DOWN"

    # ============================================================
    # OPEN PALM
    # ============================================================

    if (
        index_extended
        and middle_extended
        and ring_extended
        and pinky_extended
    ):
        return "OPEN_PALM"

    # ============================================================
    # FIST
    # ============================================================

    if (
        not index_extended
        and not middle_extended
        and not ring_extended
        and not pinky_extended
    ):
        return "FIST"

    # ============================================================
    # TWO FINGERS
    # ============================================================

    if (
        index_extended
        and middle_extended
        and not ring_extended
        and not pinky_extended
    ):
        return "TWO_FINGERS"

    # ============================================================
    # ONE FINGER
    # ============================================================

    if (
        index_extended
        and not middle_extended
        and not ring_extended
        and not pinky_extended
    ):
        return "ONE_FINGER"

    # ============================================================
    # UNKNOWN
    # ============================================================

    return "UNKNOWN"

