import re
from copy import deepcopy 
import sys

queries = list()
knowledge_base = list()

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
		knowledge_base.append(Clause(True, fact))

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


def main():
	processInput()

if __name__ == "__main__":
	main()