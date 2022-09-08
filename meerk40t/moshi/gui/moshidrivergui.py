# -*- coding: ISO-8859-1 -*-

import wx

from meerk40t.core.units import Length
from meerk40t.device.gui.warningpanel import WarningPanel
from meerk40t.gui.icons import icons8_administrative_tools_50
from meerk40t.gui.mwindow import MWindow
from meerk40t.gui.wxutils import ScrolledPanel, TextCtrl

_ = wx.GetTranslation


class MoshiConfigurationPanel(ScrolledPanel):
    def __init__(self, *args, context=None, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context

        self.checkbox_home_right = wx.CheckBox(self, wx.ID_ANY, _("Home Right"))
        self.checkbox_home_bottom = wx.CheckBox(self, wx.ID_ANY, _("Home Bottom"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.on_check_home_right, self.checkbox_home_right)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_home_bottom, self.checkbox_home_bottom)
        # self.Bind(wx.EVT_CHECKBOX, self.on_check_random_ppi, self.checkbox_random_ppi)
        # end wxGlade
        self.SetupScrolling()

    def __set_properties(self):
        self.checkbox_home_right.SetToolTip(
            _("Indicates the device Home is on the right")
        )
        self.checkbox_home_bottom.SetToolTip(
            _("Indicates the device Home is on the bottom")
        )
        # self.checkbox_random_ppi.SetToolTip(
        #     _("Rather than orderly PPI, we perform PPI based on a randomized average")
        # )
        # self.checkbox_random_ppi.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MoshiDriverGui.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Pulse Planner")), wx.HORIZONTAL
        )
        sizer_home = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Shift Home Position")), wx.HORIZONTAL
        )
        sizer_config = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Configuration")), wx.HORIZONTAL
        )
        sizer_config.Add(self.checkbox_home_right, 1, wx.EXPAND, 0)
        sizer_config.Add(self.checkbox_home_bottom, 1, wx.EXPAND, 0)
        sizer_main.Add(sizer_config, 0, wx.EXPAND, 0)

        sizer_main.Add(sizer_home, 0, wx.EXPAND, 0)
        # sizer_6.Add(self.checkbox_random_ppi, 0, 0, 0)
        sizer_main.Add(sizer_6, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        # end wxGlade

    def pane_show(self):
        # self.context.listen("pipe;buffer", self.on_buffer_update)
        self.context.listen("active", self.on_active_change)

    def pane_hide(self):
        # self.context.unlisten("pipe;buffer", self.on_buffer_update)
        self.context.unlisten("active", self.on_active_change)

    def on_active_change(self, origin, active):
        # self.Close()
        pass

    def on_check_home_right(self, event):  # wxGlade: MoshiDriverGui.<event_handler>
        self.context.home_right = self.checkbox_home_right.GetValue()

    def on_check_home_bottom(self, event):  # wxGlade: MoshiDriverGui.<event_handler>
        self.context.home_bottom = self.checkbox_home_bottom.GetValue()

    def on_check_random_ppi(self, event):  # wxGlade: MoshiDriverGui.<event_handler>
        pass


class MoshiDriverGui(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(305, 410, *args, **kwds)
        self.context = self.context.device
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Moshiboard-Configuration"))

        self.notebook_main = wx.aui.AuiNotebook(
            self,
            -1,
            style=wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_SCROLL_BUTTONS
            | wx.aui.AUI_NB_TAB_SPLIT
            | wx.aui.AUI_NB_TAB_MOVE,
        )

        self.ConfigurationPanel = MoshiConfigurationPanel(
            self.notebook_main, wx.ID_ANY, context=self.context
        )

        self.notebook_main.AddPage(self.ConfigurationPanel, _("Configuration"))

        self.panel_warn = WarningPanel(self, id=wx.ID_ANY, context=self.context)
        self.notebook_main.AddPage(self.panel_warn, _("Warning"))

        self.Layout()

        self.add_module_delegate(self.ConfigurationPanel)
        self.add_module_delegate(self.panel_warn)

    def window_open(self):
        self.ConfigurationPanel.pane_show()
        self.panel_warn.pane_show()

    def window_close(self):
        self.ConfigurationPanel.pane_hide()
        self.panel_warn.pane_hide()

    def window_preserve(self):
        return False

    @staticmethod
    def submenu():
        return ("Device-Settings", "Configuration")
