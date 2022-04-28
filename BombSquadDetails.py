# Made By OnurV2.
# You are free to change the code but don't share it.

# ba_meta require api 6
import os
import urllib.request

import ba, _ba
from bastd.ui.settings.allsettings import AllSettingsWindow
from bastd.ui.settings.plugins import PluginSettingsWindow
from bastd.ui.mainmenu import MainMenuWindow
from bastd.ui.settings.advanced import AdvancedSettingsWindow
from bastd.ui.confirm import ConfirmWindow
from bastd.ui.settings.audio import AudioSettingsWindow
from bastd.ui.fileselector import FileSelectorWindow
from bastd.ui.account.settings import AccountSettingsWindow

platform = ba.app.platform
config = ba.app.config
plugin_path = _ba.env()['python_directory_user']
main_path = plugin_path + "/BombSquadDetails/"
audio_settings_detected = False

if not os.path.exists(main_path):
    os.mkdir(main_path)

default_config = {"Leave The Server Directly": False,
                  "End The Game Directly": False,
                  "End The Replay Directly": False,
                  "Exit The Game Directly": False,
                  "Unlock Pro Mode": True,
                  "Show Volume Button": True,
                  "Show The Details Button": True,
                  "Show Exit Game Button": True}
for key in default_config:
    if not key in config:
        config[key] = default_config[key]

