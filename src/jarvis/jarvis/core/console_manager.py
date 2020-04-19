# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os
import psutil

from jarvis.utils.console import jarvis_logo, OutputStyler, clear, stdout_print
from jarvis.settings import ROOT_LOG_CONF
from jarvis.utils import console
from jarvis.enumerations import MongoCollections
from jarvis.utils.mongoDB import db


class ConsoleManager:
    def __init__(self, ):
        pass

    def console_output(self, text=''):

        clear()

        # -------------------------------------------------------------------------------------------------------------
        # Logo sector
        # -------------------------------------------------------------------------------------------------------------
        stdout_print(jarvis_logo)
        stdout_print("  NOTE: CTRL + C If you want to Quit.")

        # -------------------------------------------------------------------------------------------------------------
        # General info sector
        # -------------------------------------------------------------------------------------------------------------
        settings_documents = db.get_documents(collection=MongoCollections.GENERAL_SETTINGS.value)
        if settings_documents:
            settings = settings_documents[0]
            print(OutputStyler.HEADER + console.add_dashes('GENERAL INFO') + OutputStyler.ENDC)
            enabled = OutputStyler.GREEN + 'ENABLED' + OutputStyler.ENDC if settings['response_in_speech'] else OutputStyler.WARNING + 'NOT ENABLED' + OutputStyler.ENDC
            print(OutputStyler.BOLD + 'RESPONSE IN SPEECH: ' + enabled)
            print(OutputStyler.BOLD + 'ENABLED PERIOD: ' + OutputStyler.GREEN + '{0}'.format(str(settings['enabled_period'])) + OutputStyler.ENDC + OutputStyler.ENDC)
            print(OutputStyler.BOLD + 'INPUT MODE: ' + OutputStyler.GREEN + '{0}'.format(settings['input_mode'].upper() + OutputStyler.ENDC) + OutputStyler.ENDC)

        # -------------------------------------------------------------------------------------------------------------
        # System info sector
        # -------------------------------------------------------------------------------------------------------------
        print(OutputStyler.HEADER + console.add_dashes('SYSTEM') + OutputStyler.ENDC)
        print(OutputStyler.BOLD +
              'RAM USAGE: {0:.2f} GB'.format(self._get_memory()) + OutputStyler.ENDC)

        # -------------------------------------------------------------------------------------------------------------
        # Assistant logs sector
        # -------------------------------------------------------------------------------------------------------------

        print(OutputStyler.HEADER + console.add_dashes('LOG') + OutputStyler.ENDC)
        lines = subprocess.check_output(['tail', '-10', ROOT_LOG_CONF['handlers']['file']['filename']]).decode("utf-8")
        print(OutputStyler.BOLD + lines + OutputStyler.ENDC)

        # -------------------------------------------------------------------------------------------------------------
        # Assistant input/output sector
        # -------------------------------------------------------------------------------------------------------------

        print(OutputStyler.HEADER + console.add_dashes('ASSISTANT') + OutputStyler.ENDC)
        text = text if text else ''
        if text:
            print(OutputStyler.BOLD + '> ' + text + '\r' + OutputStyler.ENDC)
            print(OutputStyler.HEADER + console.add_dashes('-') + OutputStyler.ENDC)

    @staticmethod
    def _get_memory():
        pid = os.getpid()
        py = psutil.Process(pid)
        return py.memory_info()[0] / 2. ** 30
