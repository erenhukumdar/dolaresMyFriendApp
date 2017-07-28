#!/usr/bin/env python

import sys
import qi
from threading import Thread
import os

# from kairos_face import verify
from kairos_face import enroll
from kairos_face import recognize
from kairos_face import detect
from datetime import datetime
from customerquery import CustomerQuery


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
        self.create_signals()
        self.preferences = self.session.service("ALPreferenceManager")
        self.preferences.update()
        self.connect_to_preferences()
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
        self.stop_dialog()
        self.hide_screen()
        self.disconnect_signals()
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

            self.camera_id = int(self.preferences.getValue('my_friend', "camera_id"))
            self.picture_format = self.preferences.getValue('my_friend', "picture_format")
            self.file_name = self.preferences.getValue('my_friend', "file_name")

            self.faq_app_id	= self.preferences.getValue('global_variables', 'faq_app_id')
            self.training_app_id = self.preferences.getValue('global_variables', 'training_app_id')
            self.pair_app_id = self.preferences.getValue('global_variables', 'pair_app_id')
            self.auth_launcher_id = self.preferences.getValue('global_variables', 'auth_launcher_id')
            self.qmatic_app_id = self.preferences.getValue('global_variables', 'qmatic_app_id')
            self.game_app = self.preferences.getValue('global_variables', 'game_app')
            self.selfie_app = self.preferences.getValue('global_variables', 'selfie_app')
            self.safe_app = self.preferences.getValue('global_variables', 'safe_app')
            self.come_here_app = self.preferences.getValue('global_variables', 'come_here_app')
            self.empty_app_id = self.preferences.getValue('global_variables', 'empty_app_id')
            self.age_limit = int(self.preferences.getValue('my_friend', 'age_limit'))
            self.finie_app = self.preferences.getValue('global_variables', 'finie_app')
            self.picture_path = self.preferences.getValue('my_friend', 'picture_path')

        except Exception, e:
            self.logger.info("failed to get preferences".format(e))
        self.logger.info("Successfully connected to preferences system")

    @qi.nobind
    def create_signals(self):
        self.logger.info("Creating ColorChosen event...")
        # When you can, prefer qi.Signals instead of ALMemory events
        memory = self.session.service("ALMemory")

        # event_name = "MyFriend/StartSpeak"
        # memory.declareEvent(event_name)
        # event_subscriber = memory.subscriber(event_name)
        # event_connection = event_subscriber.signal.connect(self.catch_face)
        # self.subscriber_list.append([event_subscriber, event_connection])

        event_name = "MyFriend/ChosenApp"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.launch_app)
        self.subscriber_list.append([event_subscriber, event_connection])

        event_name = "MyFriend/CheckMemory"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.check_memory)
        self.subscriber_list.append([event_subscriber, event_connection])

        event_name = "MyFriend/Rest"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.rest_mode)
        self.subscriber_list.append([event_subscriber, event_connection])

        event_name = "MyFriend/Exit"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.return_to_idle)
        self.subscriber_list.append([event_subscriber, event_connection])

        event_name = "MyFriend/RunWithAuth"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.run_with_auth)
        self.subscriber_list.append([event_subscriber, event_connection])

        event_name = "MyFriend/RunWithoutAuth"
        memory.declareEvent(event_name)
        event_subscriber = memory.subscriber(event_name)
        event_connection = event_subscriber.signal.connect(self.run_without_auth)
        self.subscriber_list.append([event_subscriber, event_connection])

        self.logger.info("Event created!")

    @qi.nobind
    def disconnect_signals(self):
        self.logger.info("Unsubscribing to all events...")
        for sub, i in self.subscriber_list:
            try:
                sub.signal.disconnect(i)
            except Exception, e:
                self.logger.info(e)
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
            dialog.gotoTag(self.locate_dialog_tag(), "myfriend")
            self.logger.info('tag has been located')
        except Exception, e:
            self.logger.info("Error while loading dialog: {}".format(e))

    @qi.nobind
    def locate_dialog_tag(self):
        auto_life = self.session.service("ALAutonomousLife")
        app_list = auto_life.getFocusHistory(2)
        previous_app = app_list[0][0]
        self.logger.info('previous app:'+previous_app)
        if (previous_app != self.come_here_app) and (previous_app != self.empty_app_id) and (previous_app != ''):
            return 'helloAgain'
        else:
            self.catch_face(1)
            return 'firstGreet'


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

    @qi.nobind
    def take_picture(self):
        self.logger.info(str(datetime.now()) + 'take picture start')
        life_service = self.session.service("ALAutonomousLife")
        life_service.setAutonomousAbilityEnabled("BasicAwareness", False)
        camera = self.session.service("ALPhotoCapture")
        camera.setResolution(self.resolution)
        camera.setCameraID(self.camera_id)
        camera.setPictureFormat(self.picture_format)
        camera.setHalfPressEnabled(True)
        camera.takePictures(self.photo_count, self.record_folder, self.file_name)
        life_service = self.session.service("ALAutonomousLife")
        life_service.setAutonomousAbilityEnabled("BasicAwareness", True)
        self.logger.info(str(datetime.now()) + 'take picture finished')

    @qi.bind(methodName="recognizeFace", paramsType=(qi.String, ), returnType=qi.Void)
    def recognize_face(self, value):
        memory = self.session.service('ALMemory')
        try:
            memory.removeData('Global/CurrentCustomer')
            self.logger.info("clearing the memory")
        except Exception, e:
            self.logger.info('exception while erasing memory')
            self.logger.error(e)

        self.logger.info(str(datetime.now()) + 'recognize started')
        image_path = self.picture_path

        # creating new thread for checking if the speaker is a kid or an adult

        thread = Thread(target=self.verify_face, args=(1,))
        thread.start()

        try:
            self.logger.info('new thread creating has been started')
        except Exception, e:
            self.logger.error(e)

        try:
            self.logger.info(str(datetime.now()) + 'request sent')
            response = recognize.recognize_face(file=image_path, gallery_name=self.gallery_name)
            self.logger.info('Response:'+str(response))
            self.logger.info(str(datetime.now()) + 'response arrived')
            status = response['images'][0]['transaction']['status']
            if status != 'failure':
                confidence = float(response['images'][0]['transaction']['confidence'])
                if confidence > self.threshold:
                    customer_id = response['images'][0]['transaction']['subject_id']
                    if customer_id != "":
                        self.logger.info("customer info:"+customer_id)
                        customer = CustomerQuery()
                        customer.query_customer(customer_id, "U")
                        result = customer.name + " " + customer.last_name
                        self.logger.info("known person detected:" + result)
                        memory.insertData("Global/CurrentCustomer", str(customer.jsonify()))
                    else:
                        self.logger.info('no customer')
                        result = 'failure'
                else:
                    result = 'low_confidence'
            else:
                result = 'failure'
            self.logger.info(result)
        except Exception, e:
            self.logger.error(e)
            result = 'failure'

        memory = self.session.service("ALMemory")
        memory.raiseEvent("MyFriend/FinishTime", str(datetime.now()))

    @qi.nobind
    def verify_face(self, value):
        memory = self.session.service('ALMemory')
        try:
            memory.removeData('MyFriend/VerifiedAge')
        except Exception, e:
            self.logger.error(e)

        try:
            picture_path = self.picture_path
            self.logger.info('verify face has been worked')
            self.logger.info(picture_path)
            response = detect.detect_face(file=picture_path)
            self.logger.info('Response:' + str(response))
            self.logger.info(str(datetime.now()) + 'response arrived')
            age = int(response['images'][0]['faces'][0]['attributes']['age'])
            self.logger.info("age=" + str(age))
            memory.raiseEvent('MyFriend/VerifiedAge', age)
        except Exception, e:
            self.logger.error(e)

    @qi.nobind
    def enroll_face(self, value):

        try:
            picture_path = self.picture_path
            self.logger.info('enroll known face has been worked')
            self.logger.info(picture_path)
            response = enroll.enroll_face(file=picture_path, gallery_name=self.gallery_name, subject_id=value)
            self.logger.info('Response:' + str(response))
            self.logger.info(str(datetime.now()) + 'response arrived')
            status = response['images'][0]['transaction']['status']
            self.logger.info('response status='+status)

        except Exception, e:
            self.logger.error(e)

    @qi.nobind
    def catch_face(self, value):
        self.logger.info('catch face event raised value'+str(value))
        if value > 0:
            memory = self.session.service("ALMemory")
            memory.raiseEvent("MyFriend/StartSpeak", 1)
            self.logger.info(str(datetime.now()) + 'catch face event raised')
            self.take_picture()
            self.recognize_face(self.file_name)

    @qi.nobind
    def check_memory(self, value):
        if value > 0:
            try:
                memory = self.session.service('ALMemory')
                customer_info = CustomerQuery()
                customer_info.fromjson(memory.getData("Global/CurrentCustomer"))
                self.logger.info("customer no:"+customer_info.customer_number)
            except Exception, e:
                self.logger.error(e)
                customer_info = ''
            if customer_info != '':

                thread = Thread(target=self.enroll_face, args=(customer_info.customer_number,))
                thread.start()
                memory = self.session.service("ALMemory")
                memory.raiseEvent("MyFriend/LauncherForAdultKnown", customer_info.name)
            else:
                try:
                    age = int(memory.getData('MyFriend/VerifiedAge'))
                    if age > self.age_limit:
                        memory.raiseEvent("MyFriend/LauncherForAdultUnknown", 1)
                    else:
                        memory.raiseEvent("MyFriend/LauncherForKids", 1)
                except Exception, e:
                    self.logger.error(e)
                    memory.raiseEvent("MyFriend/LauncherForAdultUnknown", 1)

    @qi.nobind
    def launch_app(self, value):
        self.logger.info('launching application' + str(value))
        memory = self.session.service('ALMemory')
        customer_info = CustomerQuery()
        try:
            customer_info.fromjson(memory.getData("Global/CurrentCustomer"))
        except Exception, e:
            self.logger.error(e)

        try:

            autonomous_life = self.session.service('ALAutonomousLife')
            choices = {'0': (self.empty_app_id, self.empty_app_id, 1), '1': (self.faq_app_id, self.faq_app_id, 1), '2': (self.training_app_id, self.training_app_id, 1), '3': (self.auth_launcher_id, self.qmatic_app_id, 0), '4': (self.game_app, self.game_app, 1), '5': (self.selfie_app, self.selfie_app, 1), '6': (self.safe_app, self.safe_app, 1), '7': (self.auth_launcher_id, self.finie_app, 1)}
            (app_id, redirect_app_id, require) = choices.get(value, ('error', 'error', 'error'))

            self.logger.info('app id' + app_id)
            if customer_info.customer_number == '':
                if require == 1:
                    memory.insertData('Global/RedirectingApp', redirect_app_id)
                    self.logger.info('focusing to:' + app_id)
                    self.cleanup()
                    autonomous_life.switchFocus(app_id)
                elif require == 0:
                    memory.insertData('Global/RedirectingApp', redirect_app_id)
                    memory.raiseEvent('MyFriend/GetConfirmation', redirect_app_id)
            else:
                self.logger.info('focusing to:' + redirect_app_id)
                self.cleanup()
                autonomous_life.switchFocus(redirect_app_id)

        except Exception, e:
            self.logger.error(e)
            memory = self.session.service('ALMemory')
            memory.raiseEvent('MyFriend/ExecutionError', 1)
            self.logger.info('error event raised')

    @qi.nobind
    def rest_mode(self, value):
        self.logger.info("rest position")
        # motion = self.session.service('ALMotion')
        # motion.rest()


    @qi.nobind
    def run_with_auth(self, value):
        self.cleanup()
        autonomous_life = self.session.service('ALAutonomousLife')
        autonomous_life.switchFocus(self.auth_launcher_id)

    @qi.nobind
    def run_without_auth(self, value):
        self.cleanup()
        autonomous_life = self.session.service('ALAutonomousLife')
        autonomous_life.switchFocus(value)

    @qi.nobind
    def return_to_idle(self, value):
        self.memory_cleanup
        self.launch_app("0")

    @qi.nobind
    def memory_cleanup(self):
        memory = self.session.service('ALMemory')
        try:
           memory.removeData("Global/CurrentCustomer")
        except Exception, e:
            self.logger.error(e)
        try:
           memory.removeData("Global/RedirectingApp")
        except Exception, e:
            self.logger.error(e)
        try:
           memory.removeData("Global/QueueData")
        except Exception, e:
            self.logger.error(e)
        try:
           memory.removeData("Global/RedirectingApp")
        except Exception, e:
            self.logger.error(e)

        try:
            memory.removeData("MyFriend/VerifiedAge")
            memory.removeData("MyFriend/LauncherForAdultKnown")
        except Exception, e:
            self.logger.error(e)

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
