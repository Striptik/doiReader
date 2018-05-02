# from  urllib.request import urlopen, Request
from  rdflib import Graph, Namespace
from rdflib.namespace import FOAF, DCTERMS

DOI_URL = 'http://dx.doi.org/'


"""

  This function is deprecated. It purposed was to create a request,
  send it and retrieve the data.
  The rdflib make it

"""
# def doiReader(doi):
#   # Construct the uri with the retrieve doi
#   uri = DOI_URL + doi

#   # permits to receive turtle data
#   request_headers = {'Accept': 'text/turtle'}

#   # Create Request, send, and get the response
#   request = Request(uri, headers = request_headers)
#   response = urlopen(request)
#   data = response.read()
#   return data


""" 

    This function take the doi in parameter and return all the informations required
    --
    First Create the Graph and Parse the URI (No need anymore of the function doi Reader)
    Then, it check if there's all Subject-Predicat-Object in each Node,
    Then, Check if there's title, date and the autors
    Finnaly, get all of this informations and return them

"""
def parsingRDF(doi):
  # Init data for this DOI
  uri = DOI_URL + doi
  errors = []
  ret = {}

  # Create  the graph and parse the URI
  ret['uri'] = uri
  print('URI PARSED : ' + uri)
  graph = Graph()  
  graph.parse(uri)

  # Serialize it in turtle (optional)
  new_data = graph.serialize(format='turtle')
  
  # Check if there's Sub - Pre - Obj for each Node
  for s,p,o in graph:
    if not (s,p,o) in graph:
      errors.append('Problem with data structure (s-p-o)')
      raise Exception("Error with data structure!!")
    #print('Sub=> ',s,' Pred=> ',p,' Obj=>',o)
  
  # Title 
  title = getTitle(doi, graph)
  if title == None:
    errors.append('No Title Find !')
  else:
    ret['title'] = title 

  # Date
  date = getDate(doi, graph)
  if date == None:
    errors.append('No Date Find !')
  else:
    ret['date'] = date

  # Authors
  authors = getAuthors(graph)
  if len(authors) < 1:
    errors.append('No Authors Find !')
  else:
    ret['authors'] = authors

  # Errors
  ret['errors'] = errors

  return ret


"""

  This function permits to get the title

"""
def getTitle(doi, graph):
  for s,p,o in graph.triples((None, DCTERMS.title, None)):
    if doi in s:
      return str(o)
  return None


"""

  This function permits to get the date

"""
def getDate(doi, graph):
  for s,p,o in graph.triples((None, DCTERMS.date, None)):
    if doi in s:
      return str(o)
  return None
  

"""

  This function permits to get the Authors

"""
def getAuthors(graph):
  authors = []
  for s,p,o in graph.triples((None, FOAF.name, None)):
    if 'contributor' in s:
      authors.append(str(o))
  return authors    
