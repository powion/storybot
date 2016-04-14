from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

def file_content(filename):
        with open(filename, 'r') as infile:
            text = infile.read()
            return text

class SearchEngine:
    def __init__(self):
        pass
          
    # Load an index from 'folder'.
    def load(self, folder):
        self.ix = open_dir(folder)
    
    # Build an index of txt files in 'folder' with titles specified in 'title_file'.
    def index(self, folder, title_file):
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
        self.ix = create_in(folder, schema)
        writer = self.ix.writer()
        
        titles = []
        with open(title_file, 'r') as f:
            titles = f.readlines()
        n = 0
        for tit in titles:
            path = folder + '/{}.txt'.format(n)
            text = file_content(path)
            writer.add_document(title=tit, path=path, content=text)
            n += 1
        writer.commit()

    # Search in the index by a query. You can use AND, OR, \"phrase\" etc.
    def search(self, text_query):
        with self.ix.searcher() as searcher:
            query = QueryParser("content", self.ix.schema).parse(text_query)
            results = searcher.search(query, limit = None)
            docs = []
            for res in results:
                docs += [res['path']]
            return docs
 
def testIndexing(query):
    se = SearchEngine()
    se.index('../datasets/tifu', '../datasets/tifu/titlefile.txt')
    results = se.search(query)
    return results
    
def testLoading(query):
    se = SearchEngine()
    se.load('../datasets/tifu')
    results = se.search(query)
    return results

if __name__ == "__main__":
    print("Indexing and searching...")
    print(testIndexing('hair cut'))
    print("Loading index and searching...")
    print(testLoading('hair cut'))
    