class AccountManagerWindow(ba.Window):
    def __init__(self, transition):
        self.uiscale = uiscale = ba.app.ui.uiscale
        self._space = ("\t"*8 if uiscale is ba.UIScale.SMALL else
            "\t"*6 if uiscale is ba.UIScale.MEDIUM else "\t"*7)
        self._account_path = f"{main_path}Accounts"
        self._selected_account = ""

        self._width = width = (1300 if uiscale is ba.UIScale.SMALL else
            900 if uiscale is ba.UIScale.MEDIUM else 1000)
        height = (800 if uiscale is ba.UIScale.SMALL else
            700 if uiscale is ba.UIScale.MEDIUM else 800)
        extra = 300 if uiscale is ba.UIScale.SMALL else 0

        super().__init__(root_widget=ba.containerwidget(
                         size=(width, height),
                         scale=(1.0 if uiscale is ba.UIScale.SMALL else
                            0.80 if uiscale is ba.UIScale.MEDIUM else 0.70),
                         transition=transition))

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         position=(width-width/1.8, height/1.085-extra/5),
                                         text="Accounts",
                                         scale=1.5,
                                         color=(0.83, 1, 0))

        self._add_account_button = ba.buttonwidget(
            parent=self._root_widget,
            button_type="square",
            label="Add This Account",
            position=(height-height/10+extra, height/1.12-extra/4.9),
            size=(200, 75),
            on_activate_call=self._add_account)
        ba.containerwidget(edit=self._root_widget, start_button=self._add_account_button)

        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(300,100),
                                             size=(height/1.3+extra, height-200-extra/5),
                                             highlight=False)
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)

        self._load_accounts()

        self._set_account_button = ba.buttonwidget(
            parent=self._root_widget,
            button_type="square",
            label="Set Account",
            position=(height-height/1.037+extra/15, height/1.55-extra/5),
            size=(250, 150),
            on_activate_call=self._set_account,
            color=(0,0.50,0))

        self._delete_account_button = ba.buttonwidget(
            parent=self._root_widget,
            button_type="square",
            label="Delete Account",
            position=(height-height/1.037+extra/15, height/2.50-extra/5),
            size=(250, 150),
            on_activate_call=self._confirm_delete_account,
            color=(0.80,0.10,0))

        self._account_folder_button = ba.buttonwidget(
            parent=self._root_widget,
            button_type="square",
            label="Account Folder",
            position=(height-height/1.037+extra/15, height/6.50-extra/5),
            size=(250, 150),
            on_activate_call=self._show_account_folder,
            color=(0.80,0.50,0))

        self._back_button = ba.buttonwidget(parent=self._root_widget,
                                            button_type="backSmall",
                                            label=ba.charstr(ba.SpecialChar.BACK),
                                            position=(90, height-85-extra/5),
                                            size=(60, 60),
                                            scale=1.3,
                                            on_activate_call=self._back)
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

    def _load_accounts(self):
        if not os.path.exists(self._account_path):
            os.mkdir(self._account_path)
        try: accounts = os.listdir(self._account_path)
        except Exception:
            ba.screenmessage(message="An unexpected error occurred", color=(1,0,0))
            ba.playsound(ba.getsound("error"))
            return

        for account in accounts:
            if ".bsuuid" in account:
                ba.textwidget(parent=self._subcontainer,
                              text=f"{self._space}{account}",
                              size=(self._width/1.8, 35),
                              scale=1.2,
                              selectable=True,
                              click_activate=True,
                              color=(0,1,1),
                              on_activate_call=ba.Call(self._select_account, account))

    def _add_account(self):
        self._selected_account = ""
        account_id = _ba.get_account_display_string()
        with open(f"{plugin_path[0:-4]}.bsuuid", "r") as file:
            account_code = file.read()
            file.close()
        with open(f"{self._account_path}/{account_id[1:]}.bsuuid", "w") as file:
            file.write(account_code)
            file.close

        ba.screenmessage(f"Account successfully added", color=(0,1,0))
        ba.playsound(ba.getsound("ding"))
        ba.containerwidget(edit=self._root_widget, transition="out_scale")
        AccountManagerWindow(transition="in_scale")

    def _select_account(self, file_name):
        self._selected_account = file_name

    def _set_account(self):
        if self._selected_account:
            with open(f"{self._account_path}/{self._selected_account}", "r") as file:
                account_code = file.read()
                file.close()
            with open(f"{plugin_path[0:-4]}.bsuuid", "w") as file:
                file.write(account_code)
                file.close()

            ba.screenmessage(f"Account set to {self._selected_account}! Please restart the game", color=(0,1,0))
            ba.playsound(ba.getsound("ding"))
            self._selected_account = ""
        else:
            ba.screenmessage(f"Nothing selected!", color=(1,0,0))
            ba.playsound(ba.getsound("error"))

    def _confirm_delete_account(self):
        if self._selected_account:
            ConfirmWindow(text=f"Are you sure you want to delete {self._selected_account}?",
                          action=ba.Call(self._delete_account),
                          ok_text="Yes", cancel_text="No",
                          cancel_is_selected=True)
        else:
            ba.screenmessage(f"Nothing selected!", color=(1,0,0))
            ba.playsound(ba.getsound("error"))

    def _delete_account(self):
        try: os.unlink(f"{self._account_path}/{self._selected_account}")
        except FileNotFoundError: pass
        finally:
            ba.playsound(ba.getsound('shieldDown'))
            ba.containerwidget(edit=self._root_widget, transition="out_scale")
            AccountManagerWindow(transition="in_scale")
            self._selected_account = ""

    def _show_account_folder(self):
        self._selected_account = ""
        folder = os.path.realpath(self._account_path)
        os.startfile(folder)

    def _back(self):
        self._selected_account = ""
        ba.containerwidget(edit=self._root_widget, transition="out_right")
        MainMenuWindow(transition="in_left")

