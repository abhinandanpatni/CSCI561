import sys
from copy import deepcopy


"""DEFINING GLOBAL VARS"""
INFINITY = 100000

log = ""

"""==========CONVERT VALUES TO STRING================="""
def toStr(value):
	if value == INFINITY:
		return 'Infinity'
	elif value == -INFINITY:
		return '-Infinity'
	else:
		return str(value)	

"""======================PRINTING NEXT STATE================"""
def printNextState(outputFile, answer):
	answer = answer[1:]
	outputString = ""
	outputString += ' '.join(map(str, answer[0][1])) + "\n"
	outputString += ' '.join(map(str, answer[0][0])) + "\n"
	outputString += str(answer[1][1]) + "\n"
	outputString += str(answer[1][0]) + "\n"
	outputFile.write(outputString)


"""====================GET ALPHA BETA TRAVERSE LOG============"""
def alphaBetaTraverseLog(player, index, depth, value, alpha, beta):
	global log
	node = ""
	if player == 0:
		node = 'B'+str(index+2)
	else:
		node = 'A'+str(index+2)

	print node, depth, toStr(value), toStr(alpha), toStr(beta)
	log += node + "," + str(depth) + "," + toStr(value) + "," + toStr(alpha) + "," + toStr(beta) + "\n"

"""==============GET MINIMAX TRAVERSE LOG============================="""
def traverseLog(player, index, depth, val):
	global log
	node = ""
	value = ""
	if player == 0:
		node = 'B'+str(index+2)
	else:
		node = 'A'+str(index+2)

	print node, depth, value
	log += node + "," + str(depth) + "," + toStr(value) + "\n"


"""================================CUTOFF STATE TESTING===================="""
def cutoffTest(cutoff, localDepth):
	return cutoff <= localDepth

"""================================TERMINAL STATE TESTING===================="""
def terminalTest(state, player):
	return all(numStones == 0 for numStones in state[player])

#TODO: End terminal case where all stones go to a particular mancala
"""======================================PERFORM MOVES================================"""
def performAction(player, state, boardStates, mancalas):
	numStones = boardStates[player][state]
	boardStates[player][state] = 0
	limit = len(boardStates[player]) - 1
	endState = 0
	lastInCaptureArea = False
	lastInMancala = False
	while numStones > 0:
		if player == 0:
			#Transfer stones on own side of the board
			while numStones > 0 and state < limit:
				state += 1
				boardStates[player][state] += 1
				numStones -= 1
				endState = state
				lastInCaptureArea = True
			#Transfer stone to own mancala
			if numStones > 0:
				lastInCaptureArea = False
				lastInMancala = True
				mancalas[0] += 1
				numStones -= 1
			#Transfer stone to opponents side of the board
			if numStones > 0:
				lastInCaptureArea = False
				lastInMancala = False
				player = 1
				opponentState = 0
				while numStones > 0 and opponentState <= limit:
					boardStates[player][limit - opponentState] += 1
					opponentState += 1
					numStones -= 1
			#skip over opponent's mancala; you're on your own side. Begin again with the standard procedure.
			if numStones > 0:
				player = 0
				state = -1
		else:
			while numStones > 0 and state > 0:
				state -= 1
				boardStates[player][state] += 1
				numStones -= 1
				endState = state
				lastInCaptureArea = True

			if numStones > 0:
				lastInCaptureArea = False
				lastInMancala = True
				mancalas[1] += 1
				numStones -= 1

			if numStones > 0:
				lastInMancala = False
				lastInCaptureArea = False
				player = 0
				opponentState = 0
				while numStones > 0 and opponentState <= limit:
					boardStates[player][opponentState] += 1
					opponentState += 1
					numStones -= 1

			if numStones > 0:
				player = 1
				state = limit+1

	if lastInCaptureArea is True and boardStates[player][endState] == 1:
		print "Entering here for ", boardStates
		if player == 0:
			mancalas[0] += boardStates[player][endState] + boardStates[1][endState]
			#print mancalas
			boardStates[player][endState] = 0
			boardStates[1][endState] = 0
		else:
			mancalas[1] += boardStates[player][endState] + boardStates[0][endState]
			boardStates[player][endState] = 0
			boardStates[0][endState] = 0

	if all(pits == 0 for pits in boardStates[player][:]):
		print "Terminal State reached"
		for x in range(limit+1):
			mancalas[abs(player-1)] += boardStates[abs(player-1)][x]
			boardStates[abs(player-1)][x] = 0
	elif all(pits == 0 for pits in boardStates[abs(player-1)][:]):
		print "Another Terminal State reached"
		for x in range(limit+1):
			mancalas[player] += boardStates[player][x]
			boardStates[player][x] = 0

	#print mancalas, boardStates
	return [boardStates, mancalas, lastInMancala]

