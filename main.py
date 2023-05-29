import cv2
import cv2 as cv
from flask import Response, Flask, render_template
import os

app = Flask(__name__, template_folder='templates', static_folder='static')


# loading the Colab trained network using opencv
net = cv.dnn.readNet('yolov4-custom_last.weights','yolov4-custom.cfg.txt')
model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(256,256),scale=1/255.)


# GETTING 2D IMAGES TO AUGMENT DURING LIVE STREAMING
# curvedMayo img
curveimg = cv2.imread('augment_Messages/curvedMayo_box.jpg')
curveimg = cv2.resize(curveimg,(320,60), interpolation = cv2.INTER_LINEAR)

# dissectionClamp_box img
dissectimg = cv2.imread('augment_Messages/dissectionClamp_box.jpg')
dissectimg = cv2.resize(dissectimg,(320,60), interpolation = cv2.INTER_LINEAR)

# scalpelN4_box img
scalpelimg = cv2.imread('augment_Messages/scalpelN4_box.jpg')
scalpelimg = cv2.resize(scalpelimg,(320,60), interpolation = cv2.INTER_LINEAR)

# starightMayo_box img
straightimg = cv2.imread('augment_Messages/straightMayo_box.jpg')
straightimg = cv2.resize(straightimg,(320,60), interpolation = cv2.INTER_LINEAR)

# tumar_box img
tumarimg = cv2.imread('augment_Messages/tumar_box.jpg')
tumarimg = cv2.resize(tumarimg,(320,60), interpolation = cv2.INTER_LINEAR)


# CLASSES IN OUR DATASET
mclass = {0:'Scalpel', 1:'Dissection Clamp',
          2:'Staright Scissor', 3:'Curved Scissor'}


