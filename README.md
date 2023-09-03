# FitHub
CS50 FINAL:
 CS50 FINAL project video: https://youtu.be/Rb7y3K4OVK4
 FITHUB IS A webapp to track your workouts
 the serverside application is app.py which uses flask
 before initiating the server run cd utilities and python database_loader.py:
    this will load the database tables into the fithub.db database as well as load the starting exercises from the workouts.json file
 after initiating the database the server can be run on app.py.

 Upon client connection the client will be met with a log in screen.
 upon creating an account or logging in they are met with the homescreen where they may see their stats regaurding their logged workouts
 In order to use this application: a user must log data under the workout tab in their navbar
 Upon clicking the add workout they are met with a list of workouts to choose from if they choose one a template will popup 
 the user must click add set to add a set to log in the template. Depending on the workout type the user will be asked to insert their weight, reps, duration.. etc. 
 the user may also optionally log notes into the template which will be seen on the following use of the template. 
 Upon submitting the workout the user is taken back to the homescreen where they will be met with their logged information altering their page. 
 their workout information can be seen in the form of the radar stat chart, their workout history, and workout submission history. 
 Furthermore if the user is to go back to their workout page and create workouts based on the same previous template they are able to see their chart grow with stats.
 Optionally the user may also create their own workouts to use as templates in the create workout tab. 
 Upon creating a workout the user will be able to find their workout under the workout tab when adding a new workout to their submission. 