""" =====================GET ALL LEGAL STATES FOR TRANSITIONS==============================="""
def getLegalStates(player, boardStates):
	#print boardStates, player
	legalState = list()
	for i in range(len(boardStates[player])):
		if boardStates[player][i] > 0:
			legalState.append(i)
	return legalState

"""=====================FREE STATE TRANSITIONS HANDLER FOR MINIMAX======================================"""
def performFreeTurnMinimax(boardState, mancalas, player, state, localDepth, strategy, cutoff, originalPlayer, originalState):
	v_node = 0
	if strategy is "MIN":
		v_node = INFINITY
	else:
		v_node = -INFINITY

	traverseLog(player, state, localDepth, v_node)

	legalStates = getLegalStates(player, boardState)
	for freeTurnState in legalStates:
		temp_boardState = deepcopy(boardState)
		temp_mancalas = deepcopy(mancalas)
		newBoardState, newLocalManacala, freeTurn = performAction(player, freeTurnState, temp_boardState, temp_mancalas)
		print newBoardState, newLocalManacala, freeTurn
		if freeTurn is True:
			retVal = performFreeTurnMinimax(newBoardState, newLocalManacala, player, freeTurnState, localDepth, strategy, cutoff, originalPlayer, freeTurnState)
			if strategy is "MIN":
				if retVal[0] < v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]
			else:
				if retVal[0] > v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]
		else:
			if strategy is "MIN":
				retVal = minimaxValue(newBoardState, newLocalManacala,abs(player-1),cutoff, localDepth, "MAX", originalPlayer, freeTurnState)
				if retVal[0] < v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]
			else:
				retVal = minimaxValue(newBoardState, newLocalManacala,abs(player-1),cutoff, localDepth, "MIN", originalPlayer, freeTurnState)
				if retVal[0] > v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]

		traverseLog(player, state, localDepth, v_node)

	return value


