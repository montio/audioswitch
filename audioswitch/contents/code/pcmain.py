# -*- coding: utf-8 -*-
#
# Author: Ralf Stemmer <ralf.stemmer@gmx.net>
# Date: Son Aug 19 2012, 17:02:23
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

# Import essential modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

import os
import alsaaudio

# source: http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python/1695250#1695250
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

STATE = enum('UNKNOWN', 'SPEAKER', 'HEADPHONE')
API   = enum('PULSEAUDIO', 'ALSA')



class pcmain(plasmascript.Applet):

    #   Constructor, forward initialization to its superclass
    #   Note: try to NOT modify this constructor; all the setup code
    #   should be placed in the init method.
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    #   init method
    #   Put here all the code needed to initialize our plasmoid
    def init(self):
        # IMPORTANT: Configuration of this plasmoid
        self.api = API.ALSA
        #self.api = API.PULSEAUDIO
        # END OF CONFIG

        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        #self.setBackgroundHints(self.TranslucentBackground)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)

        self.headphone = Plasma.PushButton(self.applet)
        self.headphone.nativeWidget().setIcon(KIcon("audio-headset"))
        self.headphone.setCheckable(True)
        self.headphone.setChecked(False)
        self.headphone.clicked.connect(self.SwitchToHeadphone)
        self.layout.addItem(self.headphone)

        self.speaker = Plasma.PushButton(self.applet)
        self.speaker.nativeWidget().setIcon(KIcon("speaker"))
        self.speaker.setCheckable(True)
        self.speaker.setChecked(False)
        self.speaker.clicked.connect(self.SwitchToSpeaker)
        self.layout.addItem(self.speaker)
        #self.layout.addStretch()

        self.state = STATE.UNKNOWN;


    def SwitchToSpeaker(self):
        self.speaker.setChecked(True)
        self.headphone.setChecked(False)

        if self.state == STATE.SPEAKER :
            return

        # IMPORTANT: Configure everything to enable your speakers
        if self.api == API.PULSEAUDIO :
            # Configuration of this plasmoid - you have to change the sink and the portname
            os.system("pacmd set-sink-port alsa_output.pci-0000_00_1b.0.analog-stereo analog-output-speaker")
        elif self.api == API.ALSA :
            alsaaudio.Mixer('Speaker').setmute(0)
            alsaaudio.Mixer('Front').setmute(1)
        else :
            return

        self.state = STATE.SPEAKER
        return


    def SwitchToHeadphone(self):
        self.speaker.setChecked(False)
        self.headphone.setChecked(True)

        if self.state == STATE.HEADPHONE :
            return

        # IMPORTANT: Configure everything to enable your headphones
        if self.api == API.PULSEAUDIO :
            # Configuration of this plasmoid - you have to change the sink and the portname
            os.system("pacmd set-sink-port alsa_output.pci-0000_00_1b.0.analog-stereo analog-output")
        elif self.api == API.ALSA :
            alsaaudio.Mixer('Speaker').setmute(1)
            alsaaudio.Mixer('Front').setmute(0)
        else :
            return

        self.state = STATE.HEADPHONE
        return

    #   CreateApplet method
    #   Note: do NOT modify it, needed by Plasma
def CreateApplet(parent):
    return pcmain(parent)
