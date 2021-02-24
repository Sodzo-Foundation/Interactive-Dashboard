from django.shortcuts import render, redirect
import datetime
from .models import Pollutants, ConfirmedPollutants

from datetime import date
import xlsxwriter

from django.views.decorators.http import require_http_methods
#from pusher import Pusher

from django.http import HttpResponse, JsonResponse
from django.template import RequestContext,loader

import urllib.request, json
from geopy.geocoders import Nominatim
from geopy.point import Point
geolocator = Nominatim(user_agent="app")
from django.http import HttpResponse


"""
Feb. 10, 2021, 2:34 p.m.	Bottle	0.1766145	30.0789805	Kirembe			Kasese	1
Moonlight Lodge, Margherita Street, Kirembe, Kasese, Western Region, 471, Uganda	Uganda
Feb. 10, 2021, 2:34 p.m.	Bottle	0.1740419	30.0773055	Kirembe			Kasese	100
Kirembe, Kasese, Western Region, 471, Uganda

/stores/1/?hours=sunday&map=flash,

from django.shortcuts import render

def detail(request,store_id=1,location=None):
    # Access store_id url parameter with 'store_id' variable and location url parameter with 'location' variable
    # Extract 'hours' or 'map' value appended to url as
    # ?hours=sunday&map=flash
    hours = request.GET.get('hours', '')
    map = request.GET.get('map', '')
    # 'hours' has value 'sunday' or '' if hours not in url
    # 'map' has value 'flash' or '' if map not in url
    return render(request,'stores/detail.html')
"""

  
def create_jsonfile(dic):
    import json, os
    #filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'world-countries.js')
    filename = "static/download/district_boundaries.json"
    
    
    filehandle = open(filename, 'r')
    #print('bbbbbb')
    countriesData = json.loads(str(filehandle.read()))

    #n=0
    final= {"type":"FeatureCollection"}
    P=[]
    length = len(countriesData['features'])
    #dic={'uganda': 30000}
    for the_location,count in dic.items():
        #print(the_location,count)
        for i in range(length):
            #print(n,len(countriesData['features']) )
            location = countriesData["features"][i]["properties"]["name"].lower()
            
            if str(location.lower()) in str(the_location.lower()) or str(the_location.lower()) in str(location.lower()) or  str(location.lower()) == str(the_location.lower()):
                print(2,the_location,location, count)
                countriesData["features"][i]["properties"]["count"] = int(count)
                #print ('here',countriesData["features"][i])
                P.append(countriesData["features"][i])
            else:
                pass
                
        
        final['features']=P
    
    #print(len(final))
    with open('static/map/uganda.js', 'w') as out_file:
      out_file.write('var countriesData = %s;' % json.dumps(final))
      
