# Copyright 2016, 2017, 2018, 2019 Fraunhofer FKIE
#
# This file is part of BREACH.
#
# BREACH is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BREACH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BREACH. If not, see <http://www.gnu.org/licenses/>.


from unittest.mock import Mock

import pytest

from attacks import AttackException
from attacks.attack_email_url import EmailURLAttack


@pytest.fixture()
def attack():
    EmailURLAttack.ssh_client_class = Mock
    return EmailURLAttack()


class TestEmailURLAttack:
    def test_sendemail_command(self, attack: EmailURLAttack):
        sendemail_command = attack._sendemail_command(attack._email_body())
        expected_sendemail_command = (
            "sendemail "
            "-f attacker@localdomain "
            "-t client1@localdomain "
            "-s 172.18.0.2 "
            "-u 'Frozen User Account' "
            "-m '"
            "<p><img src=\"http://172.18.1.1/email_header.jpg\" width=\"1100\" height=\"300\"></p>"
            "<p>Dear Jane Doe,</p>"
            "<p>our Technical Support Team unfortunately had to freeze your bank account."
            "   Please download and read the file provided in the attachment for further"
            "   information.</p>"
            "<p>We apologize for the inconvenience caused, and we are really grateful for your"
            "   collaboration. This is an automated e-mail. Please do not respond.</p>"
            "<p>For further information please visit the following Link:<br>"
            "   <a href=\"http://172.18.1.1/Bank-Of-Scotland/index.htm\">Bank Of Scotland FAQ</a>"
            "   </p>"
            "<p><img src=\"http://172.18.1.1/email_footer.jpg\" width=\"90\" height=\"90\"></p>"
            "<p>&copy; 2017 bankofscotland.co.uk. All Rights Reserved.</p>"
            "' "
            "-o tls=no "
            "-o message-content-type=html "
            "-o message-charset=UTF-8 ")
        assert sendemail_command == expected_sendemail_command

    def test_raise_exception_bad_output(self, attack: EmailURLAttack):
        attack.exec_commands_on_target = lambda _: attack.printer.print("Bad output")
        with pytest.raises(AttackException):
            attack.run()

    def test_no_exception_good_output(self, attack: EmailURLAttack):
        indicator = "Email was sent successfully"
        attack.exec_commands_on_target = lambda _: attack.printer.print(indicator)
        attack.run()
