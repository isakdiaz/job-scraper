import time
import re

def convertPositionToCategory(position):
    
    # Read job title to determine category
    tempPos = ''.join(x for x in position if x.isalpha()).lower()
    if("data" in tempPos or "serverless" in tempPos):
        category = "Data-Science"
    elif("mlengineer" in tempPos or "machinelearning" in tempPos or "artificialintelligence" in tempPos):
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

    keywords = [".net",".net core","active directory","activemq","administration","aem","agile","airflow","akka","algorithm","amazon dynamodb","amazon ec2","amazon web services","analytics","android","android framework","android jetpack","angular","angular universal","angular7","angular8","angularjs","ansible","apache","apache kafka","apache spark","apex","api","appium","architecture","artificial intelligence","ase","asp.net web api","atg","audit","automated deployment","automated tests","automation","aws","aws iam","aws lambda","azure","azure devops","backbone.js","backend","bamboo","bash","bazel","bdd","bigdata","blockchain","bluetooth","bluetooth lowenergy","boost","business intelligence","butterknife","c","c++","c++11","c++14","c++17","cassandra","circleci","circuit breaker","clojure","cloud","cmake","cocoa","cocoapods","coldfusion","common lisp","confluence","connectivity","containers","content management system","continuous delivery","continuous deployment","continuous integration","cordova","core bluetooth","cpu","cryptography","csdl","css","css3","cucumber","d3.js","dagger 2","data","data modeling","data processing","data science","data structures","data warehouse","database","database design","databricks","dataflow","debugging","dependency injection","design","design patterns","detox","device management","devops","directx","distributed computing","distributed system","django","docker","domain driven design","drm","e commerce","ecmascript 6","elasticsearch","elixir","elk","elm","embedded","embedded linux","ember.js","erp","es2015","ethereum","etl","event sourcing","excel","expert system","fastlane","filesystems","finance","flask","flask sqlalchemy","flux","frontend","functional programming","gcp","gem5","gin gonic","git","github","gitlab","go","goland","golang","google analytics","google app engine","google bigquery","google cloud dataflow","google cloud platform","google data studio","graalvm","gradle","graphic design","graphics","graphql","groovy","grpc","h.265","hadoop","heroku","hibernate","hpc","hsm","html","html5","http","hybrid mobile app","hybris","ida","influxdb","informatica","infrastructure","infrastructure as a code","integration","interaction design","ios","iphone","iso","istio","itil","jasmine","java","java 8","java ee","javafx","javascript","jenkins","jira","jquery","js","jsp","junit","jvm","kafka","kdb","keras","kerberos","kotlin","kubernetes","lambda","lead","leader","less","libraries","linux","low latency","lucene","machine learning","macos","mapr","mapreduce","mariadb","matlab","maven","measurement","memcached","micro frontend","microfrontend","microservices","microsoft dynamics nav","microsoft test manager","middleware","mobile","mockups","model view controller","mongodb","mqtt","multicast","multiplatform","multithreading","mvvm","mysql","netbeans","network analysis","networking","next","next.js","ngrx","nlp","node.js","nosql","numpy","objective c","office365","oop","open source","opencart","opencl","opengl","openshift","openssl","operating system","oracle","packer","pageobjects","pandas","penetration testing","perl","php","php 7","phpunit","playframework","plsql","polymer","postgresql","powerbi","powershell","presto","procedural generation","product","product management","project management","prometheus","protocol buffers","puppet","pyramid","pyspark","pytest","python","python 3.x","qa","qnx","qt","r","rabbitmq","raspberry pi","react","react.js","react native","react native android","react redux","reactive programming","reactjs","redis","redux","rendering","rest","restful architecture","retrofit","retrofit2","reverse engineering","robotics","ror","routing","rtos","ruby","ruby on rails","ruby on rails 3","ruby on rails 5","rust","rx java","rx kotlin","rx swift","rxjs","rxswift","saas","salesforce","sass","scala","scale","scheme","scikit learn","scripting","scrum","scrumboard","scss","sdk","security","selenium","selenium webdriver","semantic web","sentiment analysis","sequence","server","serverless","shell","sidekiq","smarty","software design","software quality","solid principles","solidity","spark","spark streaming","splunk","spreadsheet","spring","spring boot","spring mvc","sprint","sql","sql loader","sql server","sre","static analysis","statistics","streaming","substrate","swift","swiftui","swing","swt","symfony","sysadmin","system","system design","system integration","tableau","tdd","tensorflow","teradata","terraform","testing","text classification","tooling","topic modeling","truffle","twitter bootstrap","types","typescript","ubuntu","uikit","uml","unit testing","unity3d","unix","unreal engine4","user experience","user interaction","user interface","user stories","virtual machine","vpc","vue.js","vulkan","warehouse","web application design","web applications","web component","web services","webassembly","webgl","webpack","webrtc","websocket","wechat","wifi","windows","wordpress","xcode","yii2"]

    # keywordsWithSpaces = [word.replace("-", " ").replace(",", ".")  for word in keywords] # Convert dashes to spaces
    tags = [word.replace(" ", "-").replace(".", ",") for word in keywords if word in desc.lower() and len(word) > 1]

    return list(dict.fromkeys(tags))