"""==============================MINIMAX ALGORITHM MAIN========================="""
def minimaxValue(boardStates, mancalas, player, cutoff, localDepth, strategy, originalPlayer, originalState):
	
	print "Local Depth:" ,localDepth

	if cutoffTest(cutoff, localDepth) or terminalTest(boardStates, player):
		#print "FinalStates: ", boardStates, mancalas
		if originalPlayer == 0:
			print "Manacala difference : ", mancalas[0] - mancalas[1]
			v_node =  mancalas[0] - mancalas[1]
			traverseLog(abs(player-1), originalState, localDepth, v_node)
			return [mancalas[0] - mancalas[1], boardStates, mancalas]
		else:
			print "Manacala difference : ", mancalas[0] - mancalas[1]
			v_node = mancalas[1] - mancalas[0]
			traverseLog(abs(player-1), originalState, localDepth, v_node)
			return [mancalas[1] - mancalas[0], boardStates, mancalas]

	v_node = 0
	if strategy is "MIN":
		v_node = INFINITY
	else:
		v_node = -INFINITY

	traverseLog(abs(player-1), originalState, localDepth, v_node)

	print "Player to play: ", player
	legalStates = getLegalStates(player, boardStates)
	print "Legal States:", legalStates
	for state in legalStates:
		temp_boardStates = deepcopy(boardStates)
		temp_mancalas = deepcopy(mancalas)
		newBoardState, newLocalManacala, freeTurn = performAction(player, state, temp_boardStates, temp_mancalas)
		print newBoardState[1], newBoardState[0], newLocalManacala, freeTurn
		if freeTurn is True:
			#call Free turn function
			retVal = performFreeTurnMinimax(newBoardState, newLocalManacala, player, state, localDepth+1, strategy, cutoff, originalPlayer, state)
			if strategy is "MIN":
				if retVal[0] < v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]
			else:
				if retVal[0] > v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]

			traverseLog(abs(player-1), originalState, localDepth, v_node)

		else:
			if strategy is "MIN": #next, I will play
				retVal = (minimaxValue(newBoardState, newLocalManacala, abs(player-1), cutoff, localDepth+1, "MAX", originalPlayer, state))
				if retVal[0] < v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]
				
			else: #next, opponent will play
				retVal = (minimaxValue(newBoardState, newLocalManacala, abs(player-1), cutoff, localDepth+1, "MIN", originalPlayer, state))
				if retVal[0] > v_node:
					v_node = retVal[0]
					value = [retVal[0], newBoardState, newLocalManacala]
				
			traverseLog(abs(player-1), originalState, localDepth, v_node)

	return value

""" ==========================DEFINING MINIMAX STARTING POINT================================== """
def minimaxDecision(task, player, cutoff, boardStates, mancalas, originalPlayer):
	global INFINITY
	global log
	v_root = -INFINITY
	log += "Node,Depth,Value\n"
	log += "root,0,-Infinity\n"
	legalStates = getLegalStates(player, boardStates)
	localDepth = 0 #root
	value = list()
	for state in legalStates:
		temp_boardStates = deepcopy(boardStates)
		temp_mancalas = deepcopy(mancalas)
		#print boardStates, mancalas
		#perform action for the player
		newBoardState, newLocalManacala, freeTurn = performAction(player, state, temp_boardStates, temp_mancalas)
		print newBoardState[1], newBoardState[0], newLocalManacala, freeTurn
		if freeTurn is True:
			retVal = performFreeTurnMinimax(newBoardState, newLocalManacala, player, state, localDepth+1, "MAX", cutoff, originalPlayer, state)
			if retVal[0] > v_root:
				v_root = retVal[0]
				value = retVal
		#now call the opponent to play out their respective possibilities. abs(player-1) will always give the other player because player = {0,1}, Min to play
		else:
			retVal = (minimaxValue(newBoardState, newLocalManacala, abs(player-1), cutoff, localDepth+1, "MIN", originalPlayer, state))
			if retVal[0] > v_root:
				v_root = retVal[0]
				value = [retVal[0], newBoardState, newLocalManacala]

		log += "root,0," + str(v_root) + "\n"

	print value
	return value

"""=================================FREE STATE HANDLER FOR ALPHA BETA PRUNING=============================="""

