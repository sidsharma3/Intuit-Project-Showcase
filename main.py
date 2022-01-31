# This is the function that is invoked in order to create
# and run the Flask Web Application
from application import createApp

if __name__ == '__main__':
    # first we get the Flask Web App
    flaskWebApp = createApp()
    # Then we run it
    flaskWebApp.run(debug=True)
    