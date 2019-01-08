"""This Clas
s is used to control and create the Windows for dispaying Videos with OpenCV"""
import cv2


class WindowManger:
    def __init__(self, name, keypressCallback=None):
        self.keypressCallback = keypressCallback

        self._windowName = name
        self._isWindowCreated = False

    @property
    def get_isWindowCreated(self):
        return self._isWindowCreated

    def create_window(self):
        cv2.namedWindow(self._windowName())
        self._isWindowCreated = True

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroy_window(self):
        cv2.destroyWindow(self._windowName)

    @staticmethod
    def destroy_all_windows():
        cv2.destroyAllWindows()

    def processEvents(self):
        keycode = cv2.waitKey(1)

        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ASCII info encoded by GTK.
            keycode &= 0xFF
            self.keypressCallback(keycode)
        