class DetailManagerWindow(ba.Window):
    def __init__(self, transition):
        uiscale = ba.app.ui.uiscale
        width = (1300 if uiscale is ba.UIScale.SMALL else
            900 if uiscale is ba.UIScale.MEDIUM else 1000)
        height = (800 if uiscale is ba.UIScale.SMALL else
            700 if uiscale is ba.UIScale.MEDIUM else 800)
        extra = 300 if uiscale is ba.UIScale.SMALL else 0

        super().__init__(root_widget=ba.containerwidget(
                         size=(width, height),
                         scale=(1.0 if uiscale is ba.UIScale.SMALL else
                            0.80 if uiscale is ba.UIScale.MEDIUM else 0.70),
                         transition=transition))

        self._title_text = ba.textwidget(parent=self._root_widget,
                                         position=(width-width/1.8, height/1.085-extra/5),
                                         text="Details",
                                         scale=1.5,
                                         color=(0.83, 1, 0))

        self._scrollwidget = ba.scrollwidget(parent=self._root_widget,
                                             position=(100,100),
                                             size=(height+extra, height-200-extra/5),
                                             highlight=False)
        self._subcontainer = ba.columnwidget(parent=self._scrollwidget,
                                             selection_loops_to_parent=True)

        ba.textwidget(parent=self._subcontainer,
                      text="Confirmation Preferences",
                      size=(0, 40),
                      scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)

        ba.checkboxwidget(parent=self._subcontainer,
                          text="Don't ask when leaving server",
                          size=(500, 47),
                          scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6,
                          value=config["Leave The Server Directly"],
                          on_value_change_call=ba.Call(self._change_value, "Leave The Server Directly", False))
        
        ba.checkboxwidget(parent=self._subcontainer,
                          text="Don't ask when ending the game",
                          size=(500, 47),
                          value=config["End The Game Directly"],
                          on_value_change_call=ba.Call(self._change_value, "End The Game Directly", False),
                          scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)
        
        ba.checkboxwidget(parent=self._subcontainer,
                          text="Don't ask when ending the replay",
                          size=(500, 47),
                          value=config["End The Replay Directly"],
                          on_value_change_call=ba.Call(self._change_value, "End The Replay Directly", False),
                          scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)

        if platform == "windows" or platform == "linux" or platform == "mac":
            if uiscale is ba.UIScale.LARGE:
                ba.checkboxwidget(parent=self._subcontainer,
                                  text="Don't ask when exiting the game",
                                  size=(500, 47),
                                  value=config["Exit The Game Directly"],
                                  on_value_change_call=ba.Call(self._change_value, "Exit The Game Directly", False),
                                  scale=1.6)

        ba.textwidget(parent=self._subcontainer,
                      text="",
                      size=(0, 40),
                      scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)
        ba.textwidget(parent=self._subcontainer,
                      text="User Preferences",
                      size=(0, 40),
                      scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)

        ba.checkboxwidget(parent=self._subcontainer,
                          text="Unlock pro mode",
                          size=(500, 47),
                          value=config["Unlock Pro Mode"],
                          on_value_change_call=ba.Call(self._change_value, "Unlock Pro Mode", True),
                          scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)

        ba.checkboxwidget(parent=self._subcontainer,
                          text="Show volume button in in-game menu",
                          size=(500, 47),
                          value=config["Show Volume Button"],
                          on_value_change_call=ba.Call(self._change_value, "Show Volume Button", False),
                          scale=1.4 if uiscale is ba.UIScale.MEDIUM else 1.6)

        ba.checkboxwidget(parent=self._subcontainer,
                          text="Show the details button in in-game menu",
                          size=(500, 47),
                          value=config["Show The Details Button"],
                          on_value_change_call=ba.Call(self._change_value, "Show The Details Button", False),
                          scale=(1.6 if uiscale is ba.UIScale.SMALL else
                            1.36 if uiscale is ba.UIScale.MEDIUM else 1.56))

        if platform == "windows" or platform == "linux" or platform == "mac":
            if uiscale is ba.UIScale.LARGE:
                ba.checkboxwidget(parent=self._subcontainer,
                                  text="Show exit game button in in-game menu",
                                  size=(500, 47),
                                  value=config["Show Exit Game Button"],
                                  on_value_change_call=ba.Call(self._change_value, "Show Exit Game Button", False),
                                  scale=1.59)

        self._back_button = ba.buttonwidget(parent=self._root_widget,
                                            label="",
                                            position=(90, height-85-extra/5),
                                            size=(60, 60),
                                            scale=1.3,
                                            on_activate_call=ba.Call(self._back, "out_scale"),
                                            icon=ba.gettexture("crossOut"),
                                            iconscale=1.2,
                                            color=(0.40,0.40,0.50))
        ba.containerwidget(edit=self._root_widget, cancel_button=self._back_button)

    def _back(self, transition):
        ba.containerwidget(edit=self._root_widget, transition=transition)

    def _change_value(self, value, must_restart: bool, *args):
        config[value] = False if config[value] else True
        if must_restart:
            ba.screenmessage(message=ba.Lstr(resource='settingsWindowAdvanced.mustRestartText'),
                             color=(1.0, 0.5, 0.0))

