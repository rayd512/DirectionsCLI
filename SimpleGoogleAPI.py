import requests
import json
import re


def processStatus(code):
	if code == 400:
		print("Bad Request, please try again")
	elif code == 401:
		print("Not authenticated, please check API Key")
	elif code == 403:
		print("Access is prohibited, please try again")
	elif code == 404:
		print("Could not find resource, please try again")
	elif code == 503:
		print("The server was not ready to handle your request, please try again")
	else:
		print("Oops, something went wrong! Please try again")

def removeTags(htmlText):
	pattern = re.compile('<.*?>')
	regText = re.sub(pattern, '', htmlText)
	return regText

def printDirections(steps):
	counter = 0
	for step in steps:
		distance = step['distance']['text']
		duration = step['duration']['text']
		start_lat = step['start_location']['lat']
		start_lng = step['start_location']['lng']
		end_lat = step['end_location']['lat']
		end_lng = step['end_location']['lng']
		instr = removeTags(step['html_instructions'])

		if not counter:
			startString = "Starting at {}, {}, {} for {} to {}, {} for {}".format(
				start_lat, start_lng, instr, distance, end_lat, end_lng, duration)
			print(startString)

		else:
			nextString = "Then {} for {} to {}, {} for {}".format(
				instr, distance, end_lat, end_lng, duration)
			print(nextString)

		counter += 1
		

def processResponse(response):
	routes = response.json()['routes']
	leg = routes[0]['legs']
	distance = leg[0]['distance']['text']
	duration = leg[0]['duration']['text']
	start_address = leg[0]['start_address']
	end_address = leg[0]['end_address']

	print("Found a route from " + start_address + " to " + end_address + 
		". It is " + distance + " and will take " + duration + ".")

	printDir = input("Would you like to print the directions? (Y/n)\n").lower()

	if printDir == "y":
		printDirections(leg[0]['steps'])

def getRequest():
	endpoint = "https://maps.googleapis.com/maps/api/directions/json?"
	api_key = # INSERT API KEY HERE

	while True:
		origin = input("Where are you starting from?\n").replace(" ", "+")
		destination = input("Where are you going to?\n").replace(" ", "+")

		request = endpoint + 'origin={}&destination={}&key={}'.format(origin,
																destination,
																api_key)
		response = requests.get(request)
		status = response.status_code

		if(status == 200 or status == 301):
			break

		else:
			processStatus()

	processResponse(response)

def main():
	getRequest()

if __name__ == '__main__':
	main()
