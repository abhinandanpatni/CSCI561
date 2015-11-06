import sys

def BFS(graph, source, destinationList, startTime):
	node = source
	# print node
	# print graph[node]
	if node in destinationList:
		return node
	frontier = []
	cameFrom = []
	frontier.append(node)
	explored = []
	while 1:
		if len(frontier) == 0:
			return False
		poppedNode = frontier.pop(0)
		explored.append(poppedNode)
		if poppedNode in graph:
			for child in graph[poppedNode]:
				if child not in frontier or child not in explored:
						if child in destinationList:
								cameFrom.append([child, poppedNode])
								answer = child
								path = [child]
								while 1:
									for lists in cameFrom:
										if lists[0] is child:
											path.append(lists[1])
											child = lists[1]
											if child in source:
												#print list(reversed(path))
												#print len(path)
												return answer, (startTime + len(path)-1)%24
						else:
							frontier.append(child)
							cameFrom.append([child, poppedNode])


def RecursiveDFS(graph, source, destinationList, startTime, frontier, explored, node, cameFrom):
	if len(frontier) == 0:
		return 'None'

	if node in destinationList:
		actualAnswer = node
		path = [node]
		while 1:
			for lists in cameFrom:
				if lists[0] is node:
					path.append(lists[1])
					node = lists[1]
					if node in source:
						#print list(reversed(path))
						#print len(path)
						return [actualAnswer, (startTime + len(path)-1)%24]
	else:
		if node not in graph or graph[node] in explored:
			explored.append(node)
			frontier.remove(node)
		else:
			for child in graph[node]:
				if child not in frontier:
					global callFrom
					frontier.append(child)
					cameFrom.append([child, node])
					answer = RecursiveDFS(graph, source, destinationList, startTime, frontier, explored, child, cameFrom)
					if answer is None:
						if len(frontier) == 0:
							return 'None'
					elif answer[0] in destinationList:
						return answer

def DFS(graph, source, destinationList, startTime):
	node = source
	if node in destinationList:
		return node
	else:
		frontier = []
		frontier.append(node)
		explored = []
		cameFrom = []
		answer =  RecursiveDFS(graph, source, destinationList, startTime, frontier, explored, node, cameFrom)
		return answer

def UCS(graph, source, destinationList, startTime, lengths, offTimeList):
	node = source
	if node in destinationList:
		return node

	frontier = []
	reachTimes = []
	reachTimes.append([node, startTime])
	frontier.append([node, 0])
	#print frontier
	explored = []

	#for xxx in range(0,20):
	while 1:
		if len(frontier) == 0:
			return 'None'

		poppedNode = frontier.pop(0)
		
		if poppedNode[0] in destinationList:
			return poppedNode

		explored.append(poppedNode)

		inFrontier = 0
		inExplored = 0
		
		#update the costs first
		if poppedNode[0] in graph:
			#print "Entered update cost block"
			#print poppedNode
			#print frontier
			for child in graph[poppedNode[0]]:
				inExplored = 0
				inFrontier = 0
				canAdd = True
				#print child
				#Adding check to see if this node can even be added to the frontier or not
				for lists in lengths:
					temp = lists
					if poppedNode[0] == temp[0] and child == temp[1]:
						#costChild = poppedNode[1] + temp[2]
						#print costChild
						# canAdd = True
						for times in offTimeList:
							if poppedNode[0] == times[0] and child == times[1]:
								if times[2] > 0:
									for i in range(1, times[2]+1):
										timePeriod = [int(x) for x in times[2+i].split('-')]
										# print "Time period under consideration is ", timePeriod
										# print "poppedNode time is ", poppedNode[1]
										if poppedNode[1] >= timePeriod[0] and poppedNode[1] <= timePeriod[1]:
											canAdd = False
											#print poppedNode[0]
											#print "Can Add is false for", child
				#check ended
				if canAdd == True:
					#print "Can add is true for ", child
					for frontierElements in frontier:
						if child in frontierElements:
							inFrontier = 1
							for lists in lengths:
								temp = lists
								if poppedNode[0] == temp[0] and child == temp[1]:
									if poppedNode[1] + temp[2] < frontierElements[1]:
										frontier.remove(frontierElements)
					for exploredElements in explored:
						if child in exploredElements:
							inExplored = 1
					#print explored, "explored", inExplored
					#if not inFrontier or not inExplored:
					if not inExplored:
						#print 'entered with ', child
						for lists in lengths:
							temp = lists
							if poppedNode[0] == temp[0] and child == temp[1]:
								costChild = poppedNode[1] + temp[2]
								# canAdd = True
								# for times in offTimeList:
								# 	if times[2] > 0:
								# 		for i in range(1, times[2]+1):
								# 			timePeriod = [int(x) for x in times[i].split('-')]
								# 			if costChild >= timePeriod[0] and costChild <= timePeriod[1]:
								# 				canAdd = False
								if canAdd == True:				
									frontier.append([child, costChild])
									reachTimes.append([child, startTime + costChild])
									frontier.sort(key=lambda x: x[::-1])
									#print frontier, "sorted"
							#print frontier
							#print reachTimes


