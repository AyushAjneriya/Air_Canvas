import sys
import os

# Adjust path to import gestures
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gestures import classify_gesture, GestureState

class MockLandmark:
    def __init__(self, x=0.5, y=0.5, z=0.0):
        self.x = x
        self.y = y
        self.z = z

def create_mock_landmarks(extended_fingers=None):
    """
    Creates a list of 21 mock landmarks.
    By default, all PIP joints are at y = 0.5 and tips are at y = 0.6 (folded/down).
    If a finger name is in extended_fingers, its tip is set to y = 0.4 (extended/up).
    """
    if extended_fingers is None:
        extended_fingers = []

    landmarks = [MockLandmark() for _ in range(21)]

    # Set PIP joints at y = 0.5
    landmarks[6].y = 0.5   # Index PIP
    landmarks[10].y = 0.5  # Middle PIP
    landmarks[14].y = 0.5  # Ring PIP
    landmarks[18].y = 0.5  # Pinky PIP

    # Set tips default to y = 0.6 (down)
    landmarks[8].y = 0.6   # Index Tip
    landmarks[12].y = 0.6  # Middle Tip
    landmarks[16].y = 0.6  # Ring Tip
    landmarks[20].y = 0.6  # Pinky Tip

    # Set tips of extended fingers to y = 0.4 (up)
    if "index" in extended_fingers:
        landmarks[8].y = 0.4
    if "middle" in extended_fingers:
        landmarks[12].y = 0.4
    if "ring" in extended_fingers:
        landmarks[16].y = 0.4
    if "pinky" in extended_fingers:
        landmarks[20].y = 0.4

    return landmarks

def test_gestures():
    print("Running gesture classification unit tests...")

    # Test Case 1: All fingers folded (Fist) -> IDLE
    lms = create_mock_landmarks(extended_fingers=[])
    state = classify_gesture(lms)
    assert state == GestureState.IDLE, f"Expected IDLE, got {state}"
    print("  - Case 1 (Fist/Idle) passed.")

    # Test Case 2: Only Index extended -> DRAW
    lms = create_mock_landmarks(extended_fingers=["index"])
    state = classify_gesture(lms)
    assert state == GestureState.DRAW, f"Expected DRAW, got {state}"
    print("  - Case 2 (Only Index / Draw) passed.")

    # Test Case 3: Index + Middle extended -> SELECT
    lms = create_mock_landmarks(extended_fingers=["index", "middle"])
    state = classify_gesture(lms)
    assert state == GestureState.SELECT, f"Expected SELECT, got {state}"
    print("  - Case 3 (Index + Middle / Select) passed.")

    # Test Case 4: Index + Middle + Ring extended -> IDLE (invalid gesture)
    lms = create_mock_landmarks(extended_fingers=["index", "middle", "ring"])
    state = classify_gesture(lms)
    assert state == GestureState.IDLE, f"Expected IDLE, got {state}"
    print("  - Case 4 (Index + Middle + Ring / Idle) passed.")

    # Test Case 5: Empty landmarks -> IDLE
    state = classify_gesture([])
    assert state == GestureState.IDLE, f"Expected IDLE, got {state}"
    print("  - Case 5 (Empty landmarks) passed.")

    print("\nAll unit tests passed successfully!")

if __name__ == "__main__":
    test_gestures()
