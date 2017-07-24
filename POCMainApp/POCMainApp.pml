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
        <File name="index" src="html/index.html" />
        <File name="customerquery" src="customerquery.py" />
        <File name="__init__" src="kairos_face/__init__.py" />
        <File name="faq" src="html/images/faq.png" />
        <File name="qmatic" src="html/images/qmatic.png" />
        <File name="training" src="html/images/training.png" />
        <File name="pepper" src="html/css/pepper.css" />
        <File name="logo" src="html/images/logo.png" />
        <File name="jquery-2.1.4.min" src="html/js/jquery-2.1.4.min.js" />
        <File name="main" src="html/js/main.js" />
        <File name="qimessaging_helper" src="html/js/qimessaging_helper.js" />
        <File name="baloon" src="html/images/baloon.jpg" />
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