#start
def index(request):


    districts= ["Mukono","Wakiso", "Kampala","Entebbe","Kalangala"] #mofidina
    locations= ["Nsazi","Koome", "Zinga","Damba","Namalusu","Nakiwogo","Bukasa","Ssese", "Nakasero", "Wandegeya"]
    dic={}
    shores ="Lake Victoria"

    #urlink = "https://wanderdrone.appspot.com/"
    dataloc= {"Nakasero": "Kampala", "Wandegeya": "Kampala"}
    try:
        import json
        #with open('gpss.txt') as f:
        #    json_data = json.load(f)
        #urlink = "https://wanderdrone.appspot.com/" [0.3261603,32.575628]
        p = [{"geometry":{"type":"Point","coordinates":[0.3252616,32.5752046]},"count":1,"type":"Feature","properties":{}},
           {"geometry":{"type":"Point","coordinates":[0.3952616,32.5752046]},"count":1,"type":"Feature","properties":{}},
           {"geometry":{"type":"Point","coordinates":[0.3352616,32.5752046]},"count":1, "type":"Feature","properties":{}}]    
        #ddic={}

        url_link = "http://192.168.1.11:5000/gps"
        #url_link = "https://wanderdrone.appspot.com/"
        with urllib.request.urlopen(url_link) as url:
            json_data = json.loads(url.read().decode())
        #print ('json_data2',json_data, type(json_data))
        """
        d = {1: "one", 2: "three"}
        d1 = {2: "two"}

        # updates the value of key 2
        d.update(d1)
        print(d)

        d1 = {3: "three"}

        # adds element with key 3
        d.update(d1)
        print(d)
        """
        for i in [json_data]:
            points  =  i["geometry"]['coordinates']
            coord = str(points[0])+', '+ str(points[1])
            #urlink = "https://wanderdrone.appspot.com/"
            #coord = location_failed_get_cordinates(urlink)
            lat= points[0]
            long = points[1]
            geolocator = Nominatim(user_agent="app")
            location = geolocator.reverse(Point(lat, long))

            #location = geolocator.reverse(coord, exactly_one=True)
            address = location.raw['address']
            city = address.get('city', '')
            suburb = address.get('suburb', '')
            country = address.get('country', '')

            loc=location[0]
            count = i['count']
            country = str(loc).split()[-1]
            
            #print(lat,long,loc)
            """
            try:
                ddic[loc] += 1
            except:
                ddic[loc] = 1
            """
            
            locations = dataloc.keys()
            for l in locations:
                #total = Pollutants.objects.filter(location=l,category='Bottle').count()
                total = Pollutants.objects.filter(lat=lat,long=long,count=count, category='Bottle').count()
                #total = Pollutants.objects.filter(lat=lat,long=long,category='Bottle').count()
                #print("1location:",l,"total:",total, 'loc:',loc, str(loc).find(l))
                cond = str(loc).find(l)
                if total == 0 or total >= 1:# and cond != -1:
                    #print("1location:",l,"total:",total)
                    try:
                        record = Pollutants.objects.create(category="Bottle",
                                                       lat=lat,
                                                       long=long,
                                                       count=count,
                                                       district = dataloc[l],
                                                       country=country,    
                                                       location=l,
                                                       address=loc)
                    except:
                        record = Pollutants.objects.create(category="Bottle",
                                                       lat=lat,
                                                       long=long,
                                                       count=count,
                                                       #district = dataloc[l],
                                                       country=country,
                                                       location=l,
                                                       address=loc)
                    record.save()
                elif total >= 1:
                    print("1location:",l,"total:",total)
                    #key = Pollutants.objects.get(location=l,lat=lat,long=long,category='Bottle')
                    #key = Pollutants.objects.get(lat=lat,long=long,category='Bottle')
                    #records = ConfirmedPollutants.objects.create(pollutant=key,shores=shores,total=total)
                    #records.save()
                else:
                    pass
                    
    except:
        print('yyyyyyyyyyyyyyyes')#, lat,long,location[0])
               
        #key = Pollutants.objects.get(district=d,location=l,category='Bottle')
    #dic3333 {1: [1, 'Wandegeya', 'Kampala'], 2: [1, 'Wandegeya', 'Kampala'], 3: [1, 'Wandegeya', 'Kampala']}    

    pollutants = ConfirmedPollutants.objects.all()

    the_pollutants = Pollutants.objects.all()
    m=1
    t=0
    res_display={}
    """
    for k in the_pollutants:
        res_display[m] = [k.count,k.location, k.district]
        m += 1
        t = t + 1
    """
    #Pollutants.objects.filter(district__isnull=True)
    #Pollutants.objects.filter(district=True) #state and village
    #Pollutants.objects.filter(district=True) # 
    
    countries={}
    for k in the_pollutants:
        total = Pollutants.objects.filter(address = k.address).count()
        #print('counting', len(k.district), len(k.location))
        if len(k.district) > 1 and len(k.location) > 1 and len(k.suburb) ==0: # case district 1
            res_display[(total,k.location, k.district.replace('Capital City', ''), k.country)] = m
            #print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxresss', res_display)
            #if k.location.lower() == 'kirembe' or k.district.lower() == 'kasese':
            #    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxresss', res_display)
            district = k.district.replace('Capital City', '')
            try:
                countries[district] += int(k.count)
            except:
                countries[district] = int(k.count)
        
        if len(k.district) > 1 and len(k.suburb) > 1 and len(k.location) ==0: # case district 1
            res_display[(total,k.suburb, k.district.replace('Capital City', ''), k.country)] = m
            district = k.district.replace('Capital City', '')
            try:
                countries[district] += int(k.count)
            except:
                countries[district] = int(k.count)
                
        elif len(k.district) == 0 and len(k.state) > 1 and len(k.city_district) > 1: #case state 2
            res_display[(total,k.city_district, k.state, k.country)] = m
            
            try:
                countries[k.state] += int(k.count)
            except:
                countries[k.state] = int(k.count)
                
        elif len(k.district) == 0 and len(k.state) > 1 and len(k.village) > 1: #case state 2
            res_display[(total,k.village, k.state, k.country)] = m
            
            try:
                countries[k.state] += int(k.count)
            except:
                countries[k.state] = int(k.count)
            
        
        #res_display[(total,k.location, k.district.replace('Capital City', ''), k.country)] = m
            
        #res_display[m]= [total,k.location, k.district]
        
        #district = k.district.replace('Capital City', '')
        """
        try:
            countries[district] += int(k.count)
        except:
            countries[district] = int(k.count)
        """
        
        #res_display[m] = [k.count,k.location, k.district]
        m += 1
        t = t + 1
        
    res_display = {y:x for x,y in res_display.items()}
    
    d={}
    for k,v in res_display.items():
        try:
            d[(str(v[1]), str(v[2]), str(v[3]))] += int(v[0])
        except:
            d[(str(v[1]), str(v[2]), str(v[3]))] = int(v[0])

    p=1
    e={}
    the_counts=[]

    for k,v in d.items():
        the_counts.append(int(v))
        val= d[(str(k[0]), str(k[1]), str(k[2]))]
        e[(val,str(k[0]), str(k[1]), str(k[2]))] = p
        p+=1

    res_display = {y:x for x,y in e.items()}
                                                                                                  
    today = datetime.datetime.now()
    now = today.strftime("%m/%d/%Y, %H:%M %p")
    
    #count = len(res_display)
    #print ("countries", countries)
    create_jsonfile(countries)
    
    """
    try:
        create_json(countries)
    except:
        pass
    """
    
    h={}
    n=1
    districts= ["Mukono","Wakiso", "Kampala","Entebbe","Kalangala"] #mofidina
    locations= ["Nsazi","Koome", "Zinga","Damba","Namalusu","Nakiwogo","Bukasa","Ssese", "Nakasero", "Wandegeya"]

    
    #start
    workbook = xlsxwriter.Workbook('static/download/Intelligent Real Time Data Visualization Dashboard Lawuna Project Data.xlsx')

    #worksheet = workbook.worksheets[0]
    worksheet = workbook.add_worksheet()
    chart = workbook.add_chart({'type': 'line'})
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Widen the first column to display the dates.
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 9)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 14)
    worksheet.set_column('F:F', 12)
    worksheet.set_column('G:G', 12)

    worksheet.set_column('H:H', 12)
    worksheet.set_column('I:I', 12)
    worksheet.set_column('J:J', 12)
    worksheet.set_column('K:K', 12)
    
    #worksheet.write_column('A1', "Date", "Location", "District", "Shores", "Total")
    #worksheet.write_column('A1', ["Date"], ["Location"])
    # Some data to be plotted in the worksheet.


    title = ["Date", "Category", "village", "Suburb", "Town","State","Location", "District", "Shores", "Total","Country"]
    dates=[]
    values=[]
    locations = []
    districts=[]
    shores=[]
    results =[]
    category=[]
    village=[]
    suburb=[]
    town=[]
    state=[]
    country=[]
    dic={}
    n=1
    display=[]
    water_body = "Lake Victoria"
    the_count=[]

    
    for row in the_pollutants:
        date_time_obj = datetime.datetime.strptime(str(row.created_on)[:21], '%Y-%m-%d %H:%M:%S.%f')
        the_date = date_time_obj.date()
        dates.append(date_time_obj.date())
        values.append(row.count)
        the_count.append(int(row.count))
        locations.append(row.location)
        districts.append(row.district)
        country.append(row.country)
        shores.append(water_body)
        category.append(row.category)

        
        village.append(row.village)
        suburb.append(row.suburb)
        town.append(row.city_district)
        state.append(row.state)

        
        #results.append([row.location, row.total, row.lat, row.long])
        #display.append([row.total,row.pollutant.location, row.pollutant.district, row.pollutant.address])
        #dic[n] = display
        #dic[n]= results
        #values.append(1)
        n+=1
        
    # Write the date to the worksheet.
    #print (dates,category, locations, districts, shores, values)
    worksheet.write_row('A4', title)
    worksheet.write_column('A5', dates,date_format)
    worksheet.write_column('B5', category )

    worksheet.write_column('C5', village)
    worksheet.write_column('D5', suburb)
    worksheet.write_column('E5', town)
    worksheet.write_column('F5', state)
    
    worksheet.write_column('G5', locations )
    worksheet.write_column('H5', districts)
    worksheet.write_column('I5', shores)
    worksheet.write_column('J5', values)
    worksheet.write_column('K5', country)


    count = sum(the_count)
    
    # Add a series to the chart.
    chart.add_series({
        'categories': '=Sheet1!$A$5:$A$'+str(count),
        'values': '=Sheet1!$J$5:$J$'+str(count),
    })
   
    # Configure the X axis as a Date axis and set the max and min limits.
    
    chart.set_x_axis({
        'date_axis': True,
        'min': date(2020, 1, 2),
        'max': date(2022, 1, 9),
        #'min': min(dates),
        #'max': max(dates),
    })

    # Turn off the legend.
    chart.set_legend({'none': True})

    # Insert the chart into the worksheet.
    pos = 'B%s'% str(count+8)
    worksheet.insert_chart(pos, chart)

    workbook.close()
    #end
    """
    print ('dic', ddic)
    print ('dic3333', h,len(h))
    #dic= {1: [['7', 'Bukasa', 'Mukono', ''], ['6', 'Nakiwogo', 'Kampala', '']]}
    d ={1: ['30', 'Nsazi', 'Entebbe', ''],2: ['26', 'Ssese', 'Kalangala', '']}
    #dic = [['7', 'Bukasa', 'Mukono', ''], ['6', 'Nakiwogo', 'Kampala', '']]
    print('dic', d)
    """
    #count=1
    count = sum(the_counts)
    context = {
        'poll': the_pollutants,
        'now': now,
        'count': count,
        'countries':countries,
        'results': results,
        'pollutants': res_display,
        'shores': "Lake Victoria",
    }

    #print('res_display 1', res_display, countries)
    return render(request, 'index.html',context )







