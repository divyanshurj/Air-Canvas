import cv2
import numpy as np
import HandTrackingModule as htm
import random
import math 

cap = cv2.VideoCapture(0)
cap.set(3, 3840) 
cap.set(4, 2160)  

detector = htm.handDetector(detectionCon=0.85, trackCon=0.9)

draw_color = (147, 20, 255) 
draw_thickness = 4 

strokes = []          
current_stroke = []   
grabbed_stroke_idx = -1 
prev_px, prev_py = 0, 0 

while True:
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    
    black_bg = np.zeros_like(img)
    canvas = np.zeros_like(img) 

    black_bg = detector.findHands(img, draw=True, draw_img=black_bg)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x_index, y_index = lmList[8][1], lmList[8][2] 
        x_thumb, y_thumb = lmList[4][1], lmList[4][2] 
        
        pinch_dist = math.hypot(x_index - x_thumb, y_index - y_thumb)
        cx, cy = (x_index + x_thumb) // 2, (y_index + y_thumb) // 2

        fingers = detector.fingersUp()

        # --- MODE 1: PINCH AND DRAG ---
        if pinch_dist < 40: # If fingers are pinched
            cv2.circle(black_bg, (cx, cy), 15, (0, 255, 255), cv2.FILLED) # Yellow grab cursor
            
            # 1. Try to grab a shape if we arent holding one
            if grabbed_stroke_idx == -1:
                for i, stroke in enumerate(strokes):
                    for px, py in stroke:
                        # INCREASED GRAB RADIUS to 60 for easier grabbing
                        if math.hypot(cx - px, cy - py) < 60:
                            grabbed_stroke_idx = i
                            break
                    if grabbed_stroke_idx != -1: break
                prev_px, prev_py = cx, cy

            # 2. Move the shape we are holding
            if grabbed_stroke_idx != -1:
                dx = cx - prev_px
                dy = cy - prev_py
                new_stroke = []
                for px, py in strokes[grabbed_stroke_idx]:
                    new_stroke.append((int(px + dx), int(py + dy)))
                strokes[grabbed_stroke_idx] = new_stroke
                prev_px, prev_py = cx, cy

        # --- MODE 2: DRAW (Index up, thumb far away) ---
        elif fingers[1]==1 and fingers[2]==0 and pinch_dist > 40:
            current_stroke.append((x_index, y_index))
            
            for _ in range(15):
                sx = x_index + random.randint(-30, 30)
                sy = y_index + random.randint(-30, 30)
                brightness = random.randint(150, 255)
                cv2.circle(black_bg, (sx, sy), random.randint(1, 2), (brightness, brightness, 255), -1)

        # --- MODE 3: STOP DRAWING / LET GO ---
        else:
            if len(current_stroke) > 0:
                strokes.append(current_stroke)
                current_stroke = []
            grabbed_stroke_idx = -1 # Drop the shape

        # --- MODE 4: CLEAR SCREEN (All 4 fingers up) ---
        if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:
            strokes = [] 

    # Render all saved shapes
    for i, stroke in enumerate(strokes):
        # If we are currently grabbing this shape, highlight it in glowing green!
        current_color = (0, 255, 0) if i == grabbed_stroke_idx else draw_color
        current_thick = 8 if i == grabbed_stroke_idx else draw_thickness
        
        for j in range(1, len(stroke)):
            cv2.line(canvas, stroke[j-1], stroke[j], current_color, current_thick)

    # Render the line being drawn right now
    for i in range(1, len(current_stroke)):
        cv2.line(canvas, current_stroke[i-1], current_stroke[i], draw_color, draw_thickness)

    final_output = cv2.bitwise_or(black_bg, canvas)

    cv2.imshow("Air Canvas Pro", final_output)
    if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()