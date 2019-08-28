from matplotlib import pyplot as plt
import cv2
import os
import json
import pycocotools.mask as mask_utils
import numpy as np
import random

# def vis_img_group(imgs_path, columns = 10, rows = 10):
#     w=10
#     h=10
#     fig=plt.figure(figsize=(16, 16))
#     fig.tight_layout()
#     for i in range(1, min(columns*rows +1, len(imgs_path)+1)):
#         img = plt.imread(imgs_path[i-1])
#         img = cv2.resize(img,(255,255))
#         fig.add_subplot(rows, columns, i)
#         plt.axis('off')
#         plt.imshow(img)
#     plt.subplots_adjust(wspace=0, hspace=0)
#     plt.show()
    
def vis_img_group(imgs_numpy, columns = 2, rows = 5):
    w=10
    h=10
    fig=plt.figure(figsize=(20, 20))
    fig.tight_layout()
    for i in range(1, min(columns*rows +1, len(imgs_numpy)+1)):
#         img = cv2.resize(imgs_numpy[i-1],(480,720))
        fig.add_subplot(rows, columns, i)
        plt.axis('off')
        plt.imshow(imgs_numpy[i-1])
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()
    
    
def vis_json(json_obj, jpg_p):
    colors = [ [255,0,0], [0,255,0], [0,0,255], [255,255,0], [255,0,255], [0,255,255] ]
    alpha = 0.6
    jpg_img = cv2.imread(jpg_p, cv2.IMREAD_COLOR)

    cs = random.choices(colors, k=len(json_obj))
    masks = []
    for idx, instance in enumerate(json_obj):
        mask = instance['segmentation']
        mask = mask_utils.decode(mask)

        output = np.zeros(jpg_img.shape)
        overlay = np.zeros(jpg_img.shape)
        overlay[:] = cs[idx]
        x, y = np.where(mask == 1)
        for x, y in zip(x,y): output[x,y] = overlay[x,y]

        vis = jpg_img.copy()
        cv2.addWeighted(output.astype('uint8'), alpha, vis, 1 - alpha, 0, vis)
        masks.append(vis)
    print(len(masks))
    vis_img_group(masks)
    

def json_name2jpg_name(json_file):
    jpg_dir = '../data/UTUBE/JPEGImages/'
    img_file = os.path.join(json_file.split('/')[-2], json_file.split('/')[-1])
    return os.path.join(jpg_dir, img_file.replace('.json','.jpg'))