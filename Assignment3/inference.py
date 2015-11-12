import sys

def backwardChain(queryList, facts, antecedents, consequents):
	for query in queryList:
		""" Query is also a clause in the clauses """
		if query in facts:
			print True
		else:
			""" Actual algorithm starts here """
			# print query.split('(')[0]
			# print [x.split('(')[0] for x in consequents]
			if query.split('(')[0] not in [x.split('(')[0] for x in consequents]:
				print False
			else:
				print "Need to do this"


def processInput():
	with open(sys.argv[-1], 'r') as inputFile:
		inputList = [line.rstrip() for line in inputFile.readlines()]

		count = 0	#To keep track of which line is being processed

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

		facts, antecedents, consequents = list(), list(), list()
		"""Get all antecedents and consequents"""
		for clause in clauseList:
			if "=>" in clause:
				dissectedClause = clause.split(" => ")
				antecedents.append(dissectedClause[0])
				consequents.append(dissectedClause[1])
			else:
				facts.append(clause)

		print facts
		print antecedents
		print consequents
		# print numClauses
		# print clauseList

		backwardChain(queryList, facts, antecedents, consequents)

def main():
	processInput()

if __name__ == "__main__":
	main()