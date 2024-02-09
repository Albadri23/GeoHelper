# GeoHelper
Flask web application submitted as final project for CS50X2023 online course, GeoHelper is aim to serve all levels of geospatial profficinals more to explain later in the file.


## Description
Here GeoHelper will be explain in more details, GeoHelper has 3 main sections: coordinates, map and surveying.


### coordinates:
This section focus on working with transformation between coordinates, it has 2 fucntions:

#### 1. Helmert transformation
This function preform Helemert transformation of coordinate between one datum to another. To achive that GeodePy python library has been used,  the user is expected to enter cartesian coordinates and choose from drop menu what datum to transform from and to, the user then will be redirect to result page.

#### 2. UTM transformation
similar to first function GeodePy has been used to tranfrom from UTM coordinate system to both geographic coordinate system and cartesian coordinate system. The user is expected to enter UTM parameters with an addition of ellipsoidal height.


### Maps:
This section uses Folium python library to provide interactive maps, it has 3 functions:

#### 1. Point map with cluster
User can upload .csv file that contain postion points in large number, then Folium will produce point map with cluster, the user must make sure that csv file has latitude and longitude headers in csv file all in lowercase letters.

#### 2. Points map
User can enter set of coordinate in form of [easting, northing] pairs, user provided with dynamic input form that allow user to add as many points as user needed and also user can delete any unwanted point before submission.

#### 3. Draw plugin
Draw plugin provided by Folium, the user draw polyline, polygon, marker and more.


### Surveying
This section simulate diffrent booking sheets that geospatialist have on thier filedwork, it has 2 booking sheets:

#### l. Traverse booking sheet
An open traverse with two fixed point and two unknown points, the user is expected to enter highlighted fields of distances(m), directions(degree), and RF point coordinates. The resulted coordinate will then be corrected using Bowditch's rule.

#### 2. Leveling booking sheet
represents a leveling sheet for the case of 2 points with one turning point, the user must input: B.S and elevation of point A, B.S and F.S for the turning point, and F.S for point B.

## GeoHelper in future:
 further future devolopment of web application will be taken, focused mainly to add new functions and improving current functions.


