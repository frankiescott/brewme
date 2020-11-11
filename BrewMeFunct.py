import requests
from hamilton import hamiltonian_beer_cycle



def search(addr, city, state, radius):
	google_but_worse = {
	'Alabama':  ["Georgia", "Mississippi", "Florida", "Tennessee", "North_Carolina", "South_Carolina"],
    'Alaska': [],
    'Arizona': ["New_Mexico", "Utah", "Nevada", "California", "Colorado"],
    'Arkansas': ["Missouri", "Oklahoma", "Louisiana", "Mississippi", "Tennessee"],
    'California': ["Arizona", "Nevada", "Oregon"],
    'Colorado': ["Wyoming", "Utah", "Nebraska", "Kansas", "Oklahoma", "New_Mexico"],
    'Connecticut': ["New_York", "Massachusetts", "Rhode_Island"],
    'Delaware': ["Maryland", "New_York", "New_Jersey"],
    'District_of_Columbia': ["Maryland", "Virginia"],
    'Florida': ["Alabama", "Georgia"],
    'Georgia': ["Alabama","Florida", "South_Carolina", "Tennessee", "North_Carolina"],
    'Hawaii': [],
    'Idaho': ["Washington", "Oregon", "Nevada", "Montana", "Utah", "Wyoming"],
    'Illinois': ["Indiana", "Wisconsin", "Iowa", "Missouri", "Kentucky"],
    'Indiana': ["Illinois", "Ohio", "Michigan", "Kentucky"],
    'Iowa': ["South_Dakota", "Minnesota", "Missouri", "Nebraska", "Illinois", "Wisconsin"],
    'Kansas': ["Nebraska", "Missouri", "Oklahoma", "Colorado"],
    'Kentucky': ["Ohio", "Indiana", "Illinois", "Tennessee", "Missouri", "West_Virginia", "Virginia"],
    'Louisiana': ["Texas", "Arkansas", "Mississippi"],
    'Maine': ["New_Hampshire"],
    'Maryland': ["Virginia", "Pennsylvania", "West_Virginia","Delaware"],
    'Massachusetts': ["Rhode_Island", "Connecticut", "New_Hampshire", "Vermont", "New_York"],
    'Michigan': ["Indiana", "Ohio"],
    'Minnesota': ["Wisconsin", "Iowa", "North_Dakota", "South_Dakota"],
    'Mississippi': ["Arkansas", "Louisiana", "Alabama", "Tennessee"],
    'Missouri': ["Illinois", "Kansas", "Oklahoma", "Arkansas", "Tennessee", "Kentucky", "Iowa", "Nebraska"],
    'Montana': ["Idaho", "Wyoming", "North_Dakota", "South_Dakota"],
    'Nebraska': ["Iowa", "South_Dakota", "Kansas", "Wyoming", "Colorado"],
    'Nevada': ["Oregon", "Idaho", "California", "Arizona", "Utah"],
    'New_Hampshire': ["Vermont", "Maine", "Massachusetts"],
    'New_Jersey': ["Pennsylvania", "New_York", "Delaware"],
    'New_Mexico': ["Texas", "Arizona", "Colorado", "Utah", "Oklahoma"],
    'New_York': ["Vermont", "Massachusetts", "Connecticut", "Pennsylvania", "New_Jersey"],
    'North_Carolina': ["Virginia", "Tennessee", "South_Carolina", "Georgia"],
    'North_Dakota': ["South_Dakota", "Montana", "Minnesota"],
    'Ohio': ["Indiana", "Kentucky", "West_Virginia", "Pennsylvania", "Michigan"],
    'Oklahoma': ["Texas", "Kansas", "Arkansas", "Colorado", "New_Mexico", "Missouri"],
    'Oregon': ["Washington", "Idaho", "California", "Nevada"],
    'Pennsylvania': ["New_York", "New_Jersey", "Delaware", "Maryland", "West_Virginia", "Ohio"],
    'Rhode_Island': ["Massachusetts", "Connecticut"],
    'South_Carolina': ["North_Carolina", "Georgia"],
    'South_Dakota': ["Minnesota", "Montana", "Wyoming", "Nebraska", "Iowa"],
    'Tennessee': ["Kentucky", "Illinois", "Indiana", "Ohio", "West_Virginia", "Virginia", "North_Carolina", "Mississippi", "Alabama", "Georgia"],
    'Texas': ["Louisiana", "Arkansas", "Oklahoma", "New_Mexico"],
    'Utah': ["Nevada", "Arizona", "Idaho", "Wyoming", "Colorado", "New_Mexico"],
    'Vermont': ["New_York", "New_Hampshire", "Massachusetts"],
    'Virginia': ["West_Virginia", "Maryland", "North_Carolina", "Tennessee", "Kentucky"],
    'Washington': ["Idaho", "Oregon"],
    'West_Virginia': ["Ohio", "Pennsylvania", "Maryland", "Virginia", "Kentucky"],
    'Wisconsin': ["Minnesota", "Iowa", "Illinois"],
    'Wyoming': ["Idaho", "Montana", "Utah", "Colorado", "Nebraska", "South_Dakota"],
	}
	loc = "https://api.openbrewerydb.org/breweries?by_state=" + state
	adj_list = google_but_worse[state]
	#addr = "4690+vestal+parkway+east,Vestal,New+York"
	#rad = 100;
#get breweries from the database based on a state query in loc
	JS = requests.get(loc).json()
    
	for state in adj_list:
		new_loc = "https://api.openbrewerydb.org/breweries?by_state=" + state
		new_list = requests.get(new_loc).json()
		JS = JS + new_list
	#print(JS)
#make a list of addresses to query to Google in the form name,city,state with spaces filled by +s
	loc_data = ['+'.join(i['name'].split())+','+'+'.join(i['city'].split())+','+'+'.join(i['state'].split()) for i in JS]
	#print(loc_data)

#Generate distance matrix data from api queries
	urls = [requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + "+".join(addr.split()) + "," + "+".join(city.split()) + "," + "+".join(state.split('_')) + "&destinations=" + i + "&key=").json() for i in loc_data]
	#print(len(urls))
	urls = [i for i in urls if i['status'] != 'INVALID_REQUEST']
#Turn string data about distances in urls into floating point
	for item in urls:
		dist = item['rows'][0]['elements'][0]['distance']['text'].split()[0]
		new_num = ""
		for c in dist:
			if c != ',':
				new_num = new_num + c
		item['rows'][0]['elements'][0]['distance']['text'] = float(new_num)

#filter distances that are greater than our selected distance
	urls = [i for i in urls if i['rows'][0]['elements'][0]['distance']['text'] < radius]

#Scrape data out of queried json that we want for final display
	final_data = [{"address": i['destination_addresses'][0], "distance": i['rows'][0]['elements'][0]['distance']['text'], "hours": i['rows'][0]['elements'][0]['duration']['text']} for i in urls]

#turn urls into list of street addresses
	urls = [i["destination_addresses"][0].split(",")[0] for i in urls]
	#url_dict = {i+1: urls[i] for i in range(len(urls))}
#print(final_data)

#filter brewery data down to breweries within our selected distance
	JS = [i for i in JS if i['street'] in urls]
	for i in range(len(JS)):
		final_data[i]["name"] = JS[i]["name"]
	loc_data = ['+'.join(i['name'].split())+','+'+'.join(i['city'].split())+','+'+'.join(i['state'].split()) for i in JS]
	






	map_data = {i+1: loc_data[i] for i in range(len(loc_data))}
	map_data[0] = "+".join(addr.split()) + "," + "+".join(city.split()) + "," + "+".join(state.split('_'))
	graph = []
	for i in range(len(loc_data)+1):
		graph.append([])
	for i in range(len(loc_data)+1):
		graph[i].append(0)
		for j in range(i+1,len(loc_data)+1):
			val = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + map_data[i] + "&destinations=" + map_data[j] + "&key=").json()
			dist = val['rows'][0]['elements'][0]['distance']['text'].split()[0]
			new_num = ""
			for c in dist:
				if c != ',':
					new_num = new_num + c
			graph[i].append(float(new_num))
			graph[j].append(float(new_num))
	val = hamiltonian_beer_cycle(graph)
	#generate place data in order to obtain
	place = [requests.get("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+'%20'.join(i["name"].split())+"&inputtype=textquery&fields=place_id,photos,formatted_address,name,rating,opening_hours,geometry&key=").json() for i in JS]

	#obtain detailed data based on the place id generated by place array
	details = [requests.get("https://maps.googleapis.com/maps/api/place/details/json?place_id="+i["candidates"][0]["place_id"]+"&fields=website,formatted_phone_number,rating&key=").json() for i in place]

	for i in range(len(details)):
		final_data[i].update(details[i]['result'])
	sol = []
	for i in val[1][1:]:
		sol.append(final_data[i-1])
	for i in range(len(sol)):
		sol[i]["dist_from_last"] = graph[val[1][i]][val[1][i+1]]
	return sol


