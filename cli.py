#!/usr/local/bin/python3

from faker import Faker
import argparse
import time

def welcome():
    print("""
 _______    ___       __  ___  _______  _______   ______  __       __  
|   ____|  /   \     |  |/  / |   ____||       \ /      ||  |     |  | 
|  |__    /  ^  \    |  '  /  |  |__   |  .--.  |  ,----'|  |     |  | 
|   __|  /  /_\  \   |    <   |   __|  |  |  |  |  |     |  |     |  | 
|  |    /  _____  \  |  .  \  |  |____ |  '--'  |  `----.|  `----.|  | 
|__|   /__/     \__\ |__|\__\ |_______||_______/ \______||_______||__| 
    """)
    print("--- Starting FakedCLI! ---")
    print("Starting program in 5 seconds...")
    time.sleep(5)

faker = Faker()

def phone():
     return faker.phone_number()

def name():
     return faker.name()

def email():
     return faker.email()

def address():
	return faker.address()

def company():
	return faker.company()

def ssn():
	return faker.ssn()

# Lookup table for the appropriate function to run
def lookup_table(number):
	d = {
		0 : "phone",
		1 : "name",
		2 : "email",
		3 : "address",
		4 : "company",
		5 : "ssn"
	}
	try:
		return(d[number])
	except KeyError:
		return False

dispatcher = {
	0 : phone,
	1 : name,
	2 : email,
	3 : address,
	4 : company,
	5 : ssn
}

def to_file(filename, content):
	filename = str(filename) + ".sql"
	try:
		f = open(filename, "x")
		content = "\n".join(content)
		f.write(content)
		f.close()
	except FileExistsError as e:
		print ("File already exists, unable to write!", e)

def output(limbo, tableName, count, chunking):
	queries = []
	number=0
	for x in range(count):
		queries.append(generate_data(limbo, tableName))
		if (chunking > 1):
			start=chunking-1
			stop=chunking
			if (queries[start::stop]):
				to_file(number, queries)
				number += 1
				del queries[:]
				queries = []
	to_file(number, queries)

def generate_data(limbo, tableName):
	countValues = len(limbo)
	lastCount = countValues - 1
	query = []
	query.append("INSERT INTO " + tableName + " (")
	for x in range(countValues):
		if (x == lastCount):
			query.append("`" + lookup_table(limbo[-1]) + "`")
		else:
			query.append("`" + lookup_table(limbo[x]) + "`,")
	query.append(") VALUES (")
	for x in range(countValues):
		if (x == lastCount):
			query.append('"' + dispatcher[x]() + '"')
		else:
			query.append('"' + dispatcher[x]() + '", ')
	query.append(");")
	return "".join(query)

# Argument Parsing
if (__name__ == "__main__"):
	parser = argparse.ArgumentParser(description="Arguments for FakedCLI Data Generator", allow_abbrev=True)
	parser.add_argument("-b", help="Boolean argument to bypass welcome and wait time", default=False)
	parser.add_argument("-c", "--count", help="Number of times to generate dummy data", default=1, type=int)
	parser.add_argument("--chunk", help="Chunk inserts by number of insert rows. Set to 0 if no chunking is desired.", default=1000, type=int)
	parser.add_argument("-t", "--table", help="Name of table to insert or delete from", default="fakercli")
	parser.add_argument("--phone-number", help="Generate a phone number", default=False, action="store_true", dest="phone")
	parser.add_argument("--name", help="Generate a full name", default=False, action="store_true", dest="name")
	parser.add_argument("--email", help="Generate an email", default=False, action="store_true", dest="email")
	parser.add_argument("--address", help="Generate a random address", default=False, action="store_true", dest="address")
	parser.add_argument("--company", help="Generate a random company", default=False, action="store_true", dest="company")
	parser.add_argument("--ssn", help="Generate a random fake ssn", default=False, action="store_true", dest="ssn")
	args = parser.parse_args()

	if (args.b == False):
		welcome()

	if (args.chunk < 2):
		chunking = 0
	else:
		chunking = args.chunk

	limbo = []
	if (args.phone):
		limbo.append(0)
	if (args.name):
		limbo.append(1)
	if (args.email):
		limbo.append(2)
	if (args.address):
		limbo.append(3)
	if (args.company):
		limbo.append(4)
	if (args.ssn):
		limbo.append(5)

	output(limbo, args.table, args.count, chunking)