from enum import Enum

class GestureState(Enum):
    IDLE = 0
    SELECT = 1
    DRAW = 2

def classify_gesture(landmarks) -> GestureState:
    """
    Classify the hand gesture based on detected landmarks.
    
    Landmarks indices:
    Index Finger: Tip (8), PIP (6), MCP (5)
    Middle Finger: Tip (12), PIP (10), MCP (9)
    Ring Finger: Tip (16), PIP (14), MCP (13)
    Pinky Finger: Tip (20), PIP (18), MCP (17)
    
    A finger is considered 'up' if its tip is higher (y value is lower in image coordinates)
    than its PIP joint.
    """
    if not landmarks or len(landmarks) < 21:
        return GestureState.IDLE

    # Check if each finger is up (y coordinate decreases as we go up the screen)
    index_up = landmarks[8].y < landmarks[6].y
    middle_up = landmarks[12].y < landmarks[10].y
    ring_up = landmarks[16].y < landmarks[14].y
    pinky_up = landmarks[20].y < landmarks[18].y

    # Classify state
    # DRAW: Only index finger is up
    if index_up and not middle_up and not ring_up and not pinky_up:
        return GestureState.DRAW
        
    # SELECT: Index and Middle fingers are up, others are down
    elif index_up and middle_up and not ring_up and not pinky_up:
        return GestureState.SELECT
        
    # Any other state is IDLE (e.g. fist, open hand, invalid postures)
    else:
        return GestureState.IDLE
