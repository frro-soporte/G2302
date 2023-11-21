from kivy.app import App
from kivy.lang import Builder

kv = Builder.load_file("vkeyboard.kv")

class MyApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()