#start
def update(request):


    districts= ["Mukono","Wakiso", "Kampala","Entebbe","Kalangala"] #mofidina
    locations= ["Nsazi","Koome", "Zinga","Damba","Namalusu","Nakiwogo","Bukasa","Ssese", "Nakasero", "Wandegeya"]
    dic={}
    shores ="Lake Victoria"

    #urlink = "https://wanderdrone.appspot.com/"
    dataloc= {"Nakasero": "Kampala", "Wandegeya": "Kampala"}
    try:
        import json
        #with open('gpss.txt') as f:
        #    json_data = json.load(f)
        #urlink = "https://wanderdrone.appspot.com/" [0.3261603,32.575628]
        p = [{"geometry":{"type":"Point","coordinates":[0.3252616,32.5752046]},"count":1,"type":"Feature","properties":{}},
           {"geometry":{"type":"Point","coordinates":[0.3952616,32.5752046]},"count":1,"type":"Feature","properties":{}},
           {"geometry":{"type":"Point","coordinates":[0.3352616,32.5752046]},"count":1, "type":"Feature","properties":{}}]    
        #ddic={}

        url_link = "http://192.168.1.11:5000/gps"
        #url_link = "https://wanderdrone.appspot.com/"
        with urllib.request.urlopen(url_link) as url:
            json_data = json.loads(url.read().decode())
        #print ('json_data2',json_data, type(json_data))
        """
        d = {1: "one", 2: "three"}
        d1 = {2: "two"}

        # updates the value of key 2
        d.update(d1)
        print(d)

        d1 = {3: "three"}

        # adds element with key 3
        d.update(d1)
        print(d)
        """
        for i in [json_data]:
            points  =  i["geometry"]['coordinates']
            coord = str(points[0])+', '+ str(points[1])
            #urlink = "https://wanderdrone.appspot.com/"
            #coord = location_failed_get_cordinates(urlink)
            lat= points[0]
            long = points[1]
            geolocator = Nominatim(user_agent="app")
            location = geolocator.reverse(Point(lat, long))

            #location = geolocator.reverse(coord, exactly_one=True)
            address = location.raw['address']
            city = address.get('city', '')
            suburb = address.get('suburb', '')
            country = address.get('country', '')

            loc=location[0]
            count = i['count']
            country = str(loc).split()[-1]
            
            #print(lat,long,loc)
            """
            try:
                ddic[loc] += 1
            except:
                ddic[loc] = 1
            """
            
            locations = dataloc.keys()
            for l in locations:
                #total = Pollutants.objects.filter(location=l,category='Bottle').count()
                total = Pollutants.objects.filter(lat=lat,long=long,count=count, category='Bottle').count()
                #total = Pollutants.objects.filter(lat=lat,long=long,category='Bottle').count()
                #print("1location:",l,"total:",total, 'loc:',loc, str(loc).find(l))
                cond = str(loc).find(l)
                if total == 0 or total >= 1:# and cond != -1:
                    #print("1location:",l,"total:",total)
                    try:
                        record = Pollutants.objects.create(category="Bottle",
                                                       lat=lat,
                                                       long=long,
                                                       count=count,
                                                       district = dataloc[l],
                                                       country=country,    
                                                       location=l,
                                                       address=loc)
                    except:
                        record = Pollutants.objects.create(category="Bottle",
                                                       lat=lat,
                                                       long=long,
                                                       count=count,
                                                       #district = dataloc[l],
                                                       country=country,
                                                       location=l,
                                                       address=loc)
                    record.save()
                elif total >= 1:
                    print("1location:",l,"total:",total)
                    #key = Pollutants.objects.get(location=l,lat=lat,long=long,category='Bottle')
                    #key = Pollutants.objects.get(lat=lat,long=long,category='Bottle')
                    #records = ConfirmedPollutants.objects.create(pollutant=key,shores=shores,total=total)
                    #records.save()
                else:
                    pass
                    
    except:
        print('yyyyyyyyyyyyyyyes')#, lat,long,location[0])
               
        #key = Pollutants.objects.get(district=d,location=l,category='Bottle')
    #dic3333 {1: [1, 'Wandegeya', 'Kampala'], 2: [1, 'Wandegeya', 'Kampala'], 3: [1, 'Wandegeya', 'Kampala']}    

    pollutants = ConfirmedPollutants.objects.all()

    the_pollutants = Pollutants.objects.all()
    m=1
    t=0
    res_display={}
    """
    for k in the_pollutants:
        res_display[m] = [k.count,k.location, k.district]
        m += 1
        t = t + 1
    """
    #Pollutants.objects.filter(district__isnull=True)
    #Pollutants.objects.filter(district=True) #state and village
    #Pollutants.objects.filter(district=True) # 
    
    countries={}
    for k in the_pollutants:
        total = Pollutants.objects.filter(address = k.address).count()
        #print('counting', len(k.district), len(k.location))
        if len(k.district) > 1 and len(k.location) > 1 and len(k.suburb) ==0: # case district 1
            res_display[(total,k.location, k.district.replace('Capital City', ''), k.country)] = m
            district = k.district.replace('Capital City', '')
            try:
                countries[district] += int(k.count)
            except:
                countries[district] = int(k.count)
        
        if len(k.district) > 1 and len(k.suburb) > 1 and len(k.location) ==0: # case district 1
            res_display[(total,k.suburb, k.district.replace('Capital City', ''), k.country)] = m
            district = k.district.replace('Capital City', '')
            try:
                countries[district] += int(k.count)
            except:
                countries[district] = int(k.count)
                
        elif len(k.district) == 0 and len(k.state) > 1 and len(k.city_district) > 1: #case state 2
            res_display[(total,k.city_district, k.state, k.country)] = m
            
            try:
                countries[k.state] += int(k.count)
            except:
                countries[k.state] = int(k.count)
                
        elif len(k.district) == 0 and len(k.state) > 1 and len(k.village) > 1: #case state 2
            res_display[(total,k.village, k.state, k.country)] = m
            
            try:
                countries[k.state] += int(k.count)
            except:
                countries[k.state] = int(k.count)
            
        
        #res_display[(total,k.location, k.district.replace('Capital City', ''), k.country)] = m
            
        #res_display[m]= [total,k.location, k.district]
        
        
        #district = k.district.replace('Capital City', '')
        """
        try:
            countries[district] += int(k.count)
        except:
            countries[district] = int(k.count)
        """
        #res_display[m] = [k.count,k.location, k.district]
        m += 1
        t = t + 1
        
    res_display = {y:x for x,y in res_display.items()}
    
    d={}
    for k,v in res_display.items():
        try:
            d[(str(v[1]), str(v[2]), str(v[3]))] += int(v[0])
        except:
            d[(str(v[1]), str(v[2]), str(v[3]))] = int(v[0])

    p=1
    e={}
    the_counts =[]
    for k,v in d.items():
        #print('val', k,d)
        the_counts.append(int(v))
        val= d[(str(k[0]), str(k[1]), str(k[2]))]
        e[(val,str(k[0]), str(k[1]), str(k[2]))] = p
        p+=1

    res_display = {y:x for x,y in e.items()}
                                                                                                  
    today = datetime.datetime.now()
    now = today.strftime("%m/%d/%Y, %H:%M %p")
    
    #count = len(res_display)
    #print ("countries", countries)
    #create_jsonfile(countries)
    """
    try:
        create_json(countries)
    except:
        pass
    """
    h={}
    n=1
    districts= ["Mukono","Wakiso", "Kampala","Entebbe","Kalangala"] #mofidina
    locations= ["Nsazi","Koome", "Zinga","Damba","Namalusu","Nakiwogo","Bukasa","Ssese", "Nakasero", "Wandegeya"]

    
    #start
    workbook = xlsxwriter.Workbook('static/download/Intelligent Real Time Data Visualization Dashboard Lawuna Project Data.xlsx')

    #worksheet = workbook.worksheets[0]
    worksheet = workbook.add_worksheet()
    chart = workbook.add_chart({'type': 'line'})
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

    # Widen the first column to display the dates.
    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 9)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 14)
    worksheet.set_column('F:F', 12)
    worksheet.set_column('G:G', 12)

    worksheet.set_column('H:H', 12)
    worksheet.set_column('I:I', 12)
    worksheet.set_column('J:J', 12)
    worksheet.set_column('K:K', 12)
    #worksheet.write_column('A1', "Date", "Location", "District", "Shores", "Total")
    #worksheet.write_column('A1', ["Date"], ["Location"])
    # Some data to be plotted in the worksheet.
    #title = ["Date", "Category", "Location", "District", "Shores", "Total","Country"]
    title = ["Date", "Category", "village", "Suburb", "Town","State","Location", "District", "Shores", "Total","Country"]
    dates=[]
    values=[]
    locations = []
    districts=[]
    shores=[]
    results =[]
    category=[]
    country=[]
    dic={}
    n=1
    display=[]
    water_body = "Lake Victoria"
    the_count=[]

    village = []
    suburb = []
    town = []
    state = []
    
    for row in the_pollutants:
        #new_dt = str(row.pollutant.created_on)[:19]
        date_time_obj = datetime.datetime.strptime(str(row.created_on)[:21], '%Y-%m-%d %H:%M:%S.%f')
        the_date = date_time_obj.date()
        dates.append(date_time_obj.date())
        values.append(row.count)
        the_count.append(int(row.count))
        locations.append(row.location)
        districts.append(row.district)
        country.append(row.country)
        shores.append(water_body)
        category.append(row.category)
        #results.append([row.location, row.total, row.lat, row.long])
        #display.append([row.total,row.pollutant.location, row.pollutant.district, row.pollutant.address])
        #dic[n] = display
        #dic[n]= results
        #values.append(1)
        village.append(row.village)
        suburb.append(row.suburb)
        town.append(row.city_district)
        state.append(row.state)
        
        n+=1
        
    # Write the date to the worksheet.
    #print (dates,category, locations, districts, shores, values)
    
    worksheet.write_row('A4', title)
    worksheet.write_column('A5', dates,date_format)
    worksheet.write_column('B5', category )

    worksheet.write_column('C5', village)
    worksheet.write_column('D5', suburb)
    worksheet.write_column('E5', town)
    worksheet.write_column('F5', state)
    
    worksheet.write_column('G5', locations )
    worksheet.write_column('H5', districts)
    worksheet.write_column('I5', shores)
    worksheet.write_column('J5', values)
    worksheet.write_column('K5', country)


    count = sum(the_count)
    
    # Add a series to the chart.
    chart.add_series({
        'categories': '=Sheet1!$A$5:$A$'+str(count),
        'values': '=Sheet1!$J$5:$J$'+str(count),
    })
   
    # Configure the X axis as a Date axis and set the max and min limits.
    
    chart.set_x_axis({
        'date_axis': True,
        'min': date(2020, 1, 2),
        'max': date(2022, 1, 9),
        #'min': min(dates),
        #'max': max(dates),
    })

    # Turn off the legend.
    chart.set_legend({'none': True})

    # Insert the chart into the worksheet.
    pos = 'B%s'% str(count+8)
    worksheet.insert_chart(pos, chart)

    workbook.close()
    #end
    """
    print ('dic', ddic)
    print ('dic3333', h,len(h))
    #dic= {1: [['7', 'Bukasa', 'Mukono', ''], ['6', 'Nakiwogo', 'Kampala', '']]}
    d ={1: ['30', 'Nsazi', 'Entebbe', ''],2: ['26', 'Ssese', 'Kalangala', '']}
    #dic = [['7', 'Bukasa', 'Mukono', ''], ['6', 'Nakiwogo', 'Kampala', '']]
    print('dic', d)
    """
    #count=1
    count = sum(the_counts)
    """
    context = {
        'poll': the_pollutants,
        'now': now,
        'count': count,
        'countries':countries,
        'results': results,
        'pollutants': res_display,
        'shores': "Lake Victoria",
    }
    """
    #print('res_display', res_display,countries)
    return JsonResponse({'latest_results_list':res_display,'countries':countries, 'count':count})



