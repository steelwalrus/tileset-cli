import cv2
import numpy as np


class Helper:
    """
    Helper class for image operations.
    """

    @staticmethod
    def apply_transparency_mask(image):
        """
        Sets any black pixels to transparent.
        :param image: Image to set transparency
        :type image: numpy.ndarray
        :rtype: numpy.ndarray
        """

        if image.shape[2] == 3:

            b_channel, g_channel, r_channel = cv2.split(image)

            alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255

            image = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

        image[np.all(image == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]

        return image

    @staticmethod
    def scale_image(image, scale):
        """
        Uses nearest neighbour scaling to scale an image by a given scaling factor.
        :param image: Image to scale
        :type image: numpy.ndarray
        :param scale: scale factor to scale image.
        :type scale: float
        :return: Returns resized image
        :rtype: numpy.ndarray
        """
        return cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
