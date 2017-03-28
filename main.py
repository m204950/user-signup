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

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

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
      <tr>
        <td>
          <label for="password">Password</label>
        </td>
        <td>
          <input name="password" type="password">
          <span style="color: red">%(passwordErr)s</span>
        </td>
      </tr>
      <tr>
        <td>
          <label for="verify">Verify Password</label>
        </td>
        <td>
          <input name="verify" type="password">
          <span style="color: red">%(verifyErr)s</span>
        </td>
      </tr>
      <tr>
        <td>
          <label for=email>Email (optional)</label>
        </td>
        <td>
          <input name="email" type=text value="%(email)s">
          <span style="color: red">%(emailErr)s</span>
        </td>
      </tr>
    </tbody>
  </table>
  <input type="submit">
</form>
"""
class MainHandler(webapp2.RequestHandler):
    def writeForm(self, username = "", usernameErr = "",
                        passwordErr = "", verifyErr = "",
                        email = "", emailErr = ""):
        username = cgi.escape(username)
        self.response.write(form % {"username" : username, "usernameErr" : usernameErr,
                                    "passwordErr" : passwordErr, "verifyErr" : verifyErr,
                                    "email" : email, "emailErr" : emailErr
                                    })

    def get(self):
        self.writeForm("", "")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        # default to all good
        form_ok = True
        usernameErr = ""
        passwordErr = ""
        verifyErr = ""
        emailErr = ""

        if not valid_username(username):
            usernameErr = "Bad Username.  Should be 3-20 Alpha-Numeric characters and '_', or '-'.  No spaces"
            form_ok = False
        if not valid_password(password):
            passwordErr = "Bad Password.  Should be 3-20 characters.  Any characters may be used"
            form_ok = False
        else:
            if password != verify:
                verifyErr = "Verify password doesn't match password"
                form_ok = False
        if email:    # anything entered for email
            if not valid_email(email):
                emailErr = "Bad email entered.  Needs to be something like user@company.domain"
                form_ok = False

        if form_ok:
            self.redirect("/welcome_user?username=" + username)
        else:
            self.writeForm(username, usernameErr,
                           passwordErr, verifyErr,
                           email, emailErr)


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