def performFreeAlphaBeta(boardState, mancalas, player, state, localDepth, strategy, cutoff, originalPlayer, originalState, alpha, beta):
	global INFINITY
	v_node = 0
	if strategy is "MIN":
		v_node = INFINITY
	else:
		v_node = -INFINITY

	print "======1======="
	alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)

	legalStates = getLegalStates(player, boardState)
	value = list()
	for freeTurnState in legalStates:
		temp_boardState = deepcopy(boardState)
		temp_mancalas = deepcopy(mancalas)
		newBoardState, newLocalManacala, freeTurn = performAction(player, freeTurnState, temp_boardState, temp_mancalas)
		print newBoardState, newLocalManacala, freeTurn
		if freeTurn is True:
			retVal = performFreeAlphaBeta(newBoardState, newLocalManacala, player, freeTurnState, localDepth, strategy, cutoff, originalPlayer, freeTurnState, alpha, beta)
			if strategy is "MIN":
				print "ABP recursion retVal: ", retVal
				print "vnode value from free turn: ", v_node
				if retVal[0] < v_node:
					print "ENTERING V_NODE CHANGE FOR MIN NODE in alpha beta free state"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if beta > v_node:
					beta = v_node
				if alpha >= beta:
					value = [beta, newBoardState, newLocalManacala]
					alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					break
				value = [beta, newBoardState, newLocalManacala]
			else:
				if retVal[0] > v_node:
					print "ENTERING V_NODE CHANGE FOR MAX NODE"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if alpha < v_node:
					alpha = v_node
				if beta <= alpha:
					value = [alpha, newBoardState, newLocalManacala]
					alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					break
				value = [alpha, newBoardState, newLocalManacala]
		else:
			if strategy is "MIN":
				retVal = alphaBetaPrune(newBoardState, newLocalManacala,abs(player-1),cutoff, localDepth, "MAX", originalPlayer, alpha, beta, freeTurnState)
				if retVal[0] < v_node:
					print "ENTERING V_NODE CHANGE FOR MIN NODE in free state 2"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if beta > v_node:
					beta = v_node
				if alpha >= beta:
					value = [beta, newBoardState, newLocalManacala]
					alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					break
				value = [beta, newBoardState, newLocalManacala]
			else:
				retVal = alphaBetaPrune(newBoardState, newLocalManacala,abs(player-1),cutoff, localDepth, "MIN", originalPlayer, alpha, beta, freeTurnState)
				if retVal[0] > v_node:
					print "ENTERING V_NODE CHANGE FOR MAX NODE"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if alpha < v_node:
					alpha = v_node
				if beta <= alpha:
					value = [alpha, newBoardState, newLocalManacala]
					alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					break
				value = [alpha, newBoardState, newLocalManacala]
		print "======2======="
		alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)

	print "RETURNING VALUE FROM ALPHA BETA: ", value
	return value


