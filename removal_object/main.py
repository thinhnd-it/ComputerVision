from cv2 import cv2
from SeamCarving import SeamCarver
import os
import getopt
import sys
from os import path
import numpy as np
draw = False  # true if the mouse is pressed. Press m to shift into curve mode.
mode = False  # if True, draw rectangle.
a, b = -1, -1
# mouse callback function


def object_removal(filename_input, filename_output, filename_mask):
    obj = SeamCarver(filename_input, 0, 0, object_mask=filename_mask)
    obj.save_result(filename_output)


def draw_circle(event, x, y, flags, param):
    global a, b, draw, mode
    if(event == cv2.EVENT_LBUTTONDOWN):
        draw = True
    elif (event == cv2.EVENT_MOUSEMOVE):
        if draw:
            cv2.circle(img, (x, y), brush_size, (0, 0, 255), -1)
            cv2.circle(mask, (x, y), brush_size, (255, 255, 255), -1)
    elif(event == cv2.EVENT_LBUTTONUP):
        draw = False


# def handle_remove(input_image, output_image, input_mask, mask, img):


def usage():
    print("Usage: python main.py [options] \n\n\
    Options: \n\
    \t-h\tPrint a brief help message and exits..\n\
    \t-s\t(Required) Specify a source image.\n\
    \t-b\t(Optional) Specify size of brush.\n")


if __name__ == "__main__":
    args = {}
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hs:b:p:")
    except getopt.GetoptError as err:
        print(err)
        print("See help: main.py -h")
        exit(2)
    for o, a in opts:
        if o in ("-h"):
            usage()
            exit()
        elif o in ("-s"):
            args['file_input'] = a
        elif o in ("-b"):
            args['brush_size'] = a
        else:
            assert False, "unhandled option"

    if ('file_input' not in args):
        usage()
        exit()
    if "brush_size" not in args:
        brush_size = 10
    else:
        brush_size = int(args['brush_size'])
    filename_input = args['file_input']
    filename_output = 'image_result.png'
    filename_mask = 'mask.png'

    input_image = os.path.join('', "", filename_input)
    input_mask = os.path.join('', "", filename_mask)
    output_image = os.path.join('', "", filename_output)

    if filename_input is None:
        print('File input not exist.')
        exit()
    img = cv2.imread(filename_input)
    mask = np.zeros(img.shape, np.uint8)
    # handle_remove(input_image, output_image, input_mask,
    #               mask, img)

    img_copy = img.copy()
    mask_copy = mask.copy()
    window_name = 'Draw mask. s:save; r: reset; q:quit'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_circle)
    while True:
        cv2.imshow(window_name, img)
        k = cv2.waitKey(1) & 0xFF
        # cv2.imshow('mask', mask)
        if k == ord('r'):
            img = img_copy.copy()
            mask = mask_copy.copy()
        elif k == ord("s"):
            cv2.imwrite('mask.png', mask)
            print('[INFO]:    processing')
            object_removal(input_image, output_image, input_mask)
            break
        elif k == ord("q"):
            cv2.destroyAllWindows()
            exit()
    print('[INFO]:    done')
    result = cv2.imread('image_result.png')
    cv2.imshow('result', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
