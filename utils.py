


def convertPositionToCategory(position):
    
    # Read job title to determine category
    tempPos = ''.join(x for x in position if x.isalpha()).lower()
    if("data" in tempPos or "serverless" in tempPos):
        category = "Data-Science"
    elif("machinelearning" in tempPos or "artificialintelligence" in tempPos):
        category = "Machine-Learning"
    elif("design" in tempPos or "userexperience" in tempPos or "uxui" in tempPos):
        category = "Design"
    elif("backend" in tempPos):
        category = "Back-End"
    elif("frontend" in tempPos):
        category = "Front-End"
    elif("fullstack" in tempPos):
        category = "Full-Stack"
    elif("qa" in tempPos or "quality analysis" in tempPos):
        category = "Quality-Analysis"
    else:
        category = "Developer"
        
    return category


def convertDescToTags(desc):

    #Desc must be in text format
    keywords = ["3d","Other","agile","akka","algorithm","amazon-ec2","amazon-web-services","android","angular","angularjs","ansible", \
    "apache-kafka","apache-spark","api","appium","audit","automated-tests","aws","backend","bdd","blockchain","c","c++","cassandra", \
    "cloud","css","dart","data-modeling","database","database-design","delphi","design","devops","docker","elasticsearch","elk","erp", \
    "ethereum","etl","event-sourcing","excel","finance","flask-sqlalchemy","flutter","frontend","functional-programming","git", \
    "google-bigquery","google-cloud-dataflow","google-cloud-platform","hadoop","hibernate","html","http","hybrid-mobile-app","ida", \
    "infrastructure","ios","iso","itil","java","java-8","javascript","jenkins","jvm","kotlin","kubernetes","lead","leader","linux", \
    "machine-learning","measurement","mobile","mysql","networking","nlp","nosql","objective-c","office365","oracle","penetration-testing", \
    "php","phpunit","postgresql","powershell","product","project-management","prometheus","pyspark","python","qa","r","react-native", \
    "react-redux","reactive-programming","reactjs","redux","rest","reverse-engineering","ruby","ruby-on-rails","rust","saas","scala", \
    "scss","security","selenium","sentiment-analysis","shell","spark","splunk","spring","spring-boot","sql","sre","substrate","swift", \
    "symfony","sysadmin","tdd","tensorflow","terraform","testing","text-classification","topic-modeling","typescript","user-experience", \
    "virtual-machine","warehouse","web-applications","web-component","web-services","windows"]

    tags = [word.lower() for word in desc.split(" ") if word.lower() in keywords]

    return list(dict.fromkeys(tags))

# tag format is lowercase with dashes instead of spaces
def formatTags(tags):
    result = []
    for tag in tags:
        tempTag = tag.lower().replace(" ", "-")
        if("react" in tempTag): tempTag = "react"
        if("python" in tempTag): tempTag = "python"
        if("angular" in tempTag): tempTag = "angular"
        result.append(tempTag)
        #Remove Duplicates
        result = list(dict.fromkeys(result))

    return [result]

def formatCountry(country):
    states = ["alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware","florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada","new hampshire","new jersey","new mexico","new york","north carolina","north dakota","ohio","oklahoma","oregon","pennsylvania","rhode island","south carolina","south dakota","tennessee","texas","utah","vermont","virginia","washington","west virginia","wisconsin","wyoming"]
    stateabbrs = ["al","ak","az","ar","ca","co","ct","de","fl","ga","hi","id","il","in","ia","ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj","nm","ny","nc","nd","oh","ok","or","pa","sc","ri","sd","tn","tx","ut","vt","va","wa","wv","wi","wy"]
    
    tempCountry =  country.lower()
    if (tempCountry in states or tempCountry in stateabbrs): country = "United States"
    elif(tempCountry == "us" or tempCountry == "usa"): country  = "United States"
    elif(tempCountry  == "uk"): country = "United Kingdom"
    elif(tempCountry  == "de" or country == "deutschland"): country = "Germany"
    elif(tempCountry  == "the netherlands"): country = "Netherlands"
    elif(tempCountry  == "remote"): country = "Remote"

    return country