#mapupdate start

#start
def mapupdate(request):


    districts= ["Mukono","Wakiso", "Kampala","Entebbe","Kalangala"] #mofidina
    locations= ["Nsazi","Koome", "Zinga","Damba","Namalusu","Nakiwogo","Bukasa","Ssese", "Nakasero", "Wandegeya"]
    dic={}
    shores ="Lake Victoria"

    #urlink = "https://wanderdrone.appspot.com/"
    dataloc= {"Nakasero": "Kampala", "Wandegeya": "Kampala"}
    """
    try:
        import json
        #with open('gpss.txt') as f:
        #    json_data = json.load(f)
        #urlink = "https://wanderdrone.appspot.com/" [0.3261603,32.575628]
        p = [{"geometry":{"type":"Point","coordinates":[0.3252616,32.5752046]},"count":1,"type":"Feature","properties":{}},
           {"geometry":{"type":"Point","coordinates":[0.3952616,32.5752046]},"count":1,"type":"Feature","properties":{}},
           {"geometry":{"type":"Point","coordinates":[0.3352616,32.5752046]},"count":1, "type":"Feature","properties":{}}]    
        #ddic={}

        url_link = "http://192.168.1.11:5000/gps"
        #url_link = "https://wanderdrone.appspot.com/"
        with urllib.request.urlopen(url_link) as url:
            json_data = json.loads(url.read().decode())
        #print ('json_data2',json_data, type(json_data))
        
        for i in [json_data]:
            points  =  i["geometry"]['coordinates']
            coord = str(points[0])+', '+ str(points[1])
            #urlink = "https://wanderdrone.appspot.com/"
            #coord = location_failed_get_cordinates(urlink)
            lat= points[0]
            long = points[1]
            geolocator = Nominatim(user_agent="app")
            location = geolocator.reverse(Point(lat, long))

            #location = geolocator.reverse(coord, exactly_one=True)
            address = location.raw['address']
            city = address.get('city', '')
            suburb = address.get('suburb', '')
            country = address.get('country', '')

            loc=location[0]
            count = i['count']
            country = str(loc).split()[-1]
            
            #print(lat,long,loc)
            
            
            locations = dataloc.keys()
            for l in locations:
                #total = Pollutants.objects.filter(location=l,category='Bottle').count()
                total = Pollutants.objects.filter(lat=lat,long=long,count=count, category='Bottle').count()
                #total = Pollutants.objects.filter(lat=lat,long=long,category='Bottle').count()
                #print("1location:",l,"total:",total, 'loc:',loc, str(loc).find(l))
                cond = str(loc).find(l)
                if total == 0 or total >= 1:# and cond != -1:
                    #print("1location:",l,"total:",total)
                    try:
                        record = Pollutants.objects.create(category="Bottle",
                                                       lat=lat,
                                                       long=long,
                                                       count=count,
                                                       district = dataloc[l],
                                                       country=country,    
                                                       location=l,
                                                       address=loc)
                    except:
                        record = Pollutants.objects.create(category="Bottle",
                                                       lat=lat,
                                                       long=long,
                                                       count=count,
                                                       #district = dataloc[l],
                                                       country=country,
                                                       location=l,
                                                       address=loc)
                    record.save()
                elif total >= 1:
                    print("1location:",l,"total:",total)
                    #key = Pollutants.objects.get(location=l,lat=lat,long=long,category='Bottle')
                    #key = Pollutants.objects.get(lat=lat,long=long,category='Bottle')
                    #records = ConfirmedPollutants.objects.create(pollutant=key,shores=shores,total=total)
                    #records.save()
                else:
                    pass
                    
    except:
        print('yyyyyyyyyyyyyyyes')#, lat,long,location[0])
               
        #key = Pollutants.objects.get(district=d,location=l,category='Bottle')
    #dic3333 {1: [1, 'Wandegeya', 'Kampala'], 2: [1, 'Wandegeya', 'Kampala'], 3: [1, 'Wandegeya', 'Kampala']}    
    """
    pollutants = ConfirmedPollutants.objects.all()

    the_pollutants = Pollutants.objects.all()
    m=1
    t=0
    res_display={}
     
    
    countries={}
    loc={}
    the_count=[]
    
    for k in the_pollutants:
        total = Pollutants.objects.filter(address = k.address).count()
        #print('counting', len(k.district), len(k.location))
        if len(k.district) > 1 and len(k.location) > 1 and len(k.suburb) ==0: # case district 1
            res_display[(total,k.location, k.district.replace('Capital City', ''), k.country)] = m
            district = k.district.replace('Capital City', '')
            loc[k.location] = (k.lat,k.long)
            the_count.append(int(k.count))
            try:
                countries[district] += int(k.count)
            except:
                countries[district] = int(k.count)
        
        if len(k.district) > 1 and len(k.suburb) > 1 and len(k.location) ==0: # case district 1
            res_display[(total,k.suburb, k.district.replace('Capital City', ''), k.country)] = m
            district = k.district.replace('Capital City', '')
            loc[k.suburb] = (k.lat,k.long)
            the_count.append(int(k.count))
            try:
                countries[district] += int(k.count)
            except:
                countries[district] = int(k.count)
                
        elif len(k.district) == 0 and len(k.state) > 1 and len(k.city_district) > 1: #case state 2
            res_display[(total,k.city_district, k.state, k.country)] = m
            loc[k.city_district] = (k.lat,k.long)
            the_count.append(int(k.count))
            
            try:
                countries[k.state] += int(k.count)
            except:
                countries[k.state] = int(k.count)
                
        elif len(k.district) == 0 and len(k.state) > 1 and len(k.village) > 1: #case state 2
            res_display[(total,k.village, k.state, k.country)] = m
            loc[k.village] = (k.lat,k.long)
            try:
                countries[k.state] += int(k.count)
            except:
                countries[k.state] = int(k.count)
            
        
        #res_display[(total,k.location, k.district.replace('Capital City', ''), k.country)] = m
            
        #res_display[m]= [total,k.location, k.district]
        
        
        #district = k.district.replace('Capital City', '')
        """
        try:
            countries[district] += int(k.count)
        except:
            countries[district] = int(k.count)
        """
        #res_display[m] = [k.count,k.location, k.district]
        m += 1
        t = t + 1
        
    res_display = {y:x for x,y in res_display.items()}


    d={}
    for k,v in res_display.items():
        try:
            d[(str(v[1]), str(v[2]), str(v[3]))] += int(v[0])
        except:
            d[(str(v[1]), str(v[2]), str(v[3]))] = int(v[0])

    p=1
    e={}

    for k,v in d.items():
        val= d[(str(k[0]), str(k[1]), str(k[2]))]
        e[(val,str(k[0]), str(k[1]), str(k[2]))] = p
        p+=1

    res_display = {y:x for x,y in e.items()}
    
    d={}
    n = 1
    for k,v in res_display.items():
        #print(v,k)
        lat = loc[v[1]][0]
        lon = loc[v[1]][1]
        d[v[1],v[0], lat,lon,v[3]]= n #('Wandegeya', 1530, '0.325356', '32.5753125', 'Uganda')=1
        #print (v[0],v[1], lat,lon,v[3])
        n += 1
    #print(d)
    
    count = sum(the_count)
    
     
   
    res_display = {y:x for x,y in d.items()}

    #print('mapupdate_display', res_display)
    count = sum(the_count)
    return JsonResponse({'latest_results_list':res_display, 'count':count})
   


