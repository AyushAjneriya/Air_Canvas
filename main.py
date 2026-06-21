import cv2
import time
import os
import config
from hand_tracker import HandTracker
from gestures import classify_gesture, GestureState
from toolbar import draw_toolbar, detect_tool_selection
from canvas import Canvas

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        print(f"Error: Could not open webcam with index {config.CAMERA_INDEX}.")
        print("Please check your camera connection or update CAMERA_INDEX in config.py.")
        return

    # Set camera resolution properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

    # Retrieve actual resolution (in case webcam doesn't support the requested one)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Webcam initialized successfully. Resolution: {width}x{height}")

    # Initialize tracker and canvas
    tracker = HandTracker()
    canvas = Canvas(width, height)

    # Initial state
    active_tool = "RED"
    prev_point = None
    
    # Timing for FPS calculation and save messages
    prev_time = time.time()
    save_msg_timer = 0.0
    save_msg_text = ""

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame from webcam.")
            break

        # 1. Flip the frame horizontally for mirror mode (intuitive drawing)
        frame = cv2.flip(frame, 1)

        # 2. Track hands (and draw landmarks overlay on the webcam feed)
        frame = tracker.find_hands(frame, draw=True)
        
        # 3. Retrieve landmarks and fingertip positions
        landmarks, index_tip, middle_tip = tracker.get_landmarks_and_tips(width, height)

        # 4. Classify gesture state
        state = classify_gesture(landmarks)

        # 5. Handle State Actions
        if state == GestureState.SELECT:
            # Enforce prev_point reset to avoid line jump when returning to DRAW
            prev_point = None
            
            # Use index fingertip for tool selection in the toolbar
            if index_tip is not None:
                selected = detect_tool_selection(index_tip[0], index_tip[1], width)
                if selected is not None:
                    active_tool = selected

            # Draw visual SELECT mode indicators on fingertips (circles)
            if index_tip is not None:
                cv2.circle(frame, index_tip, 12, config.COLOR_WHITE, 2, cv2.LINE_AA)
            if middle_tip is not None:
                cv2.circle(frame, middle_tip, 12, config.COLOR_WHITE, 2, cv2.LINE_AA)

        elif state == GestureState.DRAW:
            # Draw on canvas if index fingertip is available
            if index_tip is not None:
                # Eraser has a thicker brush and draws COLOR_BLACK (zeros) to clear strokes
                if active_tool == "ERASER":
                    color = config.TOOL_COLORS[active_tool]
                    thickness = config.DEFAULT_BRUSH_THICKNESS * config.ERASER_THICKNESS_MULTIPLIER
                else:
                    color = config.TOOL_COLORS[active_tool]
                    thickness = config.DEFAULT_BRUSH_THICKNESS
                
                # Draw line from previous point to current index fingertip
                canvas.draw_stroke(prev_point, index_tip, color, thickness)
                prev_point = index_tip

                # Draw a small indicator of the drawing color/brush on the camera feed
                cv2.circle(frame, index_tip, thickness + 2, color, cv2.FILLED, cv2.LINE_AA)

        else:  # GestureState.IDLE
            prev_point = None

        # 6. Blend Canvas onto Webcam Feed
        blended_frame = canvas.blend_canvas(frame)

        # 7. Render Toolbar on top of blended frame
        draw_toolbar(blended_frame, active_tool, width)

        # 8. Overlay UI Info (Gesture State, Active Tool, FPS)
        # Calculate FPS
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time

        # Render status texts
        cv2.putText(blended_frame, f"FPS: {int(fps)}", (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_GREEN, 2, cv2.LINE_AA)
        
        cv2.putText(blended_frame, f"State: {state.name}", (150, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2, cv2.LINE_AA)
        
        cv2.putText(blended_frame, f"Brush: {active_tool}", (350, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2, cv2.LINE_AA)
        
        # Display save status overlay message if active
        if curr_time < save_msg_timer:
            cv2.putText(blended_frame, save_msg_text, (10, height - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, config.COLOR_GREEN, 2, cv2.LINE_AA)

        # 9. Render Screen Frame
        cv2.imshow("Air Canvas", blended_frame)

        # 10. Handle Keyboard Controls
        key = cv2.waitKey(1) & 0xFF
        
        if key == config.KEY_CLEAR:
            canvas.clear()
            print("Canvas cleared.")
            save_msg_text = "Canvas Cleared"
            save_msg_timer = time.time() + 2.0  # Show message for 2 seconds

        elif key == config.KEY_SAVE:
            success, filepath = canvas.save_canvas()
            if success:
                msg = f"Saved: {os.path.basename(filepath)}"
                print(msg)
                save_msg_text = msg
            else:
                save_msg_text = "Failed to save canvas"
            save_msg_timer = time.time() + 3.0  # Show message for 3 seconds

        elif key == config.KEY_QUIT_Q or key == config.KEY_QUIT_ESC:
            print("Exiting application...")
            break

    # Release webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
