#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)
welcome_page = """
<h2>Welcome %(username)s</h2>
"""

form = """
<form method="post">
  <table>
    <tbody>
      <tr>
        <td>
          <label for=username>Username</label>
        </td>
        <td>
          <input name="username" type=text value="%(username)s">
          <span style="color: red">%(usernameErr)s</span>
        </td>
      </tr>
    </tbody>
  </table>
  <input type="submit">
</form>
"""
class MainHandler(webapp2.RequestHandler):
    def writeForm(self, username = "", usernameErr = ""):
        username = cgi.escape(username)
        self.response.write(form % {"username" : username,
                                    "usernameErr" : usernameErr})

    def get(self):
        self.writeForm("", "")

    def post(self):
        username = self.request.get('username')

        if valid_username(username):
            self.redirect("/welcome_user?username=" + username)
        else:
            self.writeForm(username, "Bad Username")

class WelcomeHandler(webapp2.RequestHandler):
    def writeForm(self, username = ""):
        self.response.write(welcome_page % {"username" : username})

    def get(self):
        username = self.request.get("username")
        self.writeForm(username)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome_user', WelcomeHandler)
], debug=True)
