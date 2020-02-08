#!/usr/local/bin/python3

from faker import Faker
import argparse

def welcome():
    print("""
     _______    ___       __  ___  _______ .______        ______  __       __  
    |   ____|  /   \     |  |/  / |   ____||   _  \      /      ||  |     |  | 
    |  |__    /  ^  \    |  '  /  |  |__   |  |_)  |    |  ,----'|  |     |  | 
    |   __|  /  /_\  \   |    <   |   __|  |      /     |  |     |  |     |  | 
    |  |    /  _____  \  |  .  \  |  |____ |  |\  \----.|  `----.|  `----.|  | 
    |__|   /__/     \__\ |__|\__\ |_______|| _| `._____| \______||_______||__| 
    """)
    print("--- Starting FakedCLI! ---")

faker = Faker()

def phone():
	return faker.phone_number()

def name():
	return faker.name()

def email():
	return faker.email()

def address():
	return faker.address()

# Lookup table for the appropriate function to run
def lookup_table(number):
	d = {
		0 : "phone",
		1 : "name",
		2 : "email",
		3 : "address"
	}
	try:
		return(d[number])
	except KeyError:
		return False

dispatcher = {
	0 : phone,
	1 : name,
	2 : email,
	3 : address
}

def output(limbo, tableName, count):
	for _ in range(count):
		generate_data(limbo, tableName)

def generate_data(limbo, tableName):
	countValues = len(limbo)
	lastCount = countValues - 1
	print("INSERT INTO " + tableName + " (", end='')
	for x in range(countValues):
		if (x == lastCount):
			print("`" + lookup_table(limbo[-1]) + "`", end='')
		else:
			print("`" + lookup_table(limbo[x]) + "`,", end='')
	print(") VALUES (", end='')
	for x in range(countValues):
		if (x == lastCount):
			print('"' + dispatcher[x]() + '"', end='')
		else:
			print('"' + dispatcher[x]() + '", ', end='')
	print(");")

# Argument Parsing
if (__name__ == "__main__"):
	parser = argparse.ArgumentParser(description="Arguments for FakedCLI Data Generator", allow_abbrev=True)
	parser.add_argument("-c", "--count", help="Number of times to generate dummy data", default=1, type=int)
	parser.add_argument("-t", "--table", help="Name of table to insert or delete from", default="fakercli")
	parser.add_argument("--phone-number", help="Generate a phone number", default=False, action="store_true", dest="phone")
	parser.add_argument("--name", help="Generate a full name", default=False, action="store_true", dest="name")
	parser.add_argument("--email", help="Generate an email", default=False, action="store_true", dest="email")
	parser.add_argument("--address", help="Generate a random address", default=False, action="store_true", dest="address")
	args = parser.parse_args()

	limbo = []
	if (args.phone):
		limbo.append(0)
	if (args.name):
		limbo.append(1)
	if (args.email):
		limbo.append(2)
	if (args.address):
		limbo.append(3)

	output(limbo, args.table, args.count)