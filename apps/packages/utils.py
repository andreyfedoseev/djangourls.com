from packages.models import PyPiPackage
import BeautifulSoup
import re
import urllib2


PYPI_URL = "http://pypi.python.org/pypi?:action=browse&show=all&c=523"
PYPY_BASE_URL = "http://pypi.python.org"


def harvest_pypi_packages():
    
    cnt = 0
    
    try:
        response = urllib2.urlopen(PYPI_URL)
    except urllib2.URLError:
        return
    
    soup = BeautifulSoup.BeautifulSoup(response.read())
    list = soup.find("table", attrs={"class":"list"})
    if not list:
        return
    for row in list.findAll("tr", attrs={"class":re.compile("(odd)|(even)")}):
        cells = row.findAll("td")
        data = {}
        data["name"] = cells[0].find("a").renderContents()
        data["url"] =  cells[0].find("a")["href"]
        if not data["url"].startswith(PYPY_BASE_URL):
            data["url"] = PYPY_BASE_URL + data["url"]
        data["version"] = data["url"].split("/")[-1]
        data["description"] = cells[1].renderContents()
        try:
            package = PyPiPackage.objects.get(name=data["name"])
            if package.version < data["version"]:
                package.version = data["version"]
                package.url = data["url"]
                package.description = data["description"]
                package.save()
                cnt += 1
        except PyPiPackage.DoesNotExist:
            package = PyPiPackage(**data)
            package.save() 
            cnt += 1
            
    return cnt
             
        
    