class NewMainMenu:
    global _show_audio_settings, _close, _show_account_manager_window
    MainMenuWindow._new_refresh = MainMenuWindow._refresh
    def _new_refresh_in_game(self):
        self._new_refresh()
        uiscale = ba.app.ui.uiscale

        b_posX = (-128 if uiscale is ba.UIScale.SMALL else
            -128 if uiscale is ba.UIScale.MEDIUM else -128)
        b_posY = (-20.5 if uiscale is ba.UIScale.SMALL else
            -53 if uiscale is ba.UIScale.MEDIUM else -78)
        extra = (5 if uiscale is ba.UIScale.SMALL else
            2 if uiscale is ba.UIScale.MEDIUM else 0)

        if platform == "windows" or platform == "linux" or platform == "mac":
            if uiscale is ba.UIScale.LARGE:
                if config["Show Exit Game Button"]:
                    posX = 8
                    posY = 7
                    icon = ba.gettexture("achievementOutline") if config["Exit The Game Directly"] else ba.gettexture("achievementEmpty")
                    if _ba.is_in_replay():
                        posY = -16
                    if self._in_game:
                        self._button_root_widget = ba.containerwidget(parent=self._root_widget,
                                                                      size=(221, 60),
                                                                      position=(posX*2.5, posY*-12.85714285),
                                                                      scale=1)
                        self._quit_button = ba.buttonwidget(
                            parent=self._button_root_widget,
                            label=ba.Lstr(resource=self._r + ('.quitText' if 'Mac' in
                            ba.app.user_agent_string else '.exitGameText')),
                            on_activate_call=self._quit,
                            size=(200, 45),
                            position=(8, 7),
                            icon=icon)
            
            if platform == "windows" and not self._in_game:
                self._account_manager_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type="square",
                    label="",
                    position=(b_posX-b_posX*4.5, b_posY),
                    size=(81, 76+extra),
                    transition_delay=self._tdelay,
                    on_activate_call=ba.Call(_show_account_manager_window, self._root_widget))
                ba.imagewidget(parent=self._root_widget,
                               texture=ba.gettexture("googlePlayLeaderboardsIcon"),
                               size=(40, 40),
                               position=(b_posX-b_posX*4.66, b_posY-b_posY/3+extra*5),
                               transition_delay=self._tdelay,
                               color=(0.5,0.60,1))
                ba.textwidget(parent=self._root_widget,
                              text="Accounts",
                              color=(0.83, 1, 0),
                              scale=0.6,
                              position=(b_posX-b_posX*4.5, b_posY-b_posY/59+extra/1.5),
                              transition_delay=self._tdelay)

        if not self._in_game:
            self._detail_manager_button = ba.buttonwidget(
                parent=self._root_widget,
                button_type="square",
                transition_delay=self._tdelay,
                position=(b_posX, b_posY),
                size=(81, 76+extra),
                label="",
                on_activate_call=ba.Call(DetailManagerWindow, "in_scale"))
            ba.imagewidget(parent=self._root_widget,
                           texture=ba.gettexture("lock"),
                           size=(40, 40),
                           position=(b_posX-b_posY/3.5+extra*2.9, b_posY-b_posY/3+extra*5),
                           transition_delay=self._tdelay)
            ba.textwidget(parent=self._root_widget,
                          text="Details",
                          color=(0.83, 1, 0),
                          scale=0.74,
                          position=(b_posX-b_posY/12+extra/1.5, b_posY-b_posY/59+extra/1.5),
                          transition_delay=self._tdelay)
        else:
            mngr_btn_pos = 50
            if config["Show Volume Button"]:
                mngr_btn_pos = 100
                self._audio_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type="square",
                    position=(self._width+25, self._height-50),
                    size=(40, 40),
                    icon=ba.gettexture("audioIcon"),
                    iconscale=1.2,
                    on_activate_call=ba.Call(_show_audio_settings, self._root_widget))

            if config["Show The Details Button"]:
                self._detail_manager_button = ba.buttonwidget(
                    parent=self._root_widget,
                    button_type="square",
                    position=(self._width+25, self._height-mngr_btn_pos),
                    size=(40, 40),
                    icon=ba.gettexture("lock"),
                    iconscale=1.25,
                    on_activate_call=ba.Call(DetailManagerWindow, "in_scale"))
    MainMenuWindow._refresh = _new_refresh_in_game

    """Remove Confirmation Requests"""
    MainMenuWindow._new_confirm_leave_party = MainMenuWindow._confirm_leave_party
    def _leave_party(self):
        _ba.disconnect_from_host() if config["Leave The Server Directly"] else self._new_confirm_leave_party()
    MainMenuWindow._confirm_leave_party = _leave_party

    MainMenuWindow._new_confirm_end_game = MainMenuWindow._confirm_end_game
    def _end_game(self):
        if config["End The Game Directly"]:
            if not self._root_widget:
                return
            ba.containerwidget(edit=self._root_widget, transition='out_left')
            ba.app.return_to_main_menu_session_gracefully(reset_ui=False)
        else:
            self._new_confirm_end_game()
    MainMenuWindow._confirm_end_game = _end_game

    MainMenuWindow._new_confirm_end_replay = MainMenuWindow._confirm_end_replay
    def _end_replay(self):
        if config["End The Replay Directly"]:
            if not self._root_widget:
                return
            ba.containerwidget(edit=self._root_widget, transition='out_left')
            ba.app.return_to_main_menu_session_gracefully(reset_ui=False)
        else:
            self._new_confirm_end_replay()
    MainMenuWindow._confirm_end_replay = _end_replay

    MainMenuWindow._new_confirm_exit_game = MainMenuWindow._quit
    def _exit_game(self):
        if config["Exit The Game Directly"]:
            _ba.fade_screen(False,
                            time=0.2,
                            endcall=lambda: ba.quit(soft=True, back=False))
        else:
            self._new_confirm_exit_game()
    MainMenuWindow._quit = _exit_game

    def _show_audio_settings(root_widget):
        global audio_settings_detected
        audio_settings_detected = True
        ba.containerwidget(edit=root_widget, transition="out_left")
        AudioSettingsWindow()

    def _show_account_manager_window(root_widget):
        ba.containerwidget(edit=root_widget, transition="out_left")
        AccountManagerWindow(transition="in_right")

