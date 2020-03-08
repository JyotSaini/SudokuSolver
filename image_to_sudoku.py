from PIL import Image
from pathlib import Path
import os
import re
import numpy as np

from parse_image_v2 import parse_image

def crop_sudoku(PATH_TO_IMAGE, SAVE_TO):
    parsed_image_dict = parse_image('./whole_sudoku/whole_sudoku_inference_graph.pb', './whole_sudoku/label_map.pbtxt', PATH_TO_IMAGE)
    im = Image.open(PATH_TO_IMAGE)
    im_width, im_height = im.size

    # Create a boolean mask for all the usable sudokus found
    parsed_image_mask = [False] * parsed_image_dict['num_detections'] 
    num_sudokus = 0

    for detection_num in reversed(range(0, parsed_image_dict['num_detections'])):
        if parsed_image_dict['detection_scores'][detection_num] > 0.92:
            parsed_image_mask[detection_num] = True
            num_sudokus += 1

    cropped_sudoku_images = [None] * num_sudokus
    image_num = 0

    for mask_num in range(num_sudokus):
        # print(num_sudokus)
        if parsed_image_mask[mask_num]:
            # print(parsed_image_dict['detection_boxes'][mask_num])
            # print(parsed_image_dict['detection_scores'][mask_num])
            # print(parsed_image_dict['detection_classes'][mask_num])
            box = tuple(parsed_image_dict['detection_boxes'][mask_num].tolist())

            im_left = im_width * box[1]
            im_top = im_height * box[0]
            im_right = im_width * box[3]
            im_bottom = im_height * box[2]

            cropped_sudoku_images[image_num] = im.crop((im_left, im_top, im_right, im_bottom))
            cropped_sudoku_images[image_num] = cropped_sudoku_images[image_num].convert('RGB')

            CROPPED_IMAGE_PATH = PATH_TO_IMAGE[:-4] + '_cropped_' + str(image_num) + '.jpg'
            CROPPED_IMAGE_PATH = re.sub("^.*[/]", SAVE_TO, CROPPED_IMAGE_PATH)

            cropped_sudoku_images[image_num].save(CROPPED_IMAGE_PATH)

            image_num += 1

def convert_to_matrix(PATH_TO_IMAGE, SAVE_TO):
    parsed_image_dict = parse_image('./sudoku_parser/sudoku_parser_inference_graph.pb', './sudoku_parser/label_map.pbtxt', PATH_TO_IMAGE)
    im = Image.open(PATH_TO_IMAGE)
    im_width, im_height = im.size

    num_detected_cells = 0

    for detection_num in reversed(range(0, parsed_image_dict['num_detections'])):
        if parsed_image_dict['detection_scores'][detection_num] >= 0.6:
            num_detected_cells += 1

    converted_sudoku = [[0 for i in range(9)] for i in range(9)]
    converted_sudoku_mask = [[0 for i in range(9)] for i in range(9)]
    converted_sudoku_likelihood = [[0 for i in range(9)] for i in range(9)]

    x_min = 1
    y_min = 1
    x_max = 0
    y_max = 0
    x_range = [0] * 10
    y_range = [0] * 10

    for cell_num in range(min(num_detected_cells, 81)):
        box = tuple(parsed_image_dict['detection_boxes'][cell_num].tolist())
        if box[0] < x_min:
            x_min = box[0]
        if box[1] < y_min:
            y_min = box[1]
        if box[2] > x_max:
            x_max = box[2]
        if box[3] > y_max:
            y_max = box[3]

    x_range[0] = x_min
    y_range[0] = y_min
    x_diff = (x_max - x_min) / 9
    y_diff = (y_max - y_min) / 9
    x_half_diff = x_diff / 2
    y_half_diff = y_diff / 2

    for num_iter in range(9):
        x_range[num_iter + 1] = x_range[num_iter] + x_diff
        y_range[num_iter + 1] = y_range[num_iter] + y_diff

    x_range[0] -= x_half_diff
    y_range[0] -= y_half_diff

    for num_iter in range(9):
        x_range[num_iter + 1] -= x_half_diff
        y_range[num_iter + 1] -= y_half_diff

    for cell in range(min(num_detected_cells, 81)):
        box = tuple(parsed_image_dict['detection_boxes'][cell].tolist())
        curr_x = 0
        curr_y = 0

        for check_x in range(9):
            if x_range[check_x] < box[0] and box[0] < x_range[check_x + 1]:
                curr_x = check_x

        for check_y in range(9):
            if y_range[check_y] < box[1] and box[1] < y_range[check_y + 1]:
                curr_y = check_y

        converted_sudoku[curr_x][curr_y] = parsed_image_dict['detection_classes'][cell] % 10
        converted_sudoku_mask[curr_x][curr_y] = 1
        converted_sudoku_likelihood[curr_x][curr_y] = parsed_image_dict['detection_scores'][cell]

    CONVERTED_SUDOKU_PATH = PATH_TO_IMAGE[:-4] + '.txt'
    CONVERTED_SUDOKU_PATH = re.sub("^.*[/]", SAVE_TO, CONVERTED_SUDOKU_PATH)
    CONVERTED_SUDOKU_PATH = re.sub("cropped", "converted", CONVERTED_SUDOKU_PATH)

    sudoku_file = open(CONVERTED_SUDOKU_PATH, "w+")
    sudoku_file.write('Unsolved Sudoku: \n')
    for row in converted_sudoku:
        for cell in row:
            sudoku_file.write(str(cell) + ',')
        sudoku_file.write('\n')
    sudoku_file.write('Changed Values: \n')
    for row in converted_sudoku_mask:
        for cell in row:
            sudoku_file.write(str(cell) + ',')
        sudoku_file.write('\n')
    sudoku_file.write('Sureness: \n')
    for row in converted_sudoku_likelihood:
        for cell in row:
            sudoku_file.write(str(cell) + ',')
        sudoku_file.write('\n')
    sudoku_file.close()


def test_all():
    currPath = Path(__file__).parent.absolute()

    for root, directories, files in os.walk('test'):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)

            filepath = str(currPath).replace('\\', '/') + "/" + filepath.replace('\\', '/')

            if filepath.endswith('.jpg'):
                crop_sudoku(filepath, './cropped/')

    for root, directories, files in os.walk('cropped'):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)

            filepath = str(currPath).replace('\\', '/') + "/" + filepath.replace('\\', '/')

            if filepath.endswith('.jpg'):
                convert_to_matrix(filepath, './converted/')

test_all()
# convert_to_matrix('./cropped/0_cropped_0.jpg', './converted/')