#mapupdate end



def mapupdates(request):
    
    
    the_pollutants = Pollutants.objects.all()
    m=1
    t=0
    res_disp={}
    d={}
    count=0
    the_count=[]
    res_display={}
    
    loc={}
    for k in the_pollutants:
        total = Pollutants.objects.filter(location = k.location, district = k.district).count()
        #res_display[m]= [total,k.location, k.district]
        res_disp[(total,k.location, k.district)] = m
        loc[k.location] = (k.lat,k.long)
        #res_display[m] = [k.count,k.location, k.district]
        the_count.append(int(k.count))
        m += 1
        t = t + 1
        count += int(k.count)
    #res_display = {y:(x[0],x[1],loc[x][0],loc[x][1],x[2]) for x,y in res_display.items()}
    
    #res_display = {
    p=1
    for x,y in res_disp.items():
        k = (str(x[1]),x[0],loc[x[1]][0],loc[x[1]][1],x[2])
        #print (x[1],x[0],loc[x[1]][0],loc[x[1]][1],x[2])
        res_display[p]=k
        p+=1
        #print('here', x[2],x[0])
        #create_jsonfile(x[2],x[0])# location, count
        #res_display[y]=(x[0],x[1],loc[x][0],loc[x][1],x[2])
    
                   
    #res_display = {y:x for x,y in res_display.items()} 
    """
    for k in the_pollutants:
        total = Pollutants.objects.filter(location = k.location, district = k.district).count()
        #res_display[m]= [total,k.location, k.district]
        res_display[(k.location,total,k.lat,k.long,k.district)] = m
        the_count.append(int(k.count))
        #res_display[m] = [k.count,k.location, k.district]
        m += 1
        #count += total
    res_display = {y:x for x,y in res_display.items()}
    """
    today = datetime.datetime.now()
    now = today.strftime("%m/%d/%Y, %H:%M %p")
    count = sum(the_count)
    
    #count = the_pollutants.count()
    print('mapupdate_display', res_display)
    return JsonResponse({'latest_results_list':res_display, 'count':count})

