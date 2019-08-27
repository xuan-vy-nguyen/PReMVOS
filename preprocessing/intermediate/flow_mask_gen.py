import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt
import cv2
TAG_FLOAT = 202021.25 # Magic number from source code


#Becareful, script only test on binary mask
#Therefore, when use this script, you should convert mask to binary
#Example in last.

def read_flow(filename):
    """
    Read a .flo file.
    Parameters
    ----------
    filename : str
        Filename to read flow from. Must have extension .flo.
    Returns
    -------
    flow : ndarray, shape (height, width, 2)
        U and V vector components of flow.
    """
    ext = os.path.splitext(filename)[1]
    if ext != '.flo':
        quit('extension .flo expected')

    with open(filename, 'rb') as f:
        tag = np.fromfile(f, np.float32, count=1)[0]
        if tag != TAG_FLOAT:
            quit('invalid .flo file')
        width = np.fromfile(f, np.int32, 1)[0]
        height = np.fromfile(f, np.int32, 1)[0]

        data = np.fromfile(f, np.float32, count=2*width*height)
        flow = np.resize(data, (height, width, 2))

    return flow


def create_next_mask(mask, flow, obj_ids=[1]):
    '''
    Create mask from flow
        mask: (h, w) -> mask[x, y] = k -> have object k as pixel x, y
        flow: (h, w, 2)
        obj_ids: List of object id to move
    '''
    if isinstance(obj_ids, int):
        obj_ids = [obj_ids]
    print(flow.shape)
    new_mask = np.zeros_like(mask)
    for obj_id in obj_ids:
        mask_index = np.where(mask == obj_id)
        mask_index = np.array(mask_index).transpose()
        for ind in mask_index:
            new_ind = [0, 0]
            new_ind[0] = flow[ind[0], ind[1], 1] + ind[0]
            new_ind[1] = flow[ind[0], ind[1], 0] + ind[1]
            new_mask[int(new_ind[0]), int(new_ind[1])] = obj_id
    return new_mask


def get_bbox_from_mask(mask):
    '''
    Get bounding from mask
        Mask: Binary - only 0 or 1

    '''
    mask_index = np.where(mask > 0 )
    print(mask_index)
    left, right = min(mask_index[0]), max(mask_index[0])
    top, bottom = min(mask_index[1]), max(mask_index[1])

    height = bottom - top
    width = right - left
    return (float(top), float(left), float(height), float(width))


def dilate(mask, kernel_size, iterations):
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size)

    kernel = np.ones(kernel_size)
    dilation = cv2.dilate(mask,kernel,iterations = 1)
    return dilation

def gaussian_blur(mask, kernel_size):
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size)
    #kernel = cv2.getGaussianKernel(5, 0.1)
    #print(kernel)
    blur = cv2.GaussianBlur(mask, kernel_size, 0)
    print((np.floor(blur) == blur).sum() - (blur.shape[0] * blur.shape[1]))
    return blur

if __name__ == '__main__':
    flow = read_flow('00000.flo')
    mask_pil = Image.open('00000.png')
    print(np.array(mask_pil).shape)
    old_mask = np.array(mask_pil)[:, :]
    print('Old mask')
    #plt.imshow(old_mask)
    #plt.show()
    new_mask = create_next_mask(old_mask, flow, obj_ids=[1, 2, 3])
    new_mask = np.array(new_mask, dtype=np.float64)
    new_mask_d = dilate(new_mask, 20, 1)
    #new_mask_g = new_mask_d
    new_mask_g = gaussian_blur(new_mask_d, 11)

    np_frame1 = np.array(Image.open('00001.jpg'), dtype=np.float64)

    for i in range(3):
        np_frame1[:, :, i] *= new_mask_g

    np_frame1 = np.array(np_frame1, dtype=np.int32)
    cv2.imwrite('00001.jpg', np_frame1[:, :, (2, 1, 0)])
    import json
    bbox = get_bbox_from_mask(new_mask_g)
    temp = [{'bbox':bbox, 'score':1.0}]
    json.dump(temp, open('00001.json', 'w'))