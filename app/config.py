import os

#Especifico la ruta donde se almacenara el archivo con la db y el motor a usar - SQLITE
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../data/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
