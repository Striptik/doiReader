from flask import Flask, render_template, request
from doiScanner import parsingRDF

app = Flask(__name__)


"""

  Home Route - Display Home page

"""
@app.route('/')
def index():
  return render_template('index.html')



"""

  Main Route - Make the Rdf Analyse of a given DOI
  Redirect to success or error page

"""
@app.route('/doi', methods = ['POST'])
def postDOI(): 
  
  # Get Form and extract DOI
  data = request.form.to_dict()
  doi = data.get('DOI', None) or None
  
  # No DOI Provided ?
  print('HO !!!')
  print(doi)
  if doi == None:
    print('yes')
    errors = []
    errors.append('No DOI provided ! Try Again')
    return render_template('error.html', errors=errors)
  
  # Parsing DOI
  res = parsingRDF(doi)
  
  # Errors ?
  errors = res.get('errors', None)
  if len(errors) > 0:
    return render_template('error.html', errors=errors)
  
  # No Errors 
  print(res)
  authors = res.get('authors', None)
  title = res.get('title', None)
  date = res.get('date', None)
  uri = res.get('uri', None)

  return render_template('success.html', uri=uri, title=title, date=date, authors=authors, lenAuth=len(authors))



"""

  Mode Route - Debug Route (Dev or Prod)

"""
@app.route('/mode', methods = ['GET'])
def appMode():
  if __name__ == '__main__':
    return 'Dev'
  else:
    return 'Production'


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')