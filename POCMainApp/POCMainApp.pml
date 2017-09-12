<?xml version="1.0" encoding="UTF-8" ?>
<Package name="POCMainApp" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="main_behavior" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="come_behavior" xar="behavior.xar" />
        <BehaviorDescription name="behavior" src="empty" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs>
        <Dialog name="myfriend" src="myfriend/myfriend.dlg" />
        <Dialog name="come_closer" src="come_closer/come_closer.dlg" />
        <Dialog name="chitchat" src="chitchat/chitchat.dlg" />
    </Dialogs>
    <Resources>
        <File name="main" src="main.py" />
        <File name="kairos" src="kairos.py" />
        <File name="detect" src="kairos_face/detect.py" />
        <File name="enroll" src="kairos_face/enroll.py" />
        <File name="entities" src="kairos_face/entities.py" />
        <File name="exceptions" src="kairos_face/exceptions.py" />
        <File name="gallery" src="kairos_face/gallery.py" />
        <File name="recognize" src="kairos_face/recognize.py" />
        <File name="remove" src="kairos_face/remove.py" />
        <File name="settings" src="kairos_face/settings.py" />
        <File name="utils" src="kairos_face/utils.py" />
        <File name="verify" src="kairos_face/verify.py" />
        <File name="customerquery" src="customerquery.py" />
        <File name="__init__" src="kairos_face/__init__.py" />
        <File name="pepper" src="html/css/pepper.css" />
        <File name="jquery-2.1.4.min" src="html/js/jquery-2.1.4.min.js" />
        <File name="main" src="html/js/main.js" />
        <File name="qimessaging_helper" src="html/js/qimessaging_helper.js" />
        <File name="pepper" src="html copy/css/pepper.css" />
        <File name="baloon" src="html copy/images/baloon.jpg" />
        <File name="faq" src="html copy/images/faq.png" />
        <File name="logo" src="html copy/images/logo.png" />
        <File name="logo_big1" src="html copy/images/logo_big1.jpg" />
        <File name="logo_big_blue" src="html copy/images/logo_big_blue.jpg" />
        <File name="qmatic" src="html copy/images/qmatic.png" />
        <File name="training" src="html copy/images/training.png" />
        <File name="index" src="html copy/index.html" />
        <File name="jquery-2.1.4.min" src="html copy/js/jquery-2.1.4.min.js" />
        <File name="main" src="html copy/js/main.js" />
        <File name="qimessaging_helper" src="html copy/js/qimessaging_helper.js" />
        <File name="main" src="html/css/main.css" />
        <File name="assistant" src="html/img/assistant.png" />
        <File name="baloon" src="html/img/baloon.jpg" />
        <File name="bg" src="html/img/bg.png" />
        <File name="buttonsBg" src="html/img/buttonsBg.png" />
        <File name="faq" src="html/img/faq.png" />
        <File name="guide" src="html/img/guide.png" />
        <File name="kids" src="html/img/kids.png" />
        <File name="leftArrow" src="html/img/leftArrow.png" />
        <File name="logo" src="html/img/logo.png" />
        <File name="logo_big1" src="html/img/logo_big1.jpg" />
        <File name="logo_big_blue" src="html/img/logo_big_blue.jpg" />
        <File name="qmatic" src="html/img/qmatic.png" />
        <File name="rightArrow" src="html/img/rightArrow.png" />
        <File name="selfie" src="html/img/selfie.png" />
        <File name="training" src="html/img/training.png" />
        <File name="index" src="html/index.html" />
        <File name="ball" src="html/img/ball.png" />
        <File name="bgKids" src="html/img/bgKids.png" />
        <File name="car" src="html/img/car.png" />
        <File name="game" src="html/img/game.png" />
        <File name="plane" src="html/img/plane.png" />
        <File name="rocket" src="html/img/rocket.png" />
        <File name="safe" src="html/img/safe.png" />
        <File name="spinner" src="html/img/spinner.png" />
        <File name="train" src="html/img/train.png" />
    </Resources>
    <Topics>
        <Topic name="myfriend_enu" src="myfriend/myfriend_enu.top" topicName="myfriend" language="en_US" />
        <Topic name="come_closer_enu" src="come_closer/come_closer_enu.top" topicName="come_closer" language="en_US" />
        <Topic name="chitchat_enu" src="chitchat/chitchat_enu.top" topicName="chitchat" language="en_US" />
    </Topics>
    <IgnoredPaths />
    <Translations auto-fill="en_US">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
    </Translations>
</Package>