# tag format is lowercase with dashes instead of spaces
def formatTags(tags):
    result = []
    for tag in tags:
        tempTag = tag.lower().replace(" ", "-").replace(".", ",")
        if("react" in tempTag): tempTag = "react"
        if("python" in tempTag): tempTag = "python"
        if("angular" in tempTag): tempTag = "angular"
        result.append(tempTag)
        #Remove Duplicates
        result = list(dict.fromkeys(result))

    return result

def formatCountry(country):
    states = ["alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware","florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada","new hampshire","new jersey","new mexico","new york","north carolina","north dakota","ohio","oklahoma","oregon","pennsylvania","rhode island","south carolina","south dakota","tennessee","texas","utah","vermont","virginia","washington","west virginia","wisconsin","wyoming"]
    stateabbrs = ["al","ak","az","ar","ca","co","ct","de","fl","ga","hi","id","il","in","ia","ks","ky","la","me","md","ma","mi","mn","ms","mo","mt","ne","nv","nh","nj","nm","ny","nc","nd","oh","ok","or","pa","sc","ri","sd","tn","tx","ut","vt","va","wa","wv","wi","wy"]
    
    tempCountry =  re.sub('\d',' ', country).lower().strip() # REGEX - only chars & spaces
    if (tempCountry in states or tempCountry in stateabbrs): country = "United States" #TODO CA can be canada and DE can be germany
    elif(tempCountry == "us" or tempCountry == "usa"): country  = "United States"
    elif(tempCountry  == "uk"): country = "United Kingdom"
    elif(tempCountry  == "de" or country == "deutschland"): country = "Germany"
    elif(tempCountry  == "the netherlands"): country = "Netherlands"
    elif(tempCountry  == "remote"): country = "Remote"

    return country

def formatCountryFromUrl(url, country):

    # Only useful for linked in urls
    if ("ca.linkedin.com" in url): country = "Canada"
    elif ("uk.linkedin.com" in url): country = "United Kingdom"
    elif ("es.linkedin.com" in url): country = "Spain"
    elif ("nl.linkedin.com" in url): country = "Netherlands"
    elif ("de.linkedin.com" in url): country = "Germany"
    elif ("jp.linkedin.com" in url): country = "Japan"
    elif ("th.linkedin.com" in url): country = "Thailand"
    elif ("cl.linkedin.com" in url): country = "Chile"

    return country

def calculateTimeMultipler(timeText):
    # English, German, Dutch, Japanese & Thai included
    today = ['today', 'heute', 'vandaag', 'hoy', '今日', 'ในวันนี้']
    hour = ['hour', 'stunde', 'uur', 'hora', '時', "ชั่วโมง"]
    day = ['day', 'tag', 'dag', 'dia', '日', 'วัน']
    week =  ['week', 'woche', 'weken', 'semana', '週間', 'สัปดาห์']
    month = ['month', 'monat', 'maand', 'mes', '月', 'เดือน']
    print(timeText)
    for word in today:
        if word in timeText:
            print("Today")
            return (60 * 60 * 24)
    for word in hour:
        if word in timeText:
            print("Hour")
            return (60 * 60)
    for word in day:
        if word in timeText:
            print("Day")
            return (60 * 60 * 24)
    for word in week:
        if word in timeText:
            print("Week")
            return (60 * 60 * 24 * 7)
    for word in month:
        if word in timeText:
            print("Month")
            return (60 * 60 * 24 * 30)
    
    print("Cannot calculate Time multipler for: ", timeText)
    return (60 * 60 * 24)

def calculateEpoch(timeText):

    timeMultiplier = calculateTimeMultipler(timeText)
    try:
        timeIntArr = [int(i) for i in timeText if i.isdigit()]
        total = 0
        for i in range(len(timeIntArr)):
            total += timeIntArr[len(timeIntArr) - 1 - i] * 10 ** i
        timeInt = total
        print("TimeInt: ", timeInt)
    except:
        print("time string", timeText)
        print("failed on time int: ", [int(i) for i in timeText.split(" ") if i.isdigit()])
        timeInt = 1 # Default value


    return round(time.time()) - (timeInt * timeMultiplier)
