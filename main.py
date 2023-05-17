# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation either version
# 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this script. If not, see <https://www.gnu.org/licenses/>.
from nsdotpy.session import NSSession
import csv


UserAgent = input("Please enter your main nation: ")
NationName = input("Nation you want to place bids on: ")
Password = input("Enter its password: ")
session = NSSession("Buy all cards in CSV", "1.0.0", "Written by Thorn1000", UserAgent)

if session.login(NationName, Password):
    with open('bids.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            session.bid(row[2], row[0], row[1])
