from copy import deepcopy
import sys

standardizedVars = 0
queries = list()
knowledge_base = list()
explored = list()

"""Queries and clauses have a general struct:
antecedent1 ^ antecedent2 ^... => consequent """
class Clause:
	def __init__ (self, antecedent, consequent):
		self.antecedent = antecedent
		self.consequent = consequent
	def printClause(self):
		print "Antecedent: ", [printComplex(i) for i in self.antecedent]
		print "Consequent: ", [printComplex(i) for i in self.consequent]

"""Every term in antecedent has a structure:
predicate(arguments)"""
class Term:
	def __init__ (self, predicate, arguments):
		self.predicate = predicate	
		self.arguments = arguments
	def printComplex(self):
		print "Predicate: ", self.predicate
		print "Arguments: ", [i.value for i in self.arguments]

"""Every constant has a value. Starts with uppercase letter"""
class FactVariable:
	def __init__ (self, value):
		self.value = value
	def printFactVariable(self):
		print "FactVariable Value: ", self.value

"""Every variable has a value. Is a single lowercase letter"""
class UnknownVariable:
	def __init__ (self, value):
		self.value = value
	def printUnknownVariable(self):
		print "UnknownVariable value", self.value

"""Get predicate for a clause"""
def getPredicate(clause):
	return clause.split('(')[0]

"""Get list of arguments for a clause"""
def getFactVariables(clause):
	return clause.split('(')[1].split(')')[0].split(',')

"""Get map of constants and how they map position wise"""
def getFactVariableMap(query):
	constants = query.split('(')[1].split(')')[0].split(',')
	constantDict = dict()
	index = 0
	for constant in constants:
		constantDict[index] = constant
		index += 1
	return constantDict

"""Check and return the correct value of the sentence/or variable of the sentence"""
def sentenceChecker(sentence):
	if isinstance(sentence, FactVariable):
		return sentence.value
	elif isinstance(sentence, (str,unicode)):
		return sentence
	else:
		return None

"""Checks in sentence is in theta or not"""
def sentenceInTheta(sentence, theta):
	if isinstance(sentence, FactVariable) and sentence.value in theta:
		return True
	elif isinstance(sentence, (str,unicode)) and sentence in theta:
		return True
	else:
		return False

"""Checks if the variable has been standardized or not"""
def checkStandardizedVar(theta, var):
	# return theta[var.value][:3] == "var"
	return theta[var.value].isdigit()

"""UNIFY_VAR according to textbook"""
def UNIFY_VAR(variable, sentence, theta):
	if variable.value in theta:
		return UNIFY(theta[variable.value], sentence, theta)
	elif sentenceInTheta(sentence, theta):
	# elif makeCheck(variable, sentence, theta):
		return UNIFY(variable, theta[sentenceChecker(sentence)], theta)
	temp_theta = theta.copy()
	if not isinstance(variable, (str, unicode)):
		temp_theta[variable.value] = sentence.value
	else:
		temp_theta[variable.value] = sentence

	return temp_theta

"""UNIFY according to textbook"""
def UNIFY(sentence1, sentence2, theta = {}):
	if theta is None:
		return None
	elif (sentenceChecker(sentence1) == sentenceChecker(sentence2)) and (sentenceChecker(sentence1) is not None):
		return theta
	elif isinstance(sentence1, UnknownVariable):
		return UNIFY_VAR(sentence1, sentence2, theta)
	elif isinstance(sentence2, UnknownVariable):
		return UNIFY_VAR(sentence2, sentence1, theta)
	elif isinstance(sentence1, Term) and isinstance(sentence2, Term):
		return UNIFY(sentence1.arguments, sentence2.arguments, UNIFY(sentence1.predicate, sentence2.predicate, theta))
	elif type(sentence1) is list and type(sentence2) is list and len(sentence1) == len(sentence2):
		if len(sentence1) == 0:
			return theta
		return UNIFY(sentence1[1:], sentence2[1:], UNIFY(sentence1[0], sentence2[0], theta))
	else:
		return None

"""SUBS according to textbook"""
def makeSubstitution(theta, sentence):
	if theta is None:
		return deepcopy(sentence)
		# return deepcopy(sentence)
	else:
		temp_sentence = deepcopy(sentence)
		for index in range(len(sentence.arguments)):
			sentence_var = sentence.arguments[index]
			if isinstance(sentence_var, UnknownVariable) and sentence_var.value in theta:
				if not checkStandardizedVar(theta, sentence_var):
					temp_sentence.arguments[index] = FactVariable(theta[sentence_var.value])
				else:
					temp_sentence.arguments[index].value = theta[sentence_var.value]
		return temp_sentence

"""Process a clause in the knowledge base and append it to the knowledge base"""
def processKBClause(clause):
	global knowledge_base

	if " => " in clause:
		antecedents = [x for x in clause.split(" => ")[0].split(" ^ ")]
		consequents = clause.split(" => ")[1]

		allAntecedents = list()
		for each in antecedents:
			each_arg_list = list()
			each_predicate = getPredicate(each)
			for const in getFactVariables(each):
				if const[0].islower():
					each_arg_list.append(UnknownVariable(const))
				else:
					each_arg_list.append(FactVariable(const))

			allAntecedents.append(Term(each_predicate, each_arg_list))


		consequent_predicate = getPredicate(consequents)
		consequent_arg_list = list()
		for const in getFactVariables(consequents):
				if const[0].islower():
					consequent_arg_list.append(UnknownVariable(const))
				else:
					consequent_arg_list.append(FactVariable(const))

		finalConsequent = Term(consequent_predicate, consequent_arg_list)
		knowledge_base.append(Clause(allAntecedents, finalConsequent))

	else:
		fact_predicate = getPredicate(clause)
		const_list = list()
		for eachFactVariable in getFactVariables(clause):
			# print eachFactVariable
			const_list.append(FactVariable(eachFactVariable))
		fact = Term(fact_predicate, const_list)
		knowledge_base.append(Clause("", fact))


