from flask import Flask, flash, redirect, render_template, request, session, url_for
import folium
from werkzeug.utils import secure_filename
import sys
import os
from os.path import join, dirname, realpath
from folium.plugins import MarkerCluster
import pandas as pd
from datetime import date
from geodepy.constants import itrf2014_to_gda2020, itrf2014_to_itrf2005
from geodepy.transform import *
from geodepy.constants import agd66_to_gda94, itrf2014_to_gda2020_sd, atrf2014_to_gda2020_sd, atrf2014_to_gda2020, itrf2008_to_gda94_sd, itrf2005_to_gda94_sd
from geodepy.transform import conform7
from matplotlib import pyplot as plt
import matplotlib



app = Flask(__name__)
app.secret_key = 'Mahmood key'

app.config["TEMPLATES_AUTO_RELOAD"] = True


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/upload')
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#function from : https://www.askpython.com/python-modules/flask/flask-error-handling
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'),500


#string to class from : https://stackoverflow.com/a/1176180
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

#from flask documantation: https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods = ["GET"] )
def index():
    return render_template("index.html")



@app.route("/about", methods = ["GET"] )
def about():
    return render_template("about.html")


@app.route("/maps", methods = ["GET", "POST"])
def maps():
    if request.method == "GET":
        return render_template("points.html")

    else:

         east = request.form.getlist("east")
         north = request.form.getlist("north")
         if not east or not north:
              return render_template("error.html")


         map = folium.Map(location=(23, 50), zoom_start=1.5)
             # the way to retrive list form : https://stackoverflow.com/a/39003383

         for (a, b) in  zip(east, north):
              folium.Marker(location=[a, b], tooltip="Point",icon = folium.Icon(color="black")).add_to(map)

         map.save('templates/map.html')
         return render_template("soresult.html")


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/cluster', methods =["GET", "POST"])
def cluster():
      if request.method == "GET":
            return render_template("cluster.html")
      else:
            if 'file' not in request.files:
                  flash('no file part')
                  return redirect("/cluster")
            file = request.files.get('file')

            if file.filename == '':
                  flash("No selected files")
                  return redirect("/cluster")

            #how to read csv file from : https://www.geeksforgeeks.org/uploading-and-reading-a-csv-file-in-flask/
            if file and allowed_file(file.filename):
                 data_file = secure_filename(file.filename)
                 file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_file))
                 session['uploaded_data_file_path'] =os.path.join(app.config['UPLOAD_FOLDER'],data_file)

                 data_file_path = session['uploaded_data_file_path']
                 df = pd.read_csv(data_file_path, encoding='unicode_escape')

                 map = folium.Map(location=(47.116386, -101.299591))
                 marker_cluster = MarkerCluster().add_to(map)

                 for lat, lon in zip(df.latitude, df.longitude):
                       folium.Marker(
                             location=[lat, lon],
                             tooltip="point",
                             icon = folium.Icon(color="black")
                       ).add_to(marker_cluster)

                 map.save("templates/fcls.html")
                 return render_template("clr.html")

@app.route('/fcls')
def fcls():
    return render_template('fcls.html')


@app.route('/mapmain')
def mapmain():
    return render_template('simple_map.html')



@app.route('/draw')
def draw():
      return render_template('draw.html')


@app.route('/drawf')
def drawf():
    return render_template('drawf.html')


@app.route('/sheet')
def sheet():
    return render_template('sheet.html')


@app.route('/level')
def level():
    return render_template('levelling.html')


@app.route('/trav')
def trav():
    return render_template('trav.html')


@app.route('/coord')
def coord():
    return render_template('coord.html')


@app.route('/trs', methods =["GET", "POST"])
def trs():
     if request.method == 'GET':
        return render_template('trs.html')
     else:
          if not request.form.get("east") or not request.form.get("north") or not request.form.get("h") or not request.form.get("zone"):
               return render_template("error.html")

          else:

            #get input from user
            east =  float(request.form.get("east"))
            north =  float(request.form.get("north"))
            h =  float(request.form.get("h"))
            zone =  float(request.form.get("zone"))

            lat, lon, psf, grid_convo = grid2geo(zone, east, north)
            x, y, z = llh2xyz(lat, lon, h)

            return render_template("trsre.html", lat = lat, lon = lon, x = x, y = y, z = z)



@app.route('/helm', methods = ["GET", "POST"])
def helm():
    if request.method == "GET":
        return render_template('helm.html')
    else:
         if not request.form.get("x") or not request.form.get("y") or not request.form.get("z"):
              return render_template("error.html")
         x = float(request.form.get("x"))
         y = float(request.form.get("y"))
         z = float(request.form.get("z"))
         value = request.form.get("val")


         cls =  str_to_class(value)


         #using conform7 to transform

         result = conform7(x, y, z, cls)
         xv = result[0]
         yv = result[1]
         zv = result[2]

         return render_template("helmr.html",xv = xv, yv = yv, zv = zv)





@app.route('/rh')
def rh():
    return render_template('rights.html')






