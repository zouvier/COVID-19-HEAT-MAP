import folium
import pandas as pd
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
	test = df1.loc[df1['date'] == '3/10/2020'].fillna(0)
	print(test)
	test2 = test.set_index('iso_code', drop=True)
	#test.reset_index(inplace=True)
	print(test2.index)
	map1 = folium.Map(location=[0, 0], zoom_start=6, tiles='OpenStreetMap')
	fg = folium.FeatureGroup(name='My Map')


	# test2 = test1.set_index('iso_code', drop=True)
	fg.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=lambda z: {'fillColor': 'YlOrRd' if z['properties']['ISO3'] in test2.index else 'Red'}))
	#test2[z['properties']['ISO3'],'total_cases_per_million']

	for i in test.index:
		fg.add_child(folium.Marker(location=[(test.loc[i, 'Latitude']), (test.loc[i, 'Longitude'])], popup=test.loc[i, 'total_cases_per_million'], icon=folium.Icon(color='red')))



	#fg.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read()))

	map1.add_child(fg)

	map1.save('test1.html')

def functown(pdata,z):
	if z in pdata.index:
		try:
			value = pdata.loc[z, 'total_cases_per_million']
			print(value)
			return int(value)
		except(ValueError, KeyError):
			return 0





# test function to read a file
def testing():
	file = open('CountryCodes1','r+')
	for i in file:
		print(i)
	file.close()
holder()