class NewSettingsWindow:
    global _show_advanced_plugins_window
    AllSettingsWindow._new_init = AllSettingsWindow.__init__
    def _new_settings_window(self, transition: str = 'in_right', origin_widget: ba.Widget = None):
        self._new_init()
        uiscale = ba.app.ui.uiscale
        width = (50 if uiscale is ba.UIScale.SMALL else
            44.7916665 if uiscale is ba.UIScale.MEDIUM else 39.58333332)
        height = (92.778021 if uiscale is ba.UIScale.LARGE else 30)
        extra = (0 if uiscale is ba.UIScale.SMALL else
            100 if uiscale is ba.UIScale.MEDIUM else 43.868132)
        
        self._new_plugins_button = ba.buttonwidget(parent=self._root_widget,
                        size=(width*2.4, 30),
                        scale=1.5,
                        label="",
                        position=(width*10.6-extra/1.05494507, width*7+height+extra/2.48704653),
                        on_activate_call=ba.Call(_show_advanced_plugins_window, self._root_widget))
        
        text_posX = width*12-extra
        text_posY = (387.5 if uiscale is ba.UIScale.SMALL else 
            391 if uiscale is ba.UIScale.MEDIUM else 395.5)
        ba.textwidget(parent=self._root_widget,
                      text="Plugins",
                      color=(0.75, 1.0, 0.7),
                      position=(text_posX, text_posY))
        ba.imagewidget(parent=self._root_widget,
                       texture=ba.gettexture("file"),
                       size=(45, 45),
                       position=(width*10.9-extra, text_posY-10))
    AllSettingsWindow.__init__ = _new_settings_window

    def _show_advanced_plugins_window(root_widget):
        ba.containerwidget(edit=root_widget, transition="out_scale")
        PluginSettingsWindow()

