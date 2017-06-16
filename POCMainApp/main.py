#!/usr/bin/env python

import sys
import qi
import os
# from kairos_face import verify
from kairos_face import enroll
from kairos_face import recognize

class MyFriendApp(object):
    subscriber_list = []
    loaded_topic = ""
    def __init__(self, application):
        # Getting a session that will be reused everywhere
        self.application = application
        self.session = application.session
        self.service_name = self.__class__.__name__

        # Getting a logger. Logs will be in /var/log/naoqi/servicemanager/{application id}.{service name}
        self.logger = qi.Logger(self.service_name)

        # Do some initializations before the service is registered to NAOqi
        self.logger.info("Initializing...")
        # @TODO: insert init functions here

        self.preferences = self.session.service("ALPreferenceManager")
        self.preferences.update()
        self.connect_to_preferences()
        self.create_signals()
        self.logger.info("Initialized!")

    @qi.nobind
    def start_app(self):
        # do something when the service starts
        print "Starting app..."
        # @TODO: insert whatever the app should do to start

        self.show_screen()
        self.start_dialog()
        self.logger.info("Started!")

    @qi.nobind
    def stop_app(self):
        # To be used if internal methods need to stop the service from inside.
        # external NAOqi scripts should use ALServiceManager.stopService if they need to stop it.
        self.logger.info("Stopping service...")
        self.application.stop()
        self.logger.info("Stopped!")

    @qi.nobind
    def cleanup(self):
        # called when your module is stopped
        self.logger.info("Cleaning...")
        # @TODO: insert cleaning functions here
        self.disconnect_signals()
        self.stop_dialog()
        self.hide_screen()
        self.logger.info("Cleaned!")
        try:
            self.audio.stopMicrophonesRecording()
        except Exception, e:
            self.logger.info("microphone already closed")

    @qi.nobind
    def connect_to_preferences(self):
        # connects to cloud preferences library and gets the initial prefs
        try:

            self.gallery_name = self.preferences.getValue('my_friend', "gallery_name")
            self.folder_path = self.preferences.getValue('my_friend', "folder_path")
            self.logger.info(self.folder_path)
            self.threshold = float(str(self.preferences.getValue('my_friend', "threshold")))

            self.logger.info(self.threshold)
            self.record_folder = self.preferences.getValue('my_friend', "record_folder")
            self.photo_count = int(self.preferences.getValue('my_friend', "photo_count"))
            self.resolution = int(self.preferences.getValue('my_friend', "resolution"))
            print(self.resolution)
            self.camera_id = int(self.preferences.getValue('my_friend', "camera_id"))
            self.picture_format = self.preferences.getValue('my_friend', "picture_format")
            self.file_name = self.preferences.getValue('my_friend', "file_name")
        except Exception, e:
            self.logger.info("failed to get preferences".format(e))
        self.logger.info("Successfully connected to preferences system")

    @qi.nobind
    def create_signals(self):
        self.logger.info("Creating ColorChosen event...")
        # When you can, prefer qi.Signals instead of ALMemory events
        memory = self.session.service("ALMemory")

        # self.subscriber = self.memory.subscriber("FaceDetected")
        # self.subscriber.signal.connect(self.on_human_tracked)
        #
        event_name = "UserSession/FocusedUser"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.catch_face)
        # event_connection = event_subscriber.signal.connect(self.on_speech_faq_input)
        self.subscriber_list.append([event_subscriber, event_connection])
        #
        # event_name = "CM/StopCoffeeMaker"
        # memory.declareEvent(event_name)
        # event_subscriber = memory.subscriber(event_name)
        # event_connection = event_subscriber.signal.connect(self.stop_coffee_maker)
        # # event_connection = event_subscriber.signal.connect(self.on_speech_faq_input)
        # self.subscriber_list.append([event_subscriber, event_connection])

        self.logger.info("Event created!")

    @qi.nobind
    def disconnect_signals(self):
        self.logger.info("Unsubscribing to all events...")
        for sub, i in self.subscriber_list:
            try:
                sub.signal.disconnect(i)
            except Exception, e:
                self.logger.info("Error unsubscribing: {}".format(e))
        self.logger.info("Unsubscribe done!")

    @qi.nobind
    def start_dialog(self):
        self.logger.info("Loading dialog")
        dialog = self.session.service("ALDialog")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        topic_path = os.path.realpath(os.path.join(dir_path, "myfriend", "myfriend_enu.top"))
        self.logger.info("File is: {}".format(topic_path))
        try:
            self.loaded_topic = dialog.loadTopic(topic_path)
            dialog.activateTopic(self.loaded_topic)
            dialog.subscribe(self.service_name)
            self.logger.info("Dialog loaded!")
            # dialog.gotoTag("cmStart", "CM")
            self.logger.info('tag has been located')
        except Exception, e:
            self.logger.info("Error while loading dialog: {}".format(e))

    @qi.nobind
    def stop_dialog(self):
        self.logger.info("Unloading dialog")
        try:
            dialog = self.session.service("ALDialog")
            dialog.unsubscribe(self.service_name)
            dialog.deactivateTopic(self.loaded_topic)
            dialog.unloadTopic(self.loaded_topic)
            self.logger.info("Dialog unloaded!")
        except Exception, e:
            self.logger.info("Error while unloading dialog: {}".format(e))

    @qi.nobind
    def show_screen(self):
        folder = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        self.logger.info("Loading tablet page for app: {}".format(folder))
        try:
            self.ts = self.session.service("ALTabletService")
            self.ts.loadApplication(folder)
            self.ts.showWebview()
            self.logger.info("Tablet loaded!")
        except Exception, e:
            self.logger.info("Error while loading tablet: {}".format(e))

    @qi.nobind
    def hide_screen(self):
        self.logger.info("Unloading tablet...")
        try:
            tablet = self.session.service("ALTabletService")
            tablet.hideWebview()
            self.logger.info("Tablet unloaded!")
        except Exception, e:
            self.logger.info("Error while unloading tablet: {}".format(e))

    @qi.bind(methodName="registerFace", paramsType=(qi.String, qi.String, ), returnType=qi.Bool)
    def register_face(self, customer_id, picture_name):
        try:
            file_path = self.get_picture_path(picture_name)
            response = enroll.enroll_face(subject_id=customer_id, gallery_name=self.gallery_name, file=file_path)
            self.logger.info(response)
            return True
        except Exception, e:
            self.logger.error(e);
            return False

    @qi.nobind
    def get_picture_path(self, picture_name):
        image_path = self.folder_path + picture_name
        return image_path

    @qi.nobind
    def take_picture(self):
        life_service = self.session.service("ALAutonomousLife")
        life_service.setAutonomousAbilityEnabled("BasicAwareness", False)
        self.logger.info('taking picture')
        camera = self.session.service("ALPhotoCapture")
        camera.setResolution(self.resolution)
        camera.setCameraID(self.camera_id)
        camera.setPictureFormat(self.picture_format)
        camera.setHalfPressEnabled(True)
        camera.takePictures(self.photo_count, self.record_folder, self.file_name)
        life_service = self.session.service("ALAutonomousLife")
        life_service.setAutonomousAbilityEnabled("BasicAwareness", True)

    @qi.bind(methodName="recognizeFace", paramsType=(qi.String, ), returnType=qi.Void)
    def recognize_face(self, picture_name):
        self.logger.info('face recognition is working')
        image_path = self.get_picture_path(picture_name)
        try:
            response = recognize.recognize_face(file=image_path, gallery_name=self.gallery_name)
            print(response)
            status = response['images'][0]['transaction']['status']
            if status != 'failure':
                confidence = float(response['images'][0]['transaction']['confidence'])
                if confidence > self.threshold:
                    customer_id = response['images'][0]['transaction']['subject_id']
                    result = customer_id
                else:
                    result = 'low_confidence'
            else:
                result = 'failure'

            self.logger.info(result)
        except Exception, e:
            self.logger.error(e)
            result = 'failure'
        memory = self.session.service("ALMemory")
        memory.raiseEvent("MyFriend/Result", result)

    @qi.nobind
    def catch_face(self, value):
        self.logger.info('event raised')
        if value > 0:
            self.take_picture()
            self.recognize_face(self.file_name)



if __name__ == "__main__":
    # with this you can run the script for tests on remote robots
    # run : python main.py --qi-url 123.123.123.123
    app = qi.Application(sys.argv)
    app.start()
    service_instance = MyFriendApp(app)
    service_id = app.session.registerService(service_instance.service_name, service_instance)
    service_instance.start_app()
    app.run()
    service_instance.cleanup()
    app.session.unregisterService(service_id)