"""Basically adds the standardizedVars number to the dict of standardizedVars"""
def Standardization(clause):
	global standardizedVars
	mapper_variable = dict()

	arguments_consequent = clause.consequent.arguments
	for eachArg in arguments_consequent:
		if isinstance(eachArg, UnknownVariable):
			if eachArg.value not in mapper_variable:
				# mapper_variable[eachArg.value] = 'var' + str(standardizedVars)
				mapper_variable[eachArg.value] = str(standardizedVars)
				eachArg.value = mapper_variable[eachArg.value]
				standardizedVars += 1
			else:
				eachArg.value = mapper_variable[eachArg.value]

	if clause.antecedent != "":
		for eachTerm in clause.antecedent:
			for eachArg in eachTerm.arguments:
				if isinstance(eachArg, UnknownVariable):
					if eachArg.value not in mapper_variable:
						# mapper_variable[eachArg.value] = 'var' + str(standardizedVars)
						mapper_variable[eachArg.value] = str(standardizedVars)
						eachArg.value = mapper_variable[eachArg.value]
						standardizedVars += 1
					else:
						eachArg.value = mapper_variable[eachArg.value]
	return clause

"""FOL_BC_AND according to textbook"""
def FOL_BC_AND(allGoals, theta, explored):
	if theta is None:
		pass
	elif len(allGoals) == 0 or allGoals == True:
		yield theta
	else:
		firstGoal = allGoals[0]
		remainingGoals = allGoals[1:] if len(allGoals) > 1 else list()
		for theta_dash in FOL_BC_OR(makeSubstitution(theta, firstGoal), theta, explored):
			for theta_dash_2 in FOL_BC_AND(remainingGoals, theta_dash, explored):
				yield theta_dash_2


"""FOL_BC_OR according to textbook. Checks for visited nodes. Adds when necessary"""
def FOL_BC_OR(finalGoal, theta, explored={}):
	for index in range(len(knowledge_base)):
		tempExplored = explored
		clause = Standardization(knowledge_base[index])
		temp_theta = UNIFY(clause.consequent, finalGoal, theta)
		if temp_theta is not None:
			subbedConsequent = makeSubstitution(temp_theta, clause.consequent)
			if not isExplored(index, subbedConsequent, explored):
				updatedExplored = deepcopy(explored)
				for argument in subbedConsequent.arguments:
					if not isinstance(argument, FactVariable):
						tempExplored = updatedExplored
						break
					try:
						updatedExplored[index].append(subbedConsequent)
					except:
						updatedExplored[index] = [subbedConsequent]

				tempExplored = updatedExplored
			else:
				continue
		for theta_dash in FOL_BC_AND(clause.antecedent, temp_theta, tempExplored):
			yield theta_dash

# def addToExplored(index, term, explored):
# 	new_explored = deepcopy(explored)
# 	for argument in term.arguments:
# 		if not isinstance(argument, FactVariable):
# 			return new_explored
# 	try:
# 		new_explored[index].append(term);
# 	except:
# 		new_explored[index] = [term]
# 	return new_explored

"""Function to check explored nodes"""
def isExplored(index, term, explored):
	visited = False
	if index not in explored:
		return False
	else:
		for each in explored[index]:
			for i in range(len(each.arguments)):
				if isinstance(term.arguments[i], FactVariable):
					if term.arguments[i].value == each.arguments[i].value:
						visited = True
				if isinstance(term.arguments[i], UnknownVariable):
					return False
		return visited

"""FOL_BC_ASK according to textbook"""
def FOL_BC_ASK(query):
	return FOL_BC_OR(query, dict())

"""Main caller"""
def backwardChain():
	global queries

	outputFile = open("output.txt", "w")

	for query in queries:
		try:
			FOL_BC_ASK(query).next()
			print "TRUE\n"
			outputFile.write("TRUE\n")
		except:
			print 'FALSE\n'
			outputFile.write("FALSE\n")

	outputFile.close()

"""Function to process input"""
def processInput():
	global queries
	with open(sys.argv[-1], 'r') as inputFile:
		num_queries = int(inputFile.readline())
		for x in range(num_queries):
			query = inputFile.readline().rstrip()
			constantMap = getFactVariableMap(query)
			query_predicate = getPredicate(query)
			const_list = list()
			for eachFactVariable in getFactVariables(query):
				const_list.append(FactVariable(eachFactVariable))
			queries.append(Term(query_predicate, const_list))

		numClauses = int(inputFile.readline())

		for i in range(numClauses):
			clause = inputFile.readline().rstrip()
			processKBClause(clause)

	backwardChain()
	

def main():
	processInput()

if __name__ == "__main__":
	main()