class AdvancedPluginsWindow:
    global _back_to_allsettings_window, _show_delete_window, _confirm_deletion, _delete_plugin
    PluginSettingsWindow._new_init = PluginSettingsWindow.__init__
    def _new_plugins_window(self, transition="in_right"):
        self._new_init(transition=transition)
        uiscale = ba.app.ui.uiscale
        w = (285 if uiscale is ba.UIScale.SMALL else
            127 if uiscale is ba.UIScale.MEDIUM else 57)
        h = (62 if uiscale is ba.UIScale.SMALL else
            60 if uiscale is ba.UIScale.MEDIUM else 58)

        self._delete_button = ba.buttonwidget(parent=self._root_widget,
                                              button_type="square",
                                              size=(50, 50),
                                              label="",
                                              position=(self._height+w, self._height-h),
                                              scale=0.87,
                                              icon=ba.gettexture("textClearButton"),
                                              iconscale=(1.22 if uiscale is ba.UIScale.SMALL else
                                                1.235 if uiscale is ba.UIScale.MEDIUM else 1.23),
                                              on_activate_call=ba.Call(_show_delete_window))
        
        ba.buttonwidget(edit=self._back_button, on_activate_call=ba.Call(_back_to_allsettings_window, self._root_widget, AllSettingsWindow))
    PluginSettingsWindow.__init__ = _new_plugins_window

    def _back_to_allsettings_window(root_widget, window):
        ba.containerwidget(edit=root_widget, transition="out_scale")
        window(transition="in_scale")

    def _show_delete_window():
        global root_widget
        root_widget = FileSelectorWindow(path=plugin_path,
                                         valid_file_extensions=["py"],
                                         allow_folders=True).get_root_widget()

    def _confirm_deletion(path, file_name, *args):
        if file_name == "BombSquadDetails":
            ba.playsound(ba.getsound("error"))
            return
        else:
            ConfirmWindow(text=f"Are you sure you want to delete {file_name}?",
                          action=ba.Call(_delete_plugin, path, file_name),
                          ok_text="Yes", cancel_text="No",
                          cancel_is_selected=True)

    def _delete_plugin(path, file_name):
        global root_widget
        try: os.unlink(f"{path}/{file_name}")
        except FileNotFoundError: pass
        finally:
            ba.playsound(ba.getsound('shieldDown'))
            ba.screenmessage(message=ba.Lstr(resource='settingsWindowAdvanced.mustRestartText'),
                             color=(1.0, 0.5, 0.0))
            ba.containerwidget(edit=root_widget, transition="out_scale")
            root_widget = FileSelectorWindow(path=plugin_path,
                                             valid_file_extensions=["py"],
                                             allow_folders=True).get_root_widget()

    FileSelectorWindow._new_command = FileSelectorWindow._on_entry_activated
    def _delete(self, entry: str):
        ba.playsound(ba.getsound("swish"))
        _confirm_deletion(plugin_path, entry)
    FileSelectorWindow._on_entry_activated = _delete

