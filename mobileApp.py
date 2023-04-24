# from kivymd.app import MDApp
# from kivy.core.window import Window
# from kivy.lang import Builder
# from kivy.factory import Factory
# from kivy.uix.modalview import ModalView
# from kivy.metrics import dp
# from kivymd.uix.filemanager import MDFileManager
# from kivymd.theming import ThemeManager
# from kivymd.toast import toast
# from kivymd.uix.menu import MDDropdownMenu
# from kivymd.uix.snackbar import Snackbar
#
# Builder.load_string('''
#
#
# <ExampleFileManager@BoxLayout>
#     orientation: 'vertical'
#     spacing: dp(5)
#
#     MDTopAppBar:
#         id: toolbar
#         title: app.title
#         left_action_items: [['menu', lambda x: app.callback(x)]]
#         elevation: 10
#         md_bg_color: app.theme_cls.primary_color
#
#
#     FloatLayout:
#
#         MDRoundFlatIconButton:
#             text: "Open manager"
#             icon: "folder"
#             pos_hint: {'center_x': .5, 'center_y': .6}
#             on_release: app.file_manager_open()
# ''')
#
#
# class Example(MDApp):
#     title = "File Manage"
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         Window.bind(on_keyboard=self.events)
#         self.manager_open = False
#         self.manager = None
#
#     def build(self):
#         menu_items = [
#             {
#                 "viewclass": "OneLineListItem",
#                 "text": f"Item {i}",
#                 "height": dp(56),
#                 "on_release": lambda x=f"Item {i}": self.menu_callback(x),
#             } for i in range(5)
#         ]
#         self.menu = MDDropdownMenu(
#             items=menu_items,
#             width_mult=4,
#         )
#         return Factory.ExampleFileManager()
#
#     def file_manager_open(self):
#         if not self.manager:
#             self.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
#             self.file_manager = MDFileManager(
#                 exit_manager=self.exit_manager, select_path=self.select_path)
#             self.manager.add_widget(self.file_manager)
#             self.file_manager.show('/')  # output manager to the screen
#         self.manager_open = True
#         self.manager.open()
#
#     def select_path(self, path):
#         '''It will be called when you click on the file name
#         or the catalog selection button.
#
#         :type path: str;
#         :param path: path to the selected directory or file;
#         '''
#
#         self.exit_manager()
#         toast(path)
#
#     def exit_manager(self, *args):
#         '''Called when the user reaches the root of the directory tree.'''
#
#         self.manager.dismiss()
#         self.manager_open = False
#
#     def events(self, instance, keyboard, keycode, text, modifiers):
#         '''Called when buttons are pressed on the mobile device..'''
#
#         if keyboard in (1001, 27):
#             if self.manager_open:
#                 self.file_manager.back()
#         return True
#
#     def callback(self, button):
#         self.menu.caller = button
#         self.menu.open()
#
#     def menu_callback(self, text_item):
#         self.menu.dismiss()
#         Snackbar(text=text_item).open()
#
#
# Example().run()

import os
import time

from kivy import platform
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

from test import *

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.images import logo

import xlsxwriter
from datetime import datetime



KV = '''
MDBoxLayout:
    orientation: "vertical"

    MDTopAppBar:
        title: "MDFileManager"
        left_action_items: [['menu', lambda x: app.callback(x)]]
        elevation: 3

    
    
    MDBottomNavigation:
        #panel_color: "#eeeaea"
        selected_color_background: "orange"
        text_color_active: "lightgrey"

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Browse'
            icon: 'home'

            MDFloatLayout:

                MDRoundFlatIconButton:
                    text: "Open manager"
                    icon: "folder"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.file_manager_open()

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Result'
            icon: 'table-account'              
                
            MDBoxLayout:
                orientation: "vertical"
                MDLabel:
                    text: "Custom color"
                    valign: "top"
                    halign: "center"
                    
                ScrollView:
                    MDList:
                        id: table_list
                
            
'''


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.res = []
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Download xlsx",
                "height": dp(56),
                "on_release": lambda x="xlsx": self.menu_callback(x),
            }
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
                )
        return Builder.load_string(KV)

    # def on_start(self, **kwargs):
    #
    #     if platform == "android":
    #         from android.permissions import request_permissions, Permission
    #         request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("C:\\Users\\wedas\\Desktop"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''
        file_name = path.split("\\")[-1]
        file_extation = file_name.split('.')[-1]
        if file_extation in ["jpg", "png", "svg", "jpeg", "ico"]:
            self.res = compare(train_model_by_img(), path)
        elif file_extation in ['egp', 'mp4', 'avi', 'mov']:
            self.res = detect_person_in_video(path, train_model_by_img())
        else:
            self.res.append("Selected file with different extension")
        self.exit_manager()
        self.root.ids.table_list.clear_widgets()
        for i in self.res:
            self.root.ids.table_list.add_widget(
                OneLineListItem(text=i)
            )
        toast("\n".join(self.res))
        # toast(path)



    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        if self.res:
            now = datetime.now()
            current_time = str(now.strftime("%H:%M:%S"))
            workbook = xlsxwriter.Workbook("cheli.xlsx")
            worksheet = workbook.add_worksheet()
            for i in range(len(self.res)):
                worksheet.write(i, 0, self.res[i])

            workbook.close()
        Snackbar(text=text_item).open()


Example().run()


def write_excel(res: list):
    recent_time = time.time()
    file_name = str(datetime.fromtimestamp(recent_time))
    workbook = xlsxwriter.Workbook(f'samara.xlsx')
    worksheet = workbook.add_worksheet()
    for i in range(len(res)):
        worksheet.write(i, 0, res[i])

    workbook.close()

