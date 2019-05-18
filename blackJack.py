###########################################
# Black Jack
# Author: RParkerE
# Date: 10/24/2014
###########################################

import random
import os
import sys
import pygame
from pygame.locals import *

#initializes pygame's fon't module
pygame.font.init()
#initializes pygame's mixer module, used for sound playback
pygame.mixer.init()

#sets the screen dimensions
screen = pygame.display.set_mode((800, 480))
#makes a clock
clock = pygame.time.Clock()

def loadImage(name, card):
	#makes the file destination of the images universal
	#anything before the file is replaced with the correct 
	#absolute path
	if card == 1:
		fullname = os.path.join("images/cards/", name)
	else: fullname = os.path.join('images', name)
	
	#tries to load the image
	try:
		image = pygame.image.load(fullname)
	#unless it receives an error message
	except pygame.error, message:
		print('Cannot load image:', name)
		raise SystemExit, message
	#changes the pixel format of the image
	image = image.convert()
	
	return image, image.get_rect()
		
def loadSound(name):
	#makes the file destination of the images universal
	#anything before the file is replaced with the correct 
	#absolute path
	fullName = os.path.join('sounds', name)
	#tries to load the sound
	try: 
		sound = pygame.mixer.Sound(fullName)
	#unless it receives an error message
	except pygame.error, message:
		print('Cannot load sound:', name)
		raise SystemExit, message
	return sound

def display(font, sentence):
	#displays what is going on to the user
	#is displayed at the bottom of the screen
	displayFont = pygame.font.Font.render(font, sentence, 1, (255,255,255), (167,103,69)) 
	return displayFont

def clickToPlay():
	#defines the function that will be called when
	#a button is clicked, resulting in a sound being
	#played back using the mixer module
	clickSound = loadSound("beep38.wav")
	clickSound.play()


