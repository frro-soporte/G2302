from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
import cv2, numpy,  os, time
from kivy.utils import get_color_from_hex
from kivy.uix.modalview import ModalView
import mediapipe as mp
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.core.window import Window
import ctypes 

FOLDER = 'docs/'

# --- this changes the app's default background --- #
Window.clearcolor = (0, 0.6, 0.1, .5)
Window.size = (750, 400)

class AuthScreen(Screen):
    def __init__(self, **kwargs):
        super(AuthScreen, self).__init__(**kwargs)
        self.username = None
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Si no tiene una cuenta creada, deberia crea una antes de iniciar sesion', font_size='20sp', text_size=(900, None), markup=True)
        self.layout.add_widget(self.label)

        self.btnSignIn = Button(text='Login', font_size='20sp',background_color=get_color_from_hex('#719159'))
        self.btnSignIn.bind(on_press=self.SignIn)

        self.btnSignUp = Button(text='Crear cuenta', font_size='20sp',background_color=get_color_from_hex('#45612f'))
        self.btnSignUp.bind(on_press=self.goToSignUp)

        self.layout.add_widget(self.btnSignIn)
        self.layout.add_widget(self.btnSignUp)

        self.add_widget(self.layout)

    def goToSignUp(self, instance):
        self.manager.current = 'RegisterScreen'

    def SignIn(self,instance):
        haar_file = 'haarcascade_frontalface_default.xml'
        datasets = 'faces'
        
        print('Training classifier...')
        # Create a list of images and a list of corresponding names along with a unique id
        (images, labels, names, id) = ([], [], {}, 0)
        isCreateAccount = False
        for (subdirs, dirs, files) in os.walk(datasets):
            for subdir in dirs:
            # the person's name is the name of the sub_dataset created using the create_data.py file
                names[id] = subdir
                subjectpath = os.path.join(datasets, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    label = id
                    images.append(cv2.imread(path, 0))
                    labels.append(int(label))
                    isCreateAccount = True
                id += 1
        if isCreateAccount:        
            (width, height) = (130, 100)
        else:
            ctypes.windll.user32.MessageBoxW(0, "Se debe crear una cuenta antes de login", "Error", 1)
            return

        # https://www.life2coding.com/drawing-fancy-round-rectangle-using-opencv-python/
        def rounded_rectangle(img, pt1, pt2, color, thickness, r, d):
            x1,y1 = pt1
            x2,y2 = pt2
        
            # Top left
            cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
            cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
            cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
        
            # Top right
            cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
            cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
            cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
        
            # Bottom left
            cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
            cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
            cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
        
            # Bottom right
            cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
            cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
            cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

        # Create a numpy array from the lists above
        (images, labels) = [numpy.array(lists) for lists in [images, labels]]

        # OpenCV trains a model from the images using the Local Binary Patterns algorithm
        # model = cv2.face.LBPHFaceRecognizer_create()
        # model = cv2.face_LBPHFaceRecognizer.create()
        model = cv2.face.LBPHFaceRecognizer_create()
        # train the LBP algorithm on the images and labels we provided above
        model.train(images, labels)

        face_cascade = cv2.CascadeClassifier(haar_file)
        webcam = cv2.VideoCapture(0)
       
        while True:
            (_, im) = webcam.read()
            # validate if exist a image
            if im is None:
                print("No se encontró ninguna imagen")
                break
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            # detect faces using the haar_cacade file
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                # colour = bgr format
            # draw a rectangle around the face and resizing/ grayscaling it
            # uses the same method as in the create_data.py file
                # cv2.rectangle(im,(x,y),(x + w,y + h),(0, 255, 255),2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                # try to recognize the face(s) using the resized faces we made above
                prediction = model.predict(face_resize)
                rounded_rectangle(im, (x, y), (x + w, y + h), (0, 255, 255), 2, 15, 30)
                # if face is recognized, display the corresponding name
                if prediction[1] < 74:
                    cv2.putText(im,'%s' % (names[prediction[0]].strip()),(x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN,1.5,(20,185,20), 2)
                    # print the confidence level with the person's name to standard output
                    confidence = (prediction[1]) if prediction[1] <= 100.0 else 100.0
                    print("Persona pronosticada: {}, confianza: {}%".format(names[prediction[0]].strip(), round((confidence / 74.5) * 100, 2)))
                    # cv2.putText(im,'SUCCESS',(x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN,1.5,(65,65, 255), 2)
                    # time.sleep(1)
                    # break
                    # close the webcam and all open windows   
                    OpenCvApp.currentUser = names[prediction[0]]
                    self.manager.get_screen('home').username = names[prediction[0]]
                    self.manager.current = 'home'                 
                    # webcam.release()
                    # cv2.destroyAllWindows()
                    break
                # if face is unknown (if classifier is not trained on this face), show 'Unknown' text...
                else:
                    cv2.putText(im,'Desconocido',(x + 5, (y + 25) + h), cv2.FONT_HERSHEY_PLAIN,1.5,(65,65, 255), 2)
                    print("Persona pronosticada: Desconocido")

            # show window and set the window title
            cv2.imshow('Reconocimiento facial OpenCV -  esc para cerrar', im)
            key = cv2.waitKey(10)
            # esc to quit applet
            if key == 27:
                break

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.txtInput = TextInput(text='', multiline=False)

        self.btnSignUp = Button(text='Registrarse',background_color=get_color_from_hex('#a90061'))
        self.btnSignUp.bind(on_press=self.register)

        self.btnBack = Button(text='Volver al inicio de sesion',background_color=get_color_from_hex('#222531'))
        self.btnBack.bind(on_press=self.back)
        
        self.layout.add_widget(self.txtInput)
        self.layout.add_widget(self.btnSignUp)
        self.layout.add_widget(self.btnBack)

        self.add_widget(self.layout)

    def back(self, instance):
        self.manager.current = 'auth'
    
    def register(self,instance):
        if self.txtInput.text == '':
            self.modal_label = Label(text="Por favor ingrese un nombre")
            self.modal_layout = BoxLayout(orientation='vertical')
            self.modal_view = ModalView(size_hint=(None, None), size=(500, 200))
            self.dismiss_button = Button(text="Ok")
            self.dismiss_button.bind(on_release=self.modal_view.dismiss)

            self.modal_layout.add_widget(self.modal_label)
            self.modal_layout.add_widget(self.dismiss_button)

            self.modal_view.add_widget(self.modal_layout)
            self.modal_view.open()
            return
        
        haar_file = 'haarcascade_frontalface_default.xml'
        datasets = 'faces'
        sub_dataset = self.txtInput.text

        path = os.path.join(datasets, sub_dataset)
        if not os.path.isdir(path):
            os.mkdir(path)

        (width, height) = (130, 100)

        face_cascade = cv2.CascadeClassifier(haar_file)
        webcam = cv2.VideoCapture(0)
        print("Webcam is open? ", webcam.isOpened())
        time.sleep(2)
        count = 1
        print("START TAKING PICS...")
        while count < 101:
            ret_val, im = webcam.read()
            if ret_val == True:
                if im is not None:
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                else:
                    print("No image found")
                    break
                faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                for (x,y,w,h) in faces:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    face = gray[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    cv2.imwrite('%s/%s.png' % (path,count), face_resize)
                count += 1
                cv2.imshow('OpenCV', im)
                key = cv2.waitKey(20)
                if key == 27:
                    break
        OpenCvApp.currentUser = self.txtInput.text
        self.txtInput.text = ''
        self.manager.get_screen('home').username = self.txtInput.text
        self.manager.current = 'home'
        self.modal_label = Label(text="Cuenta creada con exito")
        self.modal_layout = BoxLayout(orientation='vertical')
        self.modal_view = ModalView(size_hint=(None, None), size=(500, 200))
        self.dismiss_button = Button(text="Ok")
        self.dismiss_button.bind(on_release=self.modal_view.dismiss)

        self.modal_layout.add_widget(self.modal_label)
        self.modal_layout.add_widget(self.dismiss_button)

        self.modal_view.add_widget(self.modal_layout)
        self.modal_view.open()
        webcam.release()
        cv2.destroyAllWindows()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Bienvenido ' + OpenCvApp.currentUser)
        self.layout.add_widget(self.label)

        self.btnCamara = Button(text='Camara',background_color=get_color_from_hex('#a90061'))
        self.btnCamara.bind(on_press=self.openWebCam)

        self.btnFiles = Button(text='Video y foto',background_color=get_color_from_hex('#a90061'))
        self.btnFiles.bind(on_press=self.getAndShowFiles)

        self.btnLogout = Button(text='Logout',background_color=get_color_from_hex('#222531'))
        self.btnLogout.bind(on_press=self.logout)

        self.layout.add_widget(self.btnCamara)
        self.layout.add_widget(self.btnFiles)
        self.layout.add_widget(self.btnLogout)
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        if OpenCvApp.currentUser== '':
            self.manager.current = 'auth' 
        else:
            self.label.text = 'Bienvenido ' + OpenCvApp.currentUser


    def logout(self, instance):
        OpenCvApp.currentUser = ''
        self.manager.current = 'auth'
    
    def getAndShowFiles(self, instance):
        self.manager.current = 'docs'
    
    def openWebCam(self, instance):
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        pos_left = (50, 50)
        pos_right = (50, 100)
        fuente = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1
        color = (255, 255, 255)

        output_directory = FOLDER + OpenCvApp.currentUser
        os.makedirs(output_directory, exist_ok=True)

        recording = False
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_output = None

        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5) as hands:

            start_time = None
            countdown = 5

            while True:
                ret, frame = cap.read()
                if ret == False:
                    break

                height, width, _ = frame.shape
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                if recording and results.multi_hand_landmarks is None:

                    end_video_time = time.time()
                    video_duration = end_video_time - start_video_time
                    if video_duration >= 2.0:
                        video_output.release()
                        recording = False
                        self.modal_label = Label(text="¡Video guardado y guardado!")
                        self.modal_layout = BoxLayout(orientation='vertical')
                        self.modal_view = ModalView(size_hint=(None, None), size=(500, 200))
                        self.dismiss_button = Button(text="Ok")
                        self.dismiss_button.bind(on_release=self.modal_view.dismiss)

                        self.modal_layout.add_widget(self.modal_label)
                        self.modal_layout.add_widget(self.dismiss_button)

                        self.modal_view.add_widget(self.modal_layout)
                        self.modal_view.open()
                    else:
                        # Borrar el video si dura menos de 2 segundos
                        video_output.release()
                        os.remove(filename)
                        recording = False
                        # print(f"Video borrado porque dura menos de 2 segundos")

                if results.multi_hand_landmarks is not None:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        if handedness.classification[0].label == "Left":
                            if start_time is None:
                                start_time = time.time()

                            elapsed_time = time.time() - start_time
                            remaining_time = countdown - elapsed_time

                            if remaining_time > 0:
                                text = f"Left hand - {int(remaining_time)}s"
                                cv2.putText(frame, text, pos_left, fuente, scale, color, 2)
                            else:
                                filename = os.path.join(output_directory, f"foto_{int(time.time())}.jpg")
                                cv2.imwrite(filename, frame)
                                self.modal_label = Label(text="¡Foto guardada!")
                                self.modal_layout = BoxLayout(orientation='vertical')
                                self.modal_view = ModalView(size_hint=(None, None), size=(500, 200))
                                self.dismiss_button = Button(text="Ok")
                                self.dismiss_button.bind(on_release=self.modal_view.dismiss)

                                self.modal_layout.add_widget(self.modal_label)
                                self.modal_layout.add_widget(self.dismiss_button)

                                self.modal_view.add_widget(self.modal_layout)
                                self.modal_view.open()
                                start_time = None

                        if handedness.classification[0].label == "Right":
                            cv2.putText(frame, "Recording...", pos_right, fuente, scale, color, 2)
                            if not recording:
                                filename = os.path.join(output_directory, f"video_{int(time.time())}.avi")
                                video_output = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
                                recording = True
                                start_video_time = time.time()
                            if recording:
                                video_output.write(frame)
                        # else:
                        if recording and handedness.classification[0].label != "Right":
                            end_video_time = time.time()
                            video_duration = end_video_time - start_video_time
                            if video_duration >= 2.0:
                                video_output.release()
                                recording = False
                                self.modal_label = Label(text="¡Guardando video!")
                                self.modal_layout = BoxLayout(orientation='vertical')
                                self.modal_view = ModalView(size_hint=(None, None), size=(500, 200))
                                self.dismiss_button = Button(text="Ok")
                                self.dismiss_button.bind(on_release=self.modal_view.dismiss)

                                self.modal_layout.add_widget(self.modal_label)
                                self.modal_layout.add_widget(self.dismiss_button)

                                self.modal_view.add_widget(self.modal_layout)
                                self.modal_view.open()                
                            else:
                                video_output.release()
                                os.remove(filename)
                                recording = False

                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()


class DocsScreen(Screen):
    def __init__(self, **kwargs):
        super(DocsScreen, self).__init__(**kwargs)
    
    def on_pre_enter(self):
        if OpenCvApp.currentUser== '':
            self.manager.current = 'auth' 
        else:
            Boxlayout = BoxLayout(orientation='vertical')
            print(OpenCvApp.currentUser)
            print(FOLDER)
            print(os.path.join(FOLDER[:-1], OpenCvApp.currentUser))
            print(FOLDER[:-1])
            _folder = FOLDER + OpenCvApp.currentUser
            print(_folder)

            if not os.path.exists(_folder):
                os.makedirs(_folder)
            docs = os.listdir(_folder)
            print(docs)
            for file_name in docs:
                button = Button(text=file_name, size=(350, 50), size_hint=(1, None))
                path = os.path.join(os.path.join(FOLDER[:-1], OpenCvApp.currentUser), file_name)
                print('path', path)
                extension = file_name.split('.')[-1].lower()
                button.bind(on_press=lambda instance, path=path,ext = extension: self.showFile(path,ext))
                Boxlayout.add_widget(button)

            btnBack = Button(text='Volver',background_color=get_color_from_hex('#222531'))
            btnBack.bind(on_press=self.back)
            Boxlayout.add_widget(btnBack)
            self.add_widget(Boxlayout)

    def back(self, instance):
        self.manager.current = 'home'
    
    def showFile(self, path,ext):
        if(ext == 'jpg' or ext == 'jpeg' or ext == 'png'):
            try:
                image = Image(source=path)
                popup = Popup(title='Imagen', content=image, size_hint=(None, None), size=(400, 400))
                popup.open()
            except Exception as e:
                print("Error", str(e))
        else:
            fullPath = path
            replaceString = fullPath.replace('\\', '/')
            try:
                capture = cv2.VideoCapture(replaceString)
                while True:
                    ret, img = capture.read()
                    if ret:
                        cv2.imshow('video', img)
                    else:
                        break
                    if cv2.waitKey(30) == 27: 
                        break
            except Exception as e:
                print(f"Error: {str(e)}")
            finally:
                capture.release()
                cv2.destroyAllWindows()



class OpenCvApp(App):
    currentUser = 'DEFAULT_NAME'
    def build(self):
        self.title = "Trabajo practico de soporte"
        sm = ScreenManager()
        sm.add_widget(AuthScreen(name='auth'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(DocsScreen(name='docs'))
        sm.add_widget(RegisterScreen(name='RegisterScreen'))
        #sm.current = 'auth'
        return sm


if __name__ == '__main__':
    OpenCvApp().run()
