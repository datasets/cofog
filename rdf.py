'''Convert COFOG csv to RDF.

:author: William Waites, Rufus Pollock, Alistair Turnbull.
'''
# attempt at rdflib 2.4 -> 3.0 compatibility
try:
    from rdflib.graph import Graph
    from rdflib.term import URIRef, Literal
    from rdflib.namespace import Namespace, RDF, RDFS
except:
    # do not want BackwardCompatGrap
    # from rdflib import Graph
    from rdflib.Graph import Graph
    from rdflib import URIRef, Literal
    from rdflib import Namespace, RDF, RDFS

cofog_url = 'http://cofog.eu/'
COFOG_BASE = '%scofog/1999' % cofog_url
COFOG = Namespace('%scofog#' % cofog_url)

DC = Namespace('http://purl.org/dc/terms/')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
OWL = Namespace('http://www.w3.org/2002/07/owl#')

def bind_ns(g):
    g.bind('cofog', COFOG)
    g.bind('dc', DC)
    g.bind('foaf', FOAF)
    g.bind('skos', SKOS)
    g.bind('owl', OWL)

def cofog_schema():
    '''Core cofog schema.
    '''
    schema = str(COFOG)[:-1]
    g = Graph(identifier=schema)
    Function = COFOG['Function']

    g.add((Function, RDF.type, OWL.Class))
    g.add((Function, RDFS.subClassOf, SKOS.Concept))
    g.add((Function, RDFS.label, Literal('Function')))

    level = COFOG['level']
    g.add((level, RDF.type, OWL['DatatypeProperty']))
    g.add((level, RDFS.domain, Function)) 
    g.add((level, RDFS.label, Literal('Function Level')))

    g.add((COFOG.Function, RDFS.isDefinedBy, URIRef(cofog_url)))
    g.add((COFOG.level, RDFS.isDefinedBy, URIRef(cofog_url)))

    g.add((COFOG['Code'], RDF.type, RDFS.Datatype))
    g.add((COFOG['Code'], RDFS.label, Literal('Function Code')))
    g.add((COFOG['Code'], RDFS.isDefinedBy, URIRef(cofog_url)))
    return g

def cofog_rdf(csv_fileobj):
    '''Convert COFOG csv to RDF.
    '''
    import csv
    reader = csv.reader(csv_fileobj)

    g = cofog_schema()

    NS = Namespace(COFOG_BASE)
    cls = NS['']
    # g = Graph(identifier=str(cls))
    g.add((cls, RDF.type, SKOS['ConceptScheme']))
    g.add((cls, DC['identifier'], Literal('COFOG_1999')))
    g.add((cls, FOAF['homepage'],
        Literal('http://unstats.un.org/unsd/class/family/family2.asp?Cl=4')))
    label = 'Classification of the Functions of Government (COFOG 1999)'
    g.add((cls, RDFS.label, Literal(label, lang='en')))
    g.add((cls, SKOS['prefLabel'], Literal(label, lang='en')))
    # skip headings
    reader.next()
    for idx,(code,description,details,change_date) in enumerate(reader):
        def get_level_and_id(code):
            parts = code.split('.')
            idstr = '/' + '/'.join([p.rjust(2, '0') for p in parts])
            level = len(parts)
            return level, idstr
        level, idstr = get_level_and_id(code)
        i = NS[idstr]

        # is this needed?
        # g = Graph(identifier=str(i))

        g.add((i, RDF.type, COFOG['Function']))
        g.add((i, RDFS.label, Literal(description, lang='en')))
        g.add((i, SKOS['prefLabel'], Literal(description, lang='en')))
        g.add((i, SKOS['definition'], Literal(description,
        lang='en')))
        g.add((i, SKOS['notation'], Literal(code, datatype=COFOG['Code'])))
        g.add((i, COFOG['level'], Literal(level)))
        g.add((i, SKOS['inScheme'], cls))
        if level > 1:
            parent, child = str(i).rsplit('/', 1)
            g.add((i, SKOS['broader'], URIRef(parent)))
            g.add((URIRef(parent), SKOS['narrower'], i))

    # TODO: ?
    # skos:hasTopConcept to top level
    # skos:narrower
    bind_ns(g)
    return g

