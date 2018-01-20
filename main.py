from flask import Flask


app=Flask(__name__)


views=__import__('views')


if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)