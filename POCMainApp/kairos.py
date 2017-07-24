from kairos_face import recognize



image_path = "/Users/erenhukumdar/Projects/Pepper/logs/myfriend.jpg"
response = recognize.recognize_face(file=image_path, gallery_name='pepper-friends')
print(response)