def mainGame():
	
	def gameOver():
		#displays the 'Game Over' screen when 'player' runs out of funds
		while 1:
			#checks to see if there is an event
			for event in pygame.event.get():
				#if it is a quit event then exit
				if event.type == QUIT:
					sys.exit()
				#also if the escape key is pressed, exit
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					sys.exit()

			#make the screen black
			screen.fill((0,0,0))
			
			#display the 'Game Over' screen and text
			oFont = pygame.font.Font(None, 50)
			displayFont = pygame.font.Font.render(oFont, "Game over! You're outta cash!", 1, (255,255,255), (0,0,0)) 
			screen.blit(displayFont, (125, 220))
			
			#updates the display
			pygame.display.flip()
			
	def shuffle(deck):
		#Fisher-Yates shuffle
		n = len(deck) - 1
		while n > 0:
			k = random.randint(0, n)
			deck[k], deck[n] = deck[n], deck[k]
			n -= 1

		return deck        
						
	def makeDeck():
		#creates a default deck with all 52 cards
		deck = ['sj', 'sq', 'sk', 'sa', 'hj', 'hq', 'hk', 'ha', 'cj', 'cq', 'ck', 'ca', 'dj', 'dq', 'dk', 'da']
		#all card values are within 2 and 11 'points', 
		#except for the ace under certain circumstances
		#which will be accounted for later on
		values = range(2,11)
		for x in values:
			#creates a card for each value, 
			#4 for the value of 10 
			#since face cards are worth 10 'points
			spades = "s" + str(x)
			hearts = "h" + str(x)
			clubs = "c" + str(x)
			diamonds = "d" + str(x)
			deck.append(spades)
			deck.append(hearts)
			deck.append(clubs)
			deck.append(diamonds)
		return deck

	def returnToDeck(deck, discard):
		#loops over the discard pile
		for card in discard:
			#and adds the cards to the deck
			deck.append(card)
		#then clears the discard pile
		del discard[:]
		#tells the deck to be shuffled again
		deck = shuffle(deck)

		return deck, discard
		
	def deal(deck, discard):
		#tells the deck to be shuffled
		deck = shuffle(deck)
		#sets both the player and dealer hands to empty lists
		dealerHand = []
		playerHand = []
		
		#counter telling it to only deal 4 cards
		cardsToDeal = 4

		#while there are cards left to deal
		while cardsToDeal > 0:
			#and there are no cards left in the deck
			if len(deck) == 0:
				#return the cards in the discard pile to the deck
				deck, discard = returnToDeck(deck, discard)

			#deal the first card to the player and third card to the played
			if cardsToDeal % 2 == 0: playerHand.append(deck[0])
			#deal the second and last card to the dealer
			else: dealerHand.append(deck[0])
			
			#remove the card just dealt from the deck
			del deck[0]
			#remove one from the counter each time a card is dealt
			cardsToDeal -= 1
			
		return deck, discard, playerHand, dealerHand

	def hit(deck, discard, hand):
		#if the deck is emptyadd the discard pile to the deck
		if len(deck) == 0:
			deck, discard = returnToDeck(deck, discard)
		#add a card to the hand of the person who hit
		hand.append(deck[0])
		#delete the card just dealt from the deck
		del deck[0]

		return deck, discard, hand

	def checkValue(hand):
		#set a counter
		totVal = 0

		#loop over every card in the hand
		for card in hand:
			#add the value of any card that are not the first 2
			value = card[1:]

			#jacks, kings and queens are worth 10 
			if value == 'j' or value == 'q' or value == 'k': 
				value = 10
			#and ace is worth 11   
			elif value == 'a': 
				value = 11
			#and all other cards are face value
			else: 
				value = int(value)

			totVal += value
			

		if totVal > 21:
			for card in hand:
				#if the player busts and has an ace in his hand
				if card[1] == 'a': 
					#the ace is now worth one, this accommodates for the
					#circumstances described in the above comment
					totVal -= 10
				if totVal <= 21:
					break
				else:
					continue

		return totVal
		
	def blackJack(deck, discard, playerHand, dealerHand, funds, bet, cards, cardSprite):
		#this function is automatically called when either person gets blackjack
		textFont = pygame.font.Font(None, 28)

		pVal = checkValue(playerHand)
		dVal = checkValue(dealerHand)
		
		#if both dealer and player get blackjack
		if pVal == 21 and dVal == 21:
			#no money is lost and a new hand will be dealt
			displayFont = display(textFont, "Blackjack! The dealer also has blackjack, so it's a push!")
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, 0, bet, cards, cardSprite)
		  
		#elif only the player gets blackjack
		elif pVal == 21 and dVal != 21:
			#the dealer loses and the player wins his bet 3:2
			displayFont = display(textFont, "Blackjack! You won $%.2f." %(bet*1.5))
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, bet, 0, cards, cardSprite)
	 
		#elif only the dealer gets blackjack
		elif dVal == 21 and pVal != 21:
			#the player loses his bet
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, 0, bet, cards, cardSprite)
			displayFont = display(textFont, "Dealer has blackjack! You lose $%.2f." %(bet))
			
		return displayFont, playerHand, dealerHand, discard, funds, roundEnd

	def bust(deck, playerHand, dealerHand, discard, funds, moneyGained, moneyLost, cards, cardSprite):
		font = pygame.font.Font(None, 28)
		displayFont = display(font, "You bust! You lost $%.2f." %(moneyLost))
		
		deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, moneyGained, moneyLost, cards, cardSprite)
		
		return deck, playerHand, dealerHand, discard, funds, roundEnd, displayFont

	def endRound(deck, playerHand, dealerHand, discard, funds, moneyGained, moneyLost, cards, cardSprite):
		#if the player has an ace in his hand and has hit once
		if len(playerHand) == 2 and "a" in playerHand[0] or "a" in playerHand[1]:
			#pay the bet back 3:2
			moneyGained += (moneyGained/2.0)
			
		#remove old cards
		cards.empty()
		
		#the position of the dealer's first card
		dCardPos = (50, 70)
				   
		#the position for any of the dealer's cards following the first one 
		for x in dealerHand:
			card = cardSprite(x, dCardPos)
			dCardPos = (dCardPos[0] + 80, dCardPos [1])
			cards.add(card)

		#remove the cards from the player's hand
		for card in playerHand:
			discard.append(card)
		#remove the cards from the dealer's hand
		for card in dealerHand:
			discard.append(card)
		
		#make sure that both the player's and dealer's hands are empty
		del playerHand[:]
		del dealerHand[:]

		#calculates the funds remaining
		funds += moneyGained
		funds -= moneyLost
		
		textFont = pygame.font.Font(None, 28)
		
		#if there are no funds remaining end the game
		if funds <= 0:
			gameOver()  
		#roundEnd is now true
		roundEnd = 1

		return deck, playerHand, dealerHand, discard, funds, roundEnd 
		
	def compareHands(deck, discard, playerHand, dealerHand, funds, bet, cards, cardSprite):
		#called at the end of each round, or when a player busts or gets blackjack
		textFont = pygame.font.Font(None, 28)
		#how much money the player loses or gains is defaulted to 0
		#changes depending on outcome
		moneyGained = 0
		moneyLost = 0

		dVal = checkValue(dealerHand)
		pVal = checkValue(playerHand)
			
		#dealer hits until he has 17 or over        
		while 1:
			if dVal < 17:
				#dealer hits when he has less than 17
				deck, discard, dealerHand = hit(deck, discard, dealerHand)
				dVal = checkValue(dealerHand)
			#else he stands
			else:   
				break
					
		#if the player has beaten the dealer, and hasn't busted    
		if pVal > dVal and pVal <= 21:
			#money gained is equal to the bet
			moneyGained = bet
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, bet, 0, cards, cardSprite)
			displayFont = display(textFont, "You won $%.2f." %(bet))
		#elif the player and dealer tie
		elif pVal == dVal and pVal <= 21:
			#no money is lost or gained
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, 0, 0, cards, cardSprite)
			displayFont = display(textFont, "It's a push!")
		#elif the dealer busts and the player doesn't
		elif dVal > 21 and pVal <= 21:
			#money is equal to the bet
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, bet, 0, cards, cardSprite)
			displayFont = display(textFont, "Dealer busts! You won $%.2f." %(bet))
		else:
			#else the dealer wins
			deck, playerHand, dealerHand, discard, funds, roundEnd = endRound(deck, playerHand, dealerHand, discard, funds, 0, bet, cards, cardSprite)
			displayFont = display(textFont, "Dealer wins! You lost $%.2f." %(bet))
			
		return deck, discard, roundEnd, funds, displayFont

	class cardSprite(pygame.sprite.Sprite):
		#initialize the card Sprite
		def __init__(self, card, position):
			pygame.sprite.Sprite.__init__(self)
			cardImage = card + ".png"
			self.image, self.rect = loadImage(cardImage, 1)
			self.position = position
		def update(self):
			self.rect.center = self.position
			
	class hitButton(pygame.sprite.Sprite):
		#initialize the hit button Sprite 
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.image, self.rect = loadImage("hit-grey.png", 0)
			self.position = (735, 400)
			
		def update(self, mX, mY, deck, discard, playerHand, cards, pCardPos, roundEnd, cardSprite, click):
			#if the round is not over use the blue hit button
			if roundEnd == 0: 
				self.image, self.rect = loadImage("hit.png", 0)
			#otherwise use the grey one
			else: 
				self.image, self.rect = loadImage("hit-grey.png", 0)
			
			#set the position of the image/Sprite
			self.position = (735, 400)
			self.rect.center = self.position

			#if the button is clicked
			if self.rect.collidepoint(mX, mY) == 1 and click == 1:
				#and the round is not over
				if roundEnd == 0:
			#play the beep38.wav sound
						clickToPlay()
			#and run the hit function
						deck, discard, playerHand = hit(deck, discard, playerHand)

			#sets the postion of the new card
						currentCard = len(playerHand) - 1
						card = cardSprite(playerHand[currentCard], pCardPos)
						cards.add(card)
						pCardPos = (pCardPos[0] - 80, pCardPos[1])
				
						click = 0
				
			return deck, discard, playerHand, pCardPos, click
			
	class standButton(pygame.sprite.Sprite):
		#initializes the stand button and sets its position    
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.image, self.rect = loadImage("stand-grey.png", 0)
			self.position = (735, 365)
			
		def update(self, mX, mY, deck, discard, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont):
			#if the round is not over use the blue button
			if roundEnd == 0: 
				self.image, self.rect = loadImage("stand.png", 0)
			 #otherwise use the grey button
			else:
				self.image, self.rect = loadImage("stand-grey.png", 0)
			
			#sets the position of the button
			self.position = (735, 365)
			self.rect.center = self.position
			
			#if the button is clicked
			if self.rect.collidepoint(mX, mY) == 1:
				#and the round is not over
				if roundEnd == 0: 
					#play the beep38.wav sound and call the compareHands function to end the round
					clickToPlay()
					deck, discard, roundEnd, funds, displayFont = compareHands(deck, discard, playerHand, dealerHand, funds, bet, cards, cardSprite)
				
			return deck, discard, roundEnd, funds, playerHand, discard, pCardPos, displayFont 
			
	class doubleButton(pygame.sprite.Sprite):
		#initializes the double button and sets its position
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.image, self.rect = loadImage("double-grey.png", 0)
			self.position = (735, 330)
			
		def update(self, mX, mY,   deck, discard, playerHand, dealerHand, playerCards, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont):
			#if the round is not over and your funds are greater than the bet you are
			#trying to place, use the blue button
			if roundEnd == 0 and funds >= bet * 2 and len(playerHand) == 2: 
				self.image, self.rect = loadImage("double.png", 0)
			#otherwise use the grey one
			else: 
				self.image, self.rect = loadImage("double-grey.png", 0)
			
			#sets the position of the button
			self.position = (735, 330)
			self.rect.center = self.position
			   
			#if the button is clicked   
			if self.rect.collidepoint(mX, mY) == 1:
				#and if the round is not over and your funds are greater than the bet you are
				#trying to place, use the blue button
				if roundEnd == 0 and funds >= bet * 2 and len(playerHand) == 2:
					#set the bet to twice as much
					bet = bet * 2
					
					#play the beep38.wav sound
					clickToPlay()
					#call the hit function
					deck, discard, playerHand = hit(deck, discard, playerHand)

					#sets the position of the new cards
					currentCard = len(playerHand) - 1
					card = cardSprite(playerHand[currentCard], pCardPos)
					playerCards.add(card)
					pCardPos = (pCardPos[0] - 80, pCardPos[1])
		
					#calls the compareHands function
					deck, discard, roundEnd, funds, displayFont = compareHands(deck, discard, playerHand, dealerHand, funds, bet, cards, cardSprite)
					
					#set the bet back to the original
					bet = bet / 2

			return deck, discard, roundEnd, funds, playerHand, discard, pCardPos, displayFont, bet

	class dealButton(pygame.sprite.Sprite):
		#initializes the deal button and sets its position      
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.image, self.rect = loadImage("deal.png", 0)
			self.position = (735, 450)

		def update(self, mX, mY, deck, discard, roundEnd, cardSprite, cards, playerHand, dealerHand, dCardPos, pCardPos, displayFont, playerCards, click, handsPlayed):
			textFont = pygame.font.Font(None, 28)
			
			#if the round is over use the blue button
			if roundEnd == 1: 
				self.image, self.rect = loadImage("deal.png", 0)
			#otherwise use the grey one 
			else:
				self.image, self.rect = loadImage("deal-grey.png", 0)
			
			#set the position of the button
			self.position = (735, 450)
			self.rect.center = self.position
			
			#if the button is clicked    
			if self.rect.collidepoint(mX, mY) == 1:
				#and the round is over
				if roundEnd == 1 and click == 1:
					#play the beep38.wav sound
					clickToPlay()
					displayFont = display(textFont, "")
					
					#empty the player's and dealer's cards
					cards.empty()
					playerCards.empty()
					
					#call the deal function
					deck, discard, playerHand, dealerHand = deal(deck, discard)

					#set the position of the first card for both the dealer and player
					dCardPos = (50, 70)
					pCardPos = (540,370)
					#position of all the following player's cards
					for x in playerHand:
						card = cardSprite(x, pCardPos)
						pCardPos = (pCardPos[0] - 80, pCardPos [1])
						playerCards.add(card)
					
					#position of all the following dealer's cards  
					faceDownCard = cardSprite("back", dCardPos)
					dCardPos = (dCardPos[0] + 80, dCardPos[1])
					cards.add(faceDownCard)

					card = cardSprite(dealerHand [0], dCardPos)
					cards.add(card)
					roundEnd = 0
					click = 0
					handsPlayed += 1
					
			return deck, discard, playerHand, dealerHand, dCardPos, pCardPos, roundEnd, displayFont, click, handsPlayed
			
			
	class betButtonUp(pygame.sprite.Sprite):
		#initializes the up bet button and sets its position
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.image, self.rect = loadImage("up.png", 0)
			self.position = (710, 255)
			
		def update(self, mX, mY, bet, funds, click, roundEnd):
			#if the round is not over use the blue button
			if roundEnd == 1: 
				self.image, self.rect = loadImage("up.png", 0)
			#otherwise use the grey one
			else: 
				self.image, self.rect = loadImage("up-grey.png", 0)
			
			#set the button's position
			self.position = (710, 255)
			self.rect.center = self.position
			
			#if the button is clicked
			if self.rect.collidepoint(mX, mY) == 1 and click == 1 and roundEnd == 1:
				#play the beep38.wav
					clickToPlay()
				
				#if you have more money than you are trying to bet              
					if bet < funds:
					#add 5 dollars to the bet
						bet += 5.0
					#if the bet is not a multiple of 5, turn it into a multiple of 5
					if bet % 5 != 0:
						while bet % 5 != 0:
							bet -= 1

					click = 0
			
			return bet, click
			
	class betButtonDown(pygame.sprite.Sprite):
		#initializes the up bet button and sets its position
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			self.image, self.rect = loadImage("down.png", 0)
			self.position = (710, 255)
			
		def update(self, mX, mY, bet, click, roundEnd): 
			#if the round is not over use the blue button
			if roundEnd == 1: 
				self.image, self.rect = loadImage("down.png", 0)
			#otherwise use the grey one
			else: 
				self.image, self.rect = loadImage("down-grey.png", 0)
		
			#set the button's position
			self.position = (760, 255)
			self.rect.center = self.position
 
			#if the round is over and the button is clicked
			if self.rect.collidepoint(mX, mY) == 1 and click == 1 and roundEnd == 1:
				#play the beep38.wav sound
				clickToPlay()
				#if the bet is more than 5 dollars
				if bet > 5:
					#decrease the bet by 5 dollars
					bet -= 5.0
					#if the bet is not a multiple of 5, make it one
					if bet % 5 != 0:
						while bet % 5 != 0:
							bet += 1
					
				click = 0
			
			return bet, click

	#this font is used to display text on the right-hand side of the screen
	textFont = pygame.font.Font(None, 28)

	#this sets up the background image
	background, backgroundRect = loadImage("bjs.png", 0)
	
	#cards is the sprite group that will contain sprites for the dealer's cards
	cards = pygame.sprite.Group()
	#playerCards is the sprite group that will contain sprites for the dealer's cards
	playerCards = pygame.sprite.Group()

	#this creates instances of all the button sprites
	bbU = betButtonUp()
	bbD = betButtonDown()
	standButton = standButton()
	dealButton = dealButton()
	hitButton = hitButton()
	doubleButton = doubleButton()
	
	#this group contains the button sprites
	buttons = pygame.sprite.Group(bbU, bbD, hitButton, standButton, dealButton, doubleButton)

	#creates the 52 card deck
	deck = makeDeck()
	#create a discard pile for the used cards
	discard = []

	#these are default values that will be changed later
	playerHand = []
	dealerHand = []
	dCardPos = ()
	pCardPos = ()
	mX, mY = 0, 0
	click = 0

	#the default for funds and bet
	funds = 100.00
	bet = 10.00

	#a counter that counts the number of rounds played
	handsPlayed = 0

	# When the cards have been dealt, roundEnd is zero.
	#In between rounds, it is equal to one
	roundEnd = 1
	
	#firstTime is a variable that is only used once to display the initial message at the bottom
	firstTime = 1

	while 1:
		screen.blit(background, backgroundRect)
		
		if bet > funds:
			#ff you lost money, and your bet is greater than your funds, make the bet equal to the funds
			bet = funds
		
		if roundEnd == 1 and firstTime == 1:
			#when the player hasn't started. Will only be displayed the first time.
			displayFont = display(textFont, "Click on the arrows to declare your bet, then deal to start the game.")
			firstTime = 0
			
		#show the blurb at the bottom of the screen, how much money left, and current bet    
		screen.blit(displayFont, (10,444))
		fundsFont = pygame.font.Font.render(textFont, "Funds: $%.2f" %(funds), 1, (255,255,255), (167,103,69))
		screen.blit(fundsFont, (663,205))
		betFont = pygame.font.Font.render(textFont, "Bet: $%.2f" %(bet), 1, (255,255,255), (167,103,69))
		screen.blit(betFont, (680,285))
		hpFont = pygame.font.Font.render(textFont, "Round: %i " %(handsPlayed), 1, (255,255,255), (167,103,69))
		screen.blit(hpFont, (663, 180))

		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					mX, mY = pygame.mouse.get_pos()
					click = 1
			elif event.type == MOUSEBUTTONUP:
				mX, mY = 0, 0
				click = 0
			
		# Initial check for the value of the player's hand, so that his hand can be displayed and it can be determined
		# if the player busts or has blackjack or not
		if roundEnd == 0:
			# Stuff to do when the game is happening 
			pVal = checkValue(playerHand)
			dVal = checkValue(dealerHand)
	
			if pVal == 21 and len(playerHand) == 2:
				# If the player gets blackjack
				displayFont, playerHand, dealerHand, discard, funds, roundEnd = blackJack(deck, discard, playerHand, dealerHand, funds,  bet, cards, cardSprite)
				
			if dVal == 21 and len(dealerHand) == 2:
				# If the dealer has blackjack
				displayFont, playerHand, dealerHand, discard, funds, roundEnd = blackJack(deck, discard, playerHand, dealerHand, funds,  bet, cards, cardSprite)

			if pVal > 21:
				# If player busts
				deck, playerHand, dealerHand, discard, funds, roundEnd, displayFont = bust(deck, playerHand, dealerHand, discard, funds, 0, bet, cards, cardSprite)
		 
		# Update the buttons 
		# deal 
		deck, discard, playerHand, dealerHand, dCardPos, pCardPos, roundEnd, displayFont, click, handsPlayed = dealButton.update(mX, mY, deck, discard, roundEnd, cardSprite, cards, playerHand, dealerHand, dCardPos, pCardPos, displayFont, playerCards, click, handsPlayed)   
		# hit    
		deck, discard, playerHand, pCardPos, click = hitButton.update(mX, mY, deck, discard, playerHand, playerCards, pCardPos, roundEnd, cardSprite, click)
		# stand    
		deck, discard, roundEnd, funds, playerHand, discard, pCardPos,  displayFont  = standButton.update(mX, mY,   deck, discard, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont)
		# double
		deck, discard, roundEnd, funds, playerHand, discard, pCardPos, displayFont, bet  = doubleButton.update(mX, mY,   deck, discard, playerHand, dealerHand, playerCards, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont)
		# Bet buttons
		bet, click = bbU.update(mX, mY, bet, funds, click, roundEnd)
		bet, click = bbD.update(mX, mY, bet, click, roundEnd)
		# draw them to the screen
		buttons.draw(screen)
		 
		# If there are cards on the screen, draw them    
		if len(cards) is not 0:
			playerCards.update()
			playerCards.draw(screen)
			cards.update()
			cards.draw(screen)

		# Updates the contents of the display
		pygame.display.flip()


if __name__ == "__main__":
	mainGame()
