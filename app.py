from flask import Flask, render_template

app=Flask(__name__)

#this decorator is provided to give the index page link
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/about')
def about():
    return "About Page"
#this is the about page link

if __name__=='__main__':
    app.run(debug=True)
#this is the main entry point of the application