#map end
def mapurl(request):
    
    """
    import json
    with open('static/download/gpss.txt') as f:
        json_data = json.load(f)


    for i in json_data:
        points  =  i["geometry"]['coordinates']
        coord = str(points[0])+', '+ str(points[1])

        lat= points[0]
        long = points[1]

        try:

            village = ''
            city_district = ''
            district = ''
            suburb = ''
            state = ''
            country= ''
            
            geolocator = Nominatim(user_agent="app")
            loc = geolocator.reverse(Point(lat, long))
            
            location = geolocator.reverse(coord, exactly_one=True)
            address = location.raw['address']
            #print('address', address)
            village = address.get('village', '')
            city_district = address.get('city_district','')
            city = address.get('city', '')
            #neighbourhood = address.get('neighbourhood', '')
            suburb = address.get('suburb', '')
            state = address.get('state', '')
            country = address.get('country', '')
            count=1

            print('address', address)
            
           
            
            try:
                record = Pollutants.objects.create(category="Bottle",
                                                   lat=lat,
                                                   long=long,
                                                   count=count,
                                                   village = village,
                                                   city_district = city_district,
                                                   district = city,
                                                   suburb = suburb,
                                                   state = state,
                                                   country=country,
                                                   address=loc)
                record.save()
            except:
                print ('location', location)
        except:
           print ('out')
    """
    res_display= {1: ['Kampala', 1, 0.3252616,	32.5752046], 2: ['Nsazi', 2, 0.3261603, 32.575628]}

    return JsonResponse({'latest_results_list':res_display})