# DETECTING
def detect():
    cam = cv2.VideoCapture(2)  # if video don't display on website use 0 or 2 or 1

    while True:

        # READ FRAMES FROM WEBCAM EVERY SECOND
        success, frame = cam.read()

        if not success:
            break

        else:

            # MODEL.DETECT() DETECT OUR OBJECT AND RETURNS CLASSID, ACCURACY SCORE & BOUNDING BOX COORDINATES
            (class_ids, scores, bboxes) = model.detect(frame = frame, nmsThreshold = 0.6) #nms = non max suppression threshold

            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                print('class_id',class_id)
                print('score-',score)
                print('box-',bbox)

                x,y,w,h = bbox  # bounding box coordinates
                print(x,y,w,h)

                
                # DEFINING MY OWN VARIABLES FOR DRAWING BOUNDING BOX
                rect_x1 = x     #xmin
                rect_y1 = y     #ymin
                rect_x2 = x+w   #xmax
                rect_y2 = y+h   #ymax


                # BASED ON THE CLASSID OF THE DETECTED OBJECT, AUGMENT THE 2D IMAGE IN THE FRAME


                if class_ids.any() == 0:    #IF THE CLASSID IS 0
                    h2, w2, _ = scalpelimg.shape

                    if (rect_y1 >= h and rect_x1<=640/2):  #640,480 is the frame width and height
                        frame[abs(rect_y1-h2):rect_y1, rect_x1: rect_x1+w2] = scalpelimg

                        # PUTTING DETECT OBJECT NAME ON TOP OF THE BBOX
                        txt = mclass[class_id]
                        cv2.putText(frame, txt, (x, y - 65),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=1, color=(0, 255, 0), thickness=2)  # y-5 bcz text shouldn't overlap

                        # DRAWING THE BOUNDING BOX USING THE BBOX COORDINATES
                        cv2.rectangle(frame, (x,y), (x+w,y+h), color=(255,0,0), thickness=3)

                        # Naming a window
                        # cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

                        # Using resizeWindow()
                        # cv2.resizeWindow("Resized_Window", 1080, 720)

                        # Displaying the image
                        # cv2.imshow("Resized_Window", frame)


                elif class_ids.any() == 1:
                    h2, w2, _ = dissectimg.shape

                    if (rect_y1 >= h and rect_x1<=640/2):
                        frame[abs(rect_y1-h2):rect_y1, rect_x1: rect_x1+w2] = dissectimg

                        # PUTTING DETECT OBJECT NAME ON TOP OF THE BBOX
                        txt = mclass[class_id]
                        cv2.putText(frame, txt, (x, y - 65),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=1, color=(0, 255, 0), thickness=2)  # y-5 bcz text shouldn't overlap

                        # drawing the bbox
                        cv2.rectangle(frame, (x,y), (x+w,y+w), color=(255,0,0), thickness=3)

                        # Naming a window
                        # cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

                        # Using resizeWindow()
                        # cv2.resizeWindow("Resized_Window", 1080, 720)

                        # Displaying the image
                        # cv2.imshow("Resized_Window", frame)


                elif class_ids.any() == 2:
                    h2, w2, _ = straightimg.shape

                    if (rect_y1 >= h and rect_x1<=640/2):
                        frame[abs(rect_y1-h2):rect_y1, rect_x1: rect_x1+w2] = straightimg

                        # PUTTING DETECT OBJECT NAME ON TOP OF THE BBOX
                        txt = mclass[class_id]
                        cv2.putText(frame, txt, (x, y - 65),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=1, color=(0, 255, 0), thickness=2)  # y-5 bcz text shouldn't overlap

                        # drawing the bbox
                        cv2.rectangle(frame, (x,y), (x+w,y+h), color=(255,0,0), thickness=3)

                        # Naming a window
                        # cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

                        # Using resizeWindow()
                        # cv2.resizeWindow("Resized_Window", 1080, 720)

                        # Displaying the image
                        # cv2.imshow("Resized_Window", frame)


                elif class_ids.any() == 3:
                    h2, w2, _ = curveimg.shape

                    if (rect_y1 >= h and rect_x1<=640/2):
                        frame[abs(rect_y1-h2):rect_y1, rect_x1: rect_x1+w2] = curveimg

                        # PUTTING DETECT OBJECT NAME ON TOP OF THE BBOX
                        txt = mclass[class_id]
                        cv2.putText(frame, txt, (x, y - 65),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=1, color=(0, 255, 0), thickness=2)  # y-5 bcz text shouldn't overlap

                        # drawing the bbox
                        cv2.rectangle(frame, (x,y), (x+w,y+h), color=(255,0,0), thickness=3)

                        # Naming a window
                        # cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

                        # Using resizeWindow()
                        # cv2.resizeWindow("Resized_Window", 1080, 720)

                        # Displaying the image
                        # cv2.imshow("Resized_Window", frame)


                elif class_ids.any() == 5:
                    h2, w2, _ = tumarimg.shape

                    if (rect_y1 >= h and rect_x1<=640/2):
                        frame[abs(rect_y1-h2):rect_y1, rect_x1: rect_x1+w2] = tumarimg

                        # PUTTING DETECT OBJECT NAME ON TOP OF THE BBOX
                        txt = mclass[class_id]
                        cv2.putText(frame, txt, (x, y - 65),
                                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=1, color=(0, 255, 0), thickness=2)  # y-5 bcz text shouldn't overlap

                        # drawing the bbox
                        cv2.rectangle(frame, (x,y), (x+w,y+h), color=(255,0,0), thickness=3)

                        # Naming a window
                        # cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

                        # Using resizeWindow()
                        # cv2.resizeWindow("Resized_Window", 1080, 720)

                        # # Displaying the image
                        # cv2.imshow("Resized_Window", frame)


            ret, buffer = cv2.imencode('.jpg',frame)  # encode the frame so that flask can return it as a response in bytes format

            frame = buffer.tobytes()        # convert each frame to a byte object

            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


# consistently call detect() which yields each detected object frame on every call
@app.route('/video_feed')
def video_feed():
    return Response(detect(), mimetype='multipart/x-mixed-replace; boundary=frame')


# it renders each frame on html
@app.route('/liveStreming', methods=['GET','POST']) # default endpoints
def liveStreming():
    return render_template('liveStreming.html')


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