class NewAccountWindow:
    global copy_pb
    AccountSettingsWindow._new_init = AccountSettingsWindow.__init__
    def _new_account_window(self,
                            transition: str = 'in_right',
                            modal: bool = False,
                            origin_widget: ba.Widget = None,
                            close_once_signed_in: bool = False):
        self._new_init()

        if _ba.get_account_state() == "signed_in":
            pb_text = ba.textwidget(parent=self._subcontainer,
                          text=f"PB: {_ba.get_account_misc_read_val_2('resolvedAccountID', True)}",
                          position=(100, 0))
            ba.buttonwidget(parent=self._subcontainer,
                            label="Copy",
                            position=(385, 0),
                            on_activate_call=copy_pb)
    AccountSettingsWindow.__init__ = _new_account_window

    def copy_pb():
        copy_text(_ba.get_account_misc_read_val_2('resolvedAccountID', True))
        ba.screenmessage(message=f"Copied {_ba.get_account_misc_read_val_2('resolvedAccountID', True)}",
                         color=(0,1,0))
        ba.playsound(ba.getsound("ding"))

def copy_text(text):
    ba.clipboard_set_text(text)

def check_for_updates():
    url = "https://raw.githubusercontent.com/OnurV2/BombSquadDetails/main/BombSquadDetails.py"
    check = urllib.request.urlopen(url)
    check.read()

    with open(f"{plugin_path}/BombSquadDetails.py", "r") as mod:
        current_mod = mod.read()
        mod.close()
    if not check == current_mod:
        ConfirmWindow(text="BombSquadDetails:\nNew updates available!",
                      cancel_text="Not now", ok_text="Download",
                      action=ba.Call(update_mod, check))
        ba.playsound(ba.getsound("ding"))
    else:
        pass

def update_mod(new_update):
    try:
        with open(f"{plugin_path}/BombSquadDetails.py", "w") as file:
            file.write(new_update)
            ba.screenmessage(message="Successfully updated! Please restart the game",
                             color=(0,1,0))
    except Exception:
        ba.screenmessage(message="An unexpected error occurred", color=(1,0,0))
        ba.playsound(ba.getsound("error"))

# ba_meta export plugin
class Plugin(ba.Plugin):
    global _show_plugin_window, _back_to_main_menu
    def on_app_launch(self) -> None:
        if config["Unlock Pro Mode"]:
            ba.app.accounts.have_pro = lambda: True
        ba.timer(5, check_for_updates)

    """Bug Fixes"""
    AdvancedSettingsWindow._fix_old_plugins_button = AdvancedSettingsWindow.__init__
    def _fix_plugins_button(self, transition: str = 'in_right', origin_widget: ba.Widget = None):
        self._fix_old_plugins_button()
        ba.buttonwidget(edit=self._plugins_button,
                        on_activate_call=ba.Call(_show_plugin_window, self._root_widget))
    AdvancedSettingsWindow.__init__ = _fix_plugins_button

    AudioSettingsWindow._new_init = AudioSettingsWindow.__init__
    def _new_audio_window(self, transition: str = 'in_right', origin_widget: ba.Widget = None):
        self._new_init()
        global audio_settings_detected
        if audio_settings_detected:
            ba.buttonwidget(edit=self._back_button, on_activate_call=ba.Call(_back_to_main_menu, self._root_widget))
    AudioSettingsWindow.__init__ = _new_audio_window

    def _show_plugin_window(root_widget):
        ba.containerwidget(edit=root_widget, transition="out_scale")
        PluginSettingsWindow()

    def _back_to_main_menu(root_widget):
        global audio_settings_detected
        ba.containerwidget(edit=root_widget, transition="out_right")
        MainMenuWindow(transition="in_left")
        audio_settings_detected = False