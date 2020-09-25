"""
Utility functions to resize the frame from the video or normal image into specified width the increase the
processing speed on the operations on the frames.
"""

import cv2


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    Resize the image according the width with open cv's Interpolator. Height is automatically
    calculated based on the ratio of the original width of the frame

    Parameters
    ----------
    image : numpy array
        input image original from input video
    width : int
        width of the output frame
    height : int , optional
        the height is automatically calculated based on the ratios
    inter : int
        Interpolator to use

    Returns
    -------
    resized : numpy array
        output resized image
    """
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized
