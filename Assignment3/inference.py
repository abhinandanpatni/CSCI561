import sys

def backwardChain(queryList, clauseList):
	pass

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

		# print numClauses
		# print clauseList

		backwardChain(queryList, clauseList)

def main():
	processInput()

if __name__ == "__main__":
	main()