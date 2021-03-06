import folium
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# TODO: - allow user to change the date of the depicted data through the web page
#       - add chloropeth to the map to help depict which countries are faring the worst with C19
#

# Develops the map in folium with markers on the country displaying information within the data frame
def holder():
	# Covid 19 data for each country
	# world = pd.read_json('world.json')
	# world.to_csv()
	# print(world)
	data = pd.read_csv('covid.csv')
	# Country codes to map each country to folium
	ccode = pd.read_csv('CountryCodes1.txt')
	df1 = pd.DataFrame(data)
	df2 = pd.DataFrame(ccode).set_index('alpha3')
	long = []
	lat = []
	# adds each countries latitude and longtitude coordinates to the list
	for x in df1['iso_code']:
		try:
			lat.append((df2.loc[x, 'latitude']))
			long.append((df2.loc[x, 'longitude']))
		except:
			continue
	# Adds the longitude, and latitude data to the dataframe consisting of the covid 19 data of each country
	df1.loc[:, 'Latitude'] = pd.Series(lat)
	df1.loc[:, 'Longitude'] = pd.Series(long)
	# date = input('Enter date 1/1/2020 format')
	# pick which date you want to be depicted
	test = df1.loc[df1['date'] == '7/14/2020'].fillna(0)
	print(test)
	test2 = test.set_index('iso_code', drop=True)
	#test.reset_index(inplace=True)
	#print(test2.index)
	map1 = folium.Map(location=[0, 0],max_bounds=True, zoom_start=3, min_zoom=2, tiles='OpenStreetMap')
	fg = folium.FeatureGroup(name='Current spread of Corona Virus')



	# test2 = test1.set_index('iso_code', drop=True)
	fg.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=lambda z: {'fillColor': color(test2, z['properties']['ISO3']) if functown(test2, z['properties']['ISO3']) != 0 else color(test2, z['properties']['ISO3'])}))
	#test2[z['properties']['ISO3'],'total_cases_per_million']

	for i in test.index:
		fg.add_child(folium.Marker(location=[(test.loc[i, 'Latitude']), (test.loc[i, 'Longitude'])], popup= graph(test,i), icon=folium.Icon(color='red')))




	#fg.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read()))

	map1.add_child(fg)

	map1.save('test1.html')


def graph(gdata, i):
	return ('<b><font color=red> Date:</font></b> ' + str(gdata.loc[i,'date']) + '<br>' +
	        '<b><font color=red>Country:</font></b> '+str(gdata.loc[i, 'location']) + '<br>' +
	        '<b><font color=red>cases:</font></b> '+str(gdata.loc[i,'total_cases']) + '<br>' +
	        '<b><font color=red>deaths:</font></b> '+ str(gdata.loc[i,'total_deaths']))




def functown(pdata,z):
	if z in pdata.index:
		value = pdata.loc[z, 'total_cases_per_million']
		#print(value)
		return int(value)
	else:
		return 0

def color(pdata,z):
	if z in pdata.index:
		value = pdata.loc[z, 'total_cases_per_million']
		if value == 0:
			return 'White'
		elif value <= 200:
			return 'Yellow'
		elif value > 200 and value < 1000:
			return '#fc4503'
		elif value >= 1000:
			return '#fc03eb'



# test function to read a file
def testing():
	file = open('CountryCodes1','r+')
	for i in file:
		print(i)
	file.close()

holder()