"""==================================MINIMAX PRUNE ALGORITHM TO WORK WITH ALPHA BETA========================="""
def alphaBetaPrune(boardStates, mancalas, player, cutoff, localDepth, strategy, originalPlayer, alpha, beta, originalState):

	#print "For boardStates: ", boardStates, "Free Turn: ", freeTurn
	print "Local Depth:" ,localDepth
	if cutoffTest(cutoff, localDepth) or terminalTest(boardStates, player):
		#print "FinalStates: ", boardStates, mancalas
		if originalPlayer == 0:
			print "Manacala difference : ", mancalas[0] - mancalas[1]
			v_node = mancalas[0] - mancalas[1]
			print "======3======="
			alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
			return [mancalas[0] - mancalas[1], boardStates, mancalas]
		else:
			print "Manacala difference : ", mancalas[0] - mancalas[1]
			v_node = mancalas[1] - mancalas[0]
			print "======4======="
			alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
			return [mancalas[1] - mancalas[0], boardStates, mancalas]

	v_node = 0
	if strategy is "MIN":
		v_node = INFINITY
	else:
		v_node = -INFINITY
	print v_node
	print "======5======="
	alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)

	print "Player to play: ", player
	#value = list()
	legalStates = getLegalStates(player, boardStates)
	print "Legal States:", legalStates
	for state in legalStates:
		temp_boardStates = deepcopy(boardStates)
		temp_mancalas = deepcopy(mancalas)
		newBoardState, newLocalManacala, freeTurn = performAction(player, state, temp_boardStates, temp_mancalas)
		print newBoardState[1], newBoardState[0], newLocalManacala, freeTurn

		if freeTurn is True:
			#call Free turn function
			retVal = performFreeAlphaBeta(newBoardState, newLocalManacala, player, state, localDepth+1, strategy, cutoff, originalPlayer, state, alpha, beta)
			print "RETURNING RETVAL: ", retVal
			if strategy is "MIN":
				print "ABP recursion retVal: ", retVal
				print "vnode value from free turn: ", v_node
				if retVal[0] < v_node:
					print "ENTERING V_NODE CHANGE FOR MIN  in alpha beta prune"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if beta > v_node:
					beta = v_node
				if alpha >= beta:
					value = [beta, newBoardState, newLocalManacala]
					#alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
					break
				value = [beta, newBoardState, newLocalManacala]
			else:
				if retVal[0] > v_node:
					print "ENTERING V_NODE CHANGE FOR MAX NODE"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if alpha < v_node:
					alpha = v_node
				if beta <= alpha:
					value = [alpha, newBoardState, newLocalManacala]
					#alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
					break
				value = [alpha, newBoardState, newLocalManacala]
			print "======6======="
			alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)

		else:
			if strategy is "MIN": #next, I will play #this was a min move
				retVal = alphaBetaPrune(newBoardState, newLocalManacala, abs(player-1), cutoff, localDepth+1, "MAX", originalPlayer, alpha, beta, state)
				print "ABP recursion retVal: ", retVal
				print "vnode value from free turn: ", v_node
				if retVal[0] < v_node:
					print "ENTERING V_NODE CHANGE FOR MIN NODE in alpha beta prune 2"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if beta > v_node:
					beta = v_node
				if alpha >= beta:
					value = [beta, newBoardState, newLocalManacala]
					#alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
					break
				value = [beta, newBoardState, newLocalManacala]

			else: #next, opponent will play
				retVal = alphaBetaPrune(newBoardState, newLocalManacala, abs(player-1), cutoff, localDepth+1, "MIN", originalPlayer, alpha, beta, state)
				if retVal[0] > v_node:
					print "ENTERING V_NODE CHANGE FOR MAX NODE"
					v_node = retVal[0]
					print "VNODE NOW IS: ", v_node
					print "ALPHA, BETA: ", alpha, beta
				if alpha < v_node:
					alpha = v_node
				if beta <= alpha:
					value = [alpha, newBoardState, newLocalManacala]
					#alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
					alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
					break
				value = [alpha, newBoardState, newLocalManacala]
			print "======7======="
			alphaBetaTraverseLog(abs(player-1), originalState, localDepth, v_node, alpha, beta)
	
	print "vnode val just before returning", value
	return value

