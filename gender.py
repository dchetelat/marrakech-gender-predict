#######################################################
# Server side code for Naive Bayes classifier gender prediction webpage
# 11 May 2015
# By Natalia Chetelat

import webapp2
import os
import jinja2
import time
from nbpredict import Classifier


#Path to templates that use the Jinja2 templating language
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)



#Custom handler to simplify rendering of templates with Jinja2
class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        self.response.write(t.render(**kw))

#Instantiation of Classifier class (from nbpredict module).
#This is a globally accessible object initialized with null values
#by its constructor.
#Its actual values are later set by the loader handler and used
#by the Home hanlder.
classifier = Classifier()


#Main page handler
class Home(Handler):
    
    def get(self):
        self.render("index.html")

    def post(self):
        raw_text = self.request.get("raw_text")
        data = classifier.predict(raw_text)
        gender = data[0]
        probability = data[1]
        json_data = '[{"gender": "%s", "prob": "%s"}]' % (gender, probability)
        self.response.out.write(json_data)

#Handler for loading Naive Bayes model onto memory for 
#comparison with user's input text.
class LoadNB(Handler):

    def post(self):
        classifier.load("model.csv")
        self.response.out.write(classifier.isModelLoaded)

#Definition of app as mapping of URLs to handlers
app = webapp2.WSGIApplication([("/", Home),
                                ("/loadnb", LoadNB)], debug=True)


