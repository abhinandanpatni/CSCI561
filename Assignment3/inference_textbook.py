import sys
from copy import deepcopy 

queries = list()
knowledge_base = list()
standardizedVars = 0

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
class Complex:
	def __init__ (self, predicate, arguments):
		self.predicate = predicate	
		self.arguments = arguments
	def printComplex(self):
		print "Predicate: ", self.predicate
		print "Arguments: ", [i.value for i in self.arguments]

"""Every constant has a value. Starts with uppercase letter"""
class Constant:
	def __init__ (self, value):
		self.value = value
	def printConstant(self):
		print "Constant Value: ", self.value

"""Every variable has a value. Is a single lowercase letter"""
class Variable:
	def __init__ (self, value):
		self.value = value
	def printVariable(self):
		print "Variable value", self.value

"""Get predicate for a clause"""
def getPredicate(clause):
	return clause.split('(')[0]

"""Get list of arguments for a clause"""
def getConstants(clause):
	return clause.split('(')[1].split(')')[0].split(',')

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
			for const in getConstants(each):
				if const[0].islower():
					each_arg_list.append(Variable(const))
				else:
					each_arg_list.append(Constant(const))

			allAntecedents.append(Complex(each_predicate, each_arg_list))


		consequent_predicate = getPredicate(consequents)
		consequent_arg_list = list()
		for const in getConstants(consequents):
				if const[0].islower():
					consequent_arg_list.append(Variable(const))
				else:
					consequent_arg_list.append(Constant(const))

		finalConsequent = Complex(consequent_predicate, consequent_arg_list)
		knowledge_base.append(Clause(allAntecedents, finalConsequent))

	else:
		fact_predicate = getPredicate(clause)
		const_list = list()
		for eachConstant in getConstants(clause):
			# print eachConstant
			const_list.append(Constant(eachConstant))
		fact = Complex(fact_predicate, const_list)
		knowledge_base.append(Clause("FACT", fact))

def checkStandardizedVar(theta, var):
	return theta[var.value][:3] == "var"

def makeSubstitution(theta, sentence):
	if not theta:
		return deepcopy(sentence)
	else:
		temp_sentence = deepcopy(sentence)
		for index in range(len(sentence.arguments)):
			sentence_var = sentence.arguments[index]
			if isinstance(sentence_var, Variable) and sentence_var.value in theta:
				if not checkStandardizedVar(theta, sentence_var):
					temp_sentence.arguments[index] = Constant(theta[sentence_var.value])
				else:
					temp_sentence.arguments[index].value = theta[sentence_var.value]
		return temp_sentence


def makeCheck(variable, sentence, theta):
	if (isinstance(variable, Constant) and variable.value in theta) or (if isinstance(variable, (str, unicode)) and variable in theta):
		return True

def UNIFY_VAR(variable, sentence, theta):
	if variable.value in theta:
		return UNIFY(theta[variable.var], sentence, theta)
	elif makeCheck(variable, sentence, theta):
		return UNIFY(variable, theta[variable.value], theta)
	temp_theta = theta.copy()
	if not isinstance(variable, (str, unicode)):
		temp_theta[variable.value] = sentence.value
	else:
		temp_theta[variable.value] = sentence

	return temp_theta


"""Following the algorithm from the textbook"""
def UNIFY(sentence1, sentence2, theta = {}):
	if theta is None:
		return None:
	elif sentence1 == sentence2 or ((isinstance(sentence1,Constant) and isinstance(sentence2,Constant)) and sentence1.value == sentence2.value) :
		return theta
	elif isinstance(sentence1, Variable):
		return UNIFY_VAR(sentence1, sentence2, theta)
	elif isinstance(sentence2, Variable):
		return UNIFY_VAR(sentence2, sentence1, theta)
	elif isinstance(sentence1, Complex) and isinstance(sentence2, Complex):
		return UNIFY(sentence1.arguments, sentence2.arguments, UNIFY(sentence1.predicate, sentence2.predicate, theta))
	elif type(sentence1) == list and type(sentence2) == list and len(sentence1) == len(sentence2):
		return theta if len(sentence1) == 0 else UNIFY(sentence[1:], sentence2[1:], UNIFY(sentence1[1], sentence2[0], theta))
	else:
		return None

"""Localized standardization of every variable in clause"""
def Standardization(clause):
	global standardizedVars
	mapper_variable = dict()

	arguments_consequent = clause.consequent.arguments
	for eachArg in arguments_consequent:
		if isinstance(eachArg, Variable):
			if eachArg.value not in mapper_variable:
				mapper_variable[eachArg.value] = "var" + str(standardizedVars)
				eachArg.value = mapper_variable[eachArg.value]
				standardizedVars += 1
			else:
				eachArg.value = mapper_variable[eachArg.value]

	if clause.antecedent != "FACT":
		for eachClause in clause.antecedent:
			for argument in eachClause.arguments:
				if isinstance(argument, Variable):
					if argument.value not in mapper_variable:
						mapper_variable[argument.value] = "var" + str(standardizedVars)
						argument.value = mapper_variable[argument.value]
						standardizedVars += 1
					else:
						argument.value = mapper_variable[argument.value]

	return clause


"""According to textbook algorithm"""
def FOL_BC_OR(finalGoal, theta, explored = {}):
	pass

"""According to textbook algorithm"""
def FOL_BC_AND(allGoals, theta, explored):
	if theta is None:
		return
	if len(allGoals) == 0:
		yield theta
	else:
		firstGoal = allGoals[0]
		remainingGoals = allGoals[1:] if len(allGoals) > 1 else list()

		for someTheta in 

"""According to textbook algorithm"""
def FOL_BC_ASK(query):
	return FOL_BC_OR(query, {})

"""Main backward chain caller"""
def backwardChain():
	global queries

	outputFile = "output.txt"
	for eachQuery in queries:
		try:
			answer_map_gen = FOL_BC_ASK(eachQuery)

			if sum(1 for _ in answers_map_gen) > 0:
				with open(outputFile, "a") as opFile:
					opFile.write("TRUE\n")
			else:
				with open(outputFile, "a") as opFile:
					opFile.write("FALSE\n")
		except:
			with open(outputFile, "a") as opFile:
				opFile.write("FALSE\n")
  

"""Process the input. Get queries and knowledge base by the end of this."""
def processInput():
	global queries, knowledge_base
	with open(sys.argv[-1], 'r') as inputFile:
		numQueries = int(inputFile.readline())

		for i in range(numQueries):
			query = inputFile.readline().rstrip()
			query_predicate = getPredicate(query)
			const_list = list()
			for eachConstant in getConstants(query):
				const_list.append(Constant(eachConstant))
			queries.append(Complex(query_predicate, const_list))

		# for query in queries:
		# 	print query, [i for i in query.arguments]

		numClauses = int(inputFile.readline())

		for i in range(numClauses):
			clause = inputFile.readline().rstrip()
			processKBClause(clause)

		# for each in knowledge_base:
		# 	if each.antecedent == True:
		# 		pass
		# 	else:
		# 		for x in each.antecedent:
		# 			print x.predicate, [arg.value for arg in x.arguments]
			
		# 	print each.consequent.predicate, [arg.value for arg in each.consequent.arguments]

		backwardChain()


def main():
	processInput()

if __name__ == "__main__":
	main()