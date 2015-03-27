from app import app
__author__ = 'feliciaan'

@app.template_filter('euro')
def euro(value):
    result = '€' + str(value/100)
    return result