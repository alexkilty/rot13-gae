#!/usr/bin/env python
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
import cgi #for escape_html


class MainPage(webapp2.RequestHandler):
    def escape_html(s):
    #for (i, o) in (("&","&amp;"),
    #               (">","&gt;"),
    #               ("<","&lt;"),
    #               ('"',"&quot;")):
    #    s=s.replace(i, o)
    #return s
    return cgi.escape(s,quote=True)

    def valid_year(year):
        if year and year.isdigit():
            year=int(year)
            if year > 1900 and year <= 2020:
                return year
            
    def valid_day(day):
        if day and day.isdigit():
            day=int(day)
            if day > 0 and day <=31:
                return day
            
    def valid_month(month):
        months = ['January',
              'February',
              'March',
              'April',
              'May',
              'June',
              'July',
              'August',
              'September',
              'October',
              'November',
              'December']
        month_abbvs=dict((m[:3].lower(), m) for m in months)
        if month:
            short_month=month[0:3].lower()
            if short_month in month_abbvs:
                return month_abbvs.get(short_month)

    form = """
    <form method="post">
        What is your birthday?
        <br>
        <label>Month
        <input type="text" name="month" value="%(month)s">
        </label>
        <label>Day
        <input type="text" name="day" value="%(day)s">
        </label>
        <label>Year
        <input type="text" name="year" value="%(year)s">
        </label>
        <div style="color: red">%(error)s</div>
        <br>
        <br>
        
    <input type="submit">
    </form>
    """
    
    
    def write_form(self,error="",month="",day="",year=""):
        self.response.out.write(form %{"error": error,
                                      "month": escape_html(month),
                                      "day": escape_html(day),
                                      "year": escape_html(year)})
    def get(self):
        self.write_form()
    def post(self):
        user_year=self.request.get('year')
        user_month=self.request.get('month')
        user_day=self.request.get('day')
        
        month=valid_month(user_month)
        day=valid_day(user_day)
        year=valid_year(user_year)
        
        if not (month and year and day):
            self.write_form("That is not valid!",user_month,user_day,user_year)
        else:
            self.response.out.write("Thanks! Thats a totally valid day!")
        #self.response.headers['Content-Type']= 'text/plain'
        #self.response.out.write(self.request)
            
class Rot13Page(webapp2.RequestHandler):
        def rot13_char(ch):
            if ch.isalpha():
              ch_low = ch.lower()
              if ch_low <= 'm':
                dist = 13
              else:
                dist = -13
              return chr(ord(ch) + dist)
            else:
                return ch
        def rot13(s):
          return ''.join( rot13_char(ch) for ch in s )

        def escape_html(s):
            return cgi.escape(s,quote=True)

        form="""
        <form method="post">
          <textarea name="text" style="height: 100px; width: 400px;">%(sometext)s</textarea>
          <br>
          <input type="submit">
        </form>
        """
        def write_form(self,sometext=""):
        self.response.out.write(form %{"sometext": escape_html(sometext)})
        
        def get(self):
            self.write_form()
            
        def post(self):
            user_text=rot13(self.request.get('text'))
            if user_text:
                self.write_form(user_text)
                
app = webapp2.WSGIApplication([('/', MainPage),('/rot13', Rot13Page)],
                              debug=True)