"""=======================================DEFINING STARTING POINT FOR ALPHA BETA============================"""
def alphaBeta(task, player, cutoff, boardStates, mancalas, originalPlayer):
	#set value to -INFINITY 
	global INFINITY
	global log
	v_root = -INFINITY
	alpha = -INFINITY
	beta = INFINITY
	log += "Node,Depth,Value,Alpha,Beta\n"
	log += "root,0,-Infinity,-Infinity,Infinity\n"
	print "root,0,-Infinity, -Infinity, Infinity\n"
	value = list()
	localDepth = 0 #root

	legalStates = getLegalStates(player, boardStates)
	for state in legalStates:
		temp_boardStates = deepcopy(boardStates)
		temp_mancalas = deepcopy(mancalas)
		newBoardState, newLocalManacala, freeTurn = performAction(player, state, temp_boardStates, temp_mancalas)
		print newBoardState[1], newBoardState[0], newLocalManacala, freeTurn
		if freeTurn is True:
			print "Free turn was true. Will now get all states from here on."
			retVal = performFreeAlphaBeta(newBoardState, newLocalManacala, player, state, localDepth+1, "MAX", cutoff, originalPlayer, state, alpha, beta)
			if retVal[0] > v_root:
				print "ENTERING V_NODE CHANGE FOR MAX NODE"
				v_root = retVal[0]
				print "VNODE NOW IS: ", v_root
				print "ALPHA, BETA: ", alpha, beta
				value = retVal
				print "UPDATING VALUE: 1 ", value
			if alpha < v_root:
				alpha = v_root
			if beta <= alpha:
				value = [alpha, retVal[1], retVal[2]]
				print "UPDATING VALUE: 2 ", value
				#alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
				break
			# value = retVal
			#print "UPDATING VALUE: 2 ", value
				
				# print "ENTERING V_NODE CHANGE FOR MAX NODE"
				# v_root = retVal[0]
				# print "VNODE NOW IS: ", v_root
				# print "ALPHA, BETA: ", alpha, beta
				# alpha = v_root
				# value = retVal
				# if v_root > beta:
				# 	break
			
		else:
			retVal = alphaBetaPrune(newBoardState, newLocalManacala, abs(player-1), cutoff, localDepth+1, "MIN", originalPlayer, alpha, beta, state)
			if retVal[0] > v_root:
				print "ENTERING V_NODE CHANGE FOR MAX NODE"
				v_root = retVal[0]
				print "VNODE NOW IS: ", v_root
				print "ALPHA, BETA: ", alpha, beta
				#value = [retVal[0], newBoardState, newLocalManacala]
				value = retVal
				print "UPDATING VALUE: 3 ", value
				value = retVal
			if alpha < v_root:
				alpha = v_root
			if beta <= alpha:
				value = [alpha, newBoardState, newLocalManacala]
				print "UPDATING VALUE: 4 ", value
				#alphaBetaTraverseLog(player, state, localDepth, v_node, alpha, beta)
				break
			# value = [retVal[0], newBoardState, newLocalManacala]
			# print "UPDATING VALUE: 4 ", value
			
		print "root,0," + toStr(v_root) + "," + toStr(alpha) + "," + toStr(beta) + "\n"
		log += "root,0," + toStr(v_root) + "," + toStr(alpha) + "," + toStr(beta) + "\n"
	print value
	return value

"""===========================CALL AN ALGORITHM================================================"""
def callTask(task, player, cutoff, boardStates, mancalas):
	global log
	if task is '1':
		print "Calling Greedy"
		finalAnswer = minimaxDecision(task, player, 1, boardStates, mancalas, player)
		with open("next_state.txt", "w") as opfile1:
			printNextState(opfile1, finalAnswer)
		with open("traverse_log.txt", "w") as opfile2:
			opfile.write(log)

	elif task is '2':
		print "Calling MiniMax"
		finalAnswer = minimaxDecision(task, player, cutoff, boardStates, mancalas, player)
		with open("next_state.txt", "w") as opfile1:
			printNextState(opfile1, finalAnswer)
		with open("traverse_log.txt", "w") as opfile:
			opfile.write(log)

	elif task is '3':
		print "Calling Alpha-Beta"
		finalAnswer = alphaBeta(task, player, cutoff, boardStates, mancalas, player)
		print finalAnswer
		with open("next_state.txt", "w") as opfile1:
			printNextState(opfile1, finalAnswer)
		with open("traverse_log.txt", "w") as opfile:
			opfile.write(log)

def processInput():
	with open(sys.argv[-1], 'r') as inputFile:
		inputList = [line.rstrip() for line in inputFile.readlines()]
		task = inputList[0]
		player = int(inputList[1]) - 1 
		cutoff = int(inputList[2])
		
		boardStates = list()
		boardStates.append(map(int, inputList[4].split(' ')))
		boardStates.append(map(int, inputList[3].split(' ')))

		mancalas = list()
		mancalas.append(int(inputList[6]))
		mancalas.append(int(inputList[5]))

		print task
		print player
		print cutoff
		print boardStates
		print mancalas
		callTask(task, player, cutoff, boardStates, mancalas)


def main():
	processInput()

if __name__ == '__main__':
	main()