#map end
def mapurlss(request):
    the_pollutants = Pollutants.objects.all()
    m=1
    t=0
    res_display={}
    
    res_display= {1: ['Kampala', 1, 0.3252616,	32.5752046], 2: ['Nsazi', 2, 0.3261603, 32.575628]}
    return JsonResponse({'latest_results_list':res_display})
    
    

def updates(request):
     #results = [ob.as_json() for ob in Results.objects.all()]
     # results = [ob.as_json() for ob in ConfirmedPollutants.objects.all()]
     #results = [ob for ob in ConfirmedPollutants.objects.all()]
     results = {'foo':  'bar'}
     print('results', results)
     return JsonResponse({'latest_results_list':results})



@require_http_methods(["GET"])
def getcoordinates(request):
    """Directory of user profiles."""
    #coordinates = request.GET.get('coordinates', None)
    #print(request.GET)
    print('coordinates')
    print(request.GET)
    #print(coordinates)
    return None
    #response
    #return render(request, 'function_views/users.html', context)



def get_location_from_cordinates(url_link):
    import urllib.request, json

    #url_link = "https://wanderdrone.appspot.com/"
    with urllib.request.urlopen(url_link) as url:
        data = json.loads(url.read().decode())
        points = data['geometry']['coordinates']
        coord = str(points[0])+', '+ str(points[1])
        lat= points[0]
        long = points[1]
        print(lat,long)

    from geopy.geocoders import Nominatim
    from geopy.point import Point
    geolocator = Nominatim(user_agent="app")
    #                 location = geolocator.reverse("52.509669, 13.376294")
    #coord = "0.096466, 32.557266"

    lat = 0.0964666
    long = 32.557266

    #lat = -103.954
    #long = 1.97134

    location = geolocator.reverse(Point(lat, long))
    print (location)

    k = location[0]
    m = k.split()
    return (m[0], m[1], lat, long, location)


def location_failed_get_cordinates(url_link):
    import urllib.request, json

    #url_link = "https://wanderdrone.appspot.com/"
    with urllib.request.urlopen(url_link) as url:
        data = json.loads(url.read().decode())
        points = data['geometry']['coordinates']
        coord = str(points[0])+', '+ str(points[1])
        lat= points[0]
        long = points[1]
    return (lat,long)



def location(coord):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="app")
    #                 location = geolocator.reverse("52.509669, 13.376294")
    #location = geolocator.reverse("0.0964, 32.5572")
    location = geolocator.reverse(coord)
    #Location(Bugiri, Wakiso, Central Region, PO BOX 50, Uganda, (0.103562, 32.57834, 0.0))
    k = location[0]
    p = k[0].replace(',','')
    return p
    
 