def structureData(problemList, outputFile):
	#print problemList
		source = problemList[1]
		destination = problemList[2].split(' ')
		intermediate = problemList[3].split(' ')

		#counting the number of all nodes to convert to matrix format
		numNodes = len(source) + len(destination) + len(intermediate)
		numConnections = int(problemList[4])

		#getting the connections as dictionary
		graph = dict()
		for i in range(1, numConnections+1):
			#Adding to the graph dict. Appending as and when necessary to a list (for values) for each key.
			if problemList[4+i].split(' ')[0] in graph:
				graph[problemList[4+i].split(' ')[0]].append(problemList[4+i].split(' ')[1])
			else:
				graph[problemList[4+i].split(' ')[0]] = list()
				graph[problemList[4+i].split(' ')[0]].append(problemList[4+i].split(' ')[1])

		# for every key, sort the values based on alphabetical order
		for key in graph:
			graph[key] = sorted(graph[key])

		startTime = int(problemList[4+numConnections+1])

		#print graph

		if problemList[0] == 'BFS':
			#print 'Entered BFS'
			
			try:
				answer, time = BFS(graph, source, destination, startTime)
			except:
				outputFile.write('None\n')
				print 'None'
				return

			if answer == False:
				outputFile.write('None\n')
				print 'None\n'

			elif answer is None:
				outputFile.write('None\n')
				print 'None\n'

			else:
				outputFile.write(str(answer) + " " + str(time) + "\n")
				print answer, time

			return
			
		elif problemList[0] == 'DFS':
			#print "Entered DFS"
			

			try:
				answer = DFS(graph, source, destination, startTime)
			except:
				outputFile.write('None\n')
				print 'None\n'
				return

			if answer == 'None':
				outputFile.write('None\n')
				print 'None'

			elif answer is None:
				outputFile.write('None\n')
				print 'None'

			else:
				outputFile.write(str(answer[0]) + " "  + str(answer[1]) + "\n")
				print answer[0], answer[1]
			return

		else:
			#extra processing for UCS
			#print "Entered UCS"
			pipelength = []
			offTimeList = []
			for i in range(1, numConnections+1):
				pipelengthList = [problemList[4+i].split(' ')[0], problemList[4+i].split(' ')[1], int(problemList[4+i].split(' ')[2])]
				pipelength.append(pipelengthList)
				numOffTime = int(problemList[4+i].split(' ')[3])
				offTime = [problemList[4+i].split(' ')[0], problemList[4+i].split(' ')[1], numOffTime]
				if numOffTime > 0:
					#offTimes = []
					for j in range(0, numOffTime):
						offTime.append(problemList[4+i].split(' ')[4+j])
						#print numOffTime, offTimes
					offTimeList.append(offTime)
			#print pipelength
			#print offTimeList
			try:
				answer = UCS(graph, source, destination, startTime, pipelength, offTimeList)
			except:
				outputFile.write('None\n')
				print 'None\n'
				return

			if answer == 'None':
				outputFile.write("None\n")
				print 'None'
			
			elif answer is None:
				outputFile.write("None\n")
				print 'None'

			else:
				print answer
				outputFile.write(str(answer[0]) + " " + str(answer[1]%24) + "\n")
				print answer[0], answer[1]%24
			return

def takeInput():
	#getting file and opening it
	inputFilename = sys.argv[-1]
	inputFile = open(inputFilename, 'r')
	outputFilename = 'output.txt'
	outputFile = open(outputFilename, 'w')
	inputList = [line.rstrip() for line in inputFile.readlines()]
	#getting input in deconstructed form
	numtests = int(inputList.pop(0))	#number of tests
	problemList = []
	newlineCount = 0
	for field in inputList:
		if field == '':
			structureData(problemList, outputFile)
			newlineCount += 1
			problemList = []
		else:
			problemList.append(field)
	if newlineCount != numtests:
		structureData(problemList, outputFile)

def main():
	takeInput()

if __name__ == "__main__":
	main()

	