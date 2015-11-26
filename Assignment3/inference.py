import sys
from copy import deepcopy

facts, clauses = list(), dict()

def getPredicate(clause):
	return clause.split('(')[0]

def getConstants(clause):
	return tuple(clause.split('(')[1].split(')')[0].split(','))

def getConstantMap(query):
	constants = query.split('(')[1].split(')')[0].split(',')
	constantDict = dict()
	index = 0
	for constant in constants:
		constantDict[index] = constant
		index += 1
	return constantDict

def getValidValues(constantDict, variableDict, posMap):
	validValues = dict()
	for key in variableDict:
		for innerKey in posMap:
			if key in posMap[innerKey] and innerKey in constantDict:
				try:
					validValues[key].extend(constantDict[innerKey])
					# print "Entering try"
					# print "Constant being printed here", constantDict[innerKey]
				except:
					# print "Entering except"
					# print "Constant being printed here", constantDict[innerKey]
					validValues[key] = constantDict[innerKey]
			elif key not in validValues:
				validValues[key] = []
	return validValues

def getValidConstants(query_predicate):
	if query_predicate in [getPredicate(x) for x in facts]:
		"""If something found in facts, create a dictionary of valid values and send it up"""
		validConstants = dict()
		for singleFact in facts:
			if query_predicate == getPredicate(singleFact):
				factConstants = getConstants(singleFact)
				print factConstants
				const_index = 0
				for eachConstant in factConstants:
					if const_index in validConstants:
						if eachConstant not in validConstants[const_index]:
							validConstants[const_index].append(eachConstant)
							
					else:
						validConstants[const_index] = [eachConstant]

					const_index += 1

		return validConstants

	else:
		"""Nothing was found in the facts with the same query predicate. Return empty dict or something weird"""
		return {}

def createPosMap(query_predicate, rule):
	global clauses
	query_constant_list = tuple()
	rule_constant_list = rule.split('(')[1].split(')')[0].split(',')
	posMap = dict()
	for key in clauses:
		if query_predicate == key[0]:
			query_constant_list = key[1]

	unmappedList = deepcopy(rule_constant_list)
	for index in range(len(query_constant_list)):
		posMap[index] = [i for i, x in enumerate(rule_constant_list) if x == query_constant_list[index]]
		unmappedList = filter(lambda a: a != query_constant_list[index], unmappedList)

	return posMap, unmappedList

def getRules(query_predicate):
	global clauses
	for key in clauses:
		if key[0] == query_predicate:
			return clauses[key]
	return "noRuleFound"

def backwardChain(query_predicate, query_constant, unmappedList, explored):
	global facts
	"""Creating a dictionary of valid constant values.
	keys are positions of the constant in the query. Integers.
	values are all possible values of the constant. List."""
	index = 0
	constantDict = dict()
	for each in query_constant:
			constantDict[index] = query_constant[each]
			index += 1
	
	if [query_predicate, query_constant] in explored:
		print "Duplicate!"
		return

	explored.append([query_predicate, query_constant])


	"""Handle single antecedent => consequent and also antecedent1 ^ antecedent2 ^ ... => consequent"""
	rules = getRules(query_predicate)
	
	print rules

	"""Check if any form of predicate with values from constantDict is in facts.
	if True for all, send back constant dict. Else, modify constantDict to get only constants with true values. If none found, proceed."""

	if rules == "noRuleFound":
		return getValidConstants(query_predicate)
		

	else:
		"""Also generate position mapping for variables between current query and the rule you're going to explore.
	keys are original position in this query. Values are mappings in the rule you're going to explore.
	For e.g. H(x) => A(x). Here, 0:0. 
	H(y,x) => A(x,y). Here, 0:1, 1:0
	H(y,y) => A(x,y). Here, 0:1, 1:1
	There will be some bizarre cases where there are no mappings at all. In that case, dictionary is empty. Handle that somehow (Maybe allow everything, since no constraint)"""
		for eachRule in rules:
			if '^' in eachRule:
				"""Create a position map for every rule. Recursively call backward chaining on each rule that is mapped. Then, find intersection between
				every antecedent to generate a valid set of values."""
				singleClauseList = eachRule.split(' ^ ')
				for single in singleClauseList:
					posMap, unmappedValues =  createPosMap(query_predicate, single)
					# print posMap, unmappedValues
					single_predicate = getPredicate(single)
					single_constant = getConstantMap(single)
					# print "Getting valid values for ", constantDict, single_constant, posMap
					validValues = getValidValues(constantDict, single_constant, posMap)
					# print "Valid Values", validValues
					# print "Now calling backward for ", single_predicate, single_constant
					"""This should return a dictionary. 
					Do an intersection of that dict with constantDict. Return the intersection"""
					returnedConstDict = backwardChain(single_predicate, validValues, unmappedValues, explored)
			else:
				"""Create a position map for the rule. Call backward chaining on it to return the set of possible values for constants"""
				posMap, unmappedValues = createPosMap(query_predicate, eachRule)
				# print posMap, unmappedValues
				rule_predicate = getPredicate(eachRule)
				rule_constant = getConstantMap(eachRule)
				# print "Getting valid values for ", constantDict, rule_constant, posMap
				validValues = getValidValues(constantDict, rule_constant, posMap)
				# print "Valid Values", validValues
				# print "Now calling backward for ", rule_predicate, rule_constant
				# print validValues
				returnedConstDict = backwardChain(rule_predicate, validValues, unmappedValues, explored)


	return


def processInput():
	global facts, antecedents, consequents

	with open(sys.argv[-1], 'r') as inputFile:
		inputList = [line.rstrip() for line in inputFile.readlines()]

		count = 0   #To keep track of which line is being processed

		"""Get all the queries"""
		numQueries = int(inputList[count])
		queryList = list()
		for i in range(numQueries):
			count += 1
			queryList.append(inputList[count])
		# print numQueries
		# print queryList

		count += 1

		"""Get all the knowledge base clauses"""
		numClauses = int(inputList[count])
		clauseList = list()
		for i in range(numClauses):
			count += 1
			clauseList.append(inputList[count])
		
		"""Get dictionary of clauses. Keys = consequents. Values = antecedents"""
		for each in clauseList:
			if "=>" in each:
				dissectedClause = each.split(" => ")
				antecedent = dissectedClause[0]             
				predicate = getPredicate(dissectedClause[1])
				constants = getConstants(dissectedClause[1])
				clauseKey = tuple([predicate, constants])
				try:    
					clauses[clauseKey].append(antecedent)
				except:
					clauses[clauseKey] = [antecedent]
			else:
				facts.append(each)

		print queryList
		print clauses
		print facts

		for query in queryList:
			explored, unmappedList = list(), list()
			query_predicate = getPredicate(query)
			query_constant = getConstantMap(query)
			# print query_predicate, query_constant, explored
			# print getRules(query_predicate)
			returnedDict = backwardChain(query_predicate, query_constant, unmappedList, explored)
			answer = True
			"""TODO: Match the returned dictionary to the query constants """
			# for eachKey in returnedDict:
			#     if returnedDict[eachKey] == query_constant[eachKey]:
			#         answer &= True
			#     else:
			#         answer &= False
			print answer

def main():
	processInput()

if __name__ == "__main__":
	main()