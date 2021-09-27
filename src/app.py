import os
import logging
import threading
import time
import requests
import subprocess
from rtsparty import Stream
from objectdaddy import Daddy


class HalloweenMannequinHead():

    def __init__(self):
        logging.info('Starting application')
        self._setup_stream()
        self._setup_object_recognition()
        self.server_mode = bool(os.environ.get('SERVER_MODE', False))
        if not self.server_mode:
            self._setup_servo()

    def _setup_servo(self):
        """Sets up the servo; requires raspberry pi to run"""
        from servo_controller import ServoController
        self.servo_controller = ServoController()

    def _setup_stream(self):
        """Set up the stream to the camera"""
        logging.info('Starting stream')
        self.stream = Stream(os.environ.get('STREAM_URI', None))

    def _setup_object_recognition(self):
        """Set up object recognition and load models"""
        logging.info('Loading ML models')
        self.daddy = Daddy()

    def get_person_location_x_percentage(self, detection):
        """Returns the person's horizontal location in the frame as a percentage"""
        frame_height, frame_width = detection.frame.shape[:2]
        percentage = round(detection.x / float(frame_width), 2)
        return percentage

    def person_detected(self, detection):
        """Call back for a person being detected"""
        x_percentage = self.get_person_location_x_percentage(detection)
        print('x percentage {}'.format(x_percentage))
        if self.server_mode:
            host = os.environ['RASPBERRY_PI_HOST']
            url = 'http://{}:8000/servo/?p={}'.format(host, x_percentage)
            requests.get(url)
        else:
            self.servo_controller.set_servo_percent(x_percentage)

    def process_frames_from_stream(self):
        """Processes the frames from the stream"""
        while True:
            frame = self.stream.get_frame()
            if self.stream.is_frame_empty(frame):
                continue
            self.latest_frame = frame
            results, frame = self.daddy.process_frame(frame)
            for detection in results:
                if detection.is_person():
                    self.person_detected(detection)
            if self.server_mode:
                time.sleep(0.1)

    def run(self):
        """Run the application"""
        try:
            self.process_frames_from_stream()
        except KeyboardInterrupt:
            logging.info('Exiting application')


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    hmh = HalloweenMannequinHead()
    hmh.run()
