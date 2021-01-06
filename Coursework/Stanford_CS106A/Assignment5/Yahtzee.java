/*
 * File: Yahtzee.java
 * ------------------
 * This program will eventually play the Yahtzee game.
 */

import acm.io.*;
import acm.program.*;
import acm.util.*;

public class Yahtzee extends GraphicsProgram implements YahtzeeConstants {
	
	public static void main(String[] args) {
		new Yahtzee().start(args);
	}
	
	public void run() {
		IODialog dialog = getDialog();
		nPlayers = dialog.readInt("Enter number of players");
		playerNames = new String[nPlayers];
		for (int i = 1; i <= nPlayers; i++) {
			playerNames[i - 1] = dialog.readLine("Enter name for player " + i);
		}
		display = new YahtzeeDisplay(getGCanvas(), playerNames);
		dice = new int[N_DICE];
		scoreBoard = new int[nPlayers][N_CATEGORIES];
		playGame();
	}

	private void playGame() {
		for(int i=0; i<N_SCORING_CATEGORIES; i++) { //1 game = 13 rounds
			for(int j=1; j<=nPlayers; j++) {
				aTurn(j);
			}
		}
		gameOver();
	}
	
	/**Simulates one turn, player rolls dices and pick category to store score*/
	private void aTurn(int player) { //player: The index of the player, ranging from 1 to nPlayers
		display.printMessage(playerNames[player-1] + "'s turn. Click \"Roll Dice\" button to roll the dice.");
		display.waitForPlayerToClickRoll(player); //1st roll 
		diceArray();
		display.displayDice(dice); 
		reroll(player); //2nd roll chance
		reroll(player); //3rd roll chance
		int category = display.waitForPlayerToSelectCategory();
		storeScore(category, player);
	}
	
	/**additional chances to improve their roll. Selected dices will be rolled again.*/
	private void reroll(int player) { //player: The index of the player, ranging from 1 to nPlayers
		display.printMessage("Select the dice you wish to re-roll and click \"Roll Again\".");
		display.waitForPlayerToSelectDice(); 
		for(int i=0; i<N_DICE; i++) {
			if (display.isDieSelected(i)) {
				dice[i] = rgen.nextInt(1, 6);
			}
		}
		display.displayDice(dice);
	}
	
	/**Returns Array of random dice values*/
	private int[] diceArray() {		
		for(int i=0; i<N_DICE; i++) {
			int temp = rgen.nextInt(1, 6);
			dice[i] = temp;
		}
		return dice;
	}
	
	/**Store score on selected category and update score card
	 * @param category: specific category of the scoresheet
	 * @param player: index of the player, raging from 1 to nPlayers*/
	private void storeScore(int category, int player) { //player: The index of the player, ranging from 1 to nPlayers
		display.printMessage("Select a category for this roll.");
		int score = 0;
		switch(category) {
		  case ONES:
			score = upperScore_calculation(ONES, score);
			scoreBoard[player-1][category-1] = score;
		    break;
		  case TWOS:
			score = upperScore_calculation(TWOS, score);
			scoreBoard[player-1][category-1] = score;
		    break;
		  case THREES:
			score = upperScore_calculation(THREES, score);
			scoreBoard[player-1][category-1] = score;
			break;
		  case FOURS:
			score = upperScore_calculation(FOURS, score);
			scoreBoard[player-1][category-1] = score;
			break;
		  case FIVES:
			score = upperScore_calculation(FIVES, score);
			scoreBoard[player-1][category-1] = score;
			break;
		  case SIXES:
			score = upperScore_calculation(SIXES, score);
			scoreBoard[player-1][category-1] = score;
			break;
		  case UPPER_SCORE:
			int sum_upper = 0;
			for(int i=0; i<SIXES; i++) {
				sum_upper += scoreBoard[player-1][i];
			}
			score = sum_upper;
			scoreBoard[player-1][category-1] = score;
			break;
		  case UPPER_BONUS:
			if(scoreBoard[player-1][UPPER_SCORE-1] >= 63) {
				score = 35;
			}		
			scoreBoard[player-1][category-1] = score;
			break;
		  case THREE_OF_A_KIND:
			if(isRepetition(3) == true) {
				for(int i=0; i<N_DICE; i++) {
					score += dice[i];
				}
			}
			scoreBoard[player-1][category-1] = score;
			break;
		  case FOUR_OF_A_KIND:
			if(isRepetition(4) == true) {
				for(int i=0; i<N_DICE; i++) {
					score += dice[i];
				}
			}
			scoreBoard[player-1][category-1] = score;
			break;
		  case FULL_HOUSE:
			if(isFullhouse()) {
				score = 25;
			} 
			scoreBoard[player-1][category-1] = score;
			break;
		  case SMALL_STRAIGHT:
			if(straight(4) == true) {
				score = 30;
			}
			scoreBoard[player-1][category-1] = score;
			break;
		  case LARGE_STRAIGHT:
			if(straight(5) == true) {
				score = 40;
			}
			scoreBoard[player-1][category-1] = score;
			break;
		  case YAHTZEE:
			if(isRepetition(5) == true) {
				score = 50;
			} 
			scoreBoard[player-1][category-1] = score;
			break;
		  case CHANCE:
			for(int i=0; i<N_DICE; i++) {
				score += dice[i];
			}
			scoreBoard[player-1][category-1] = score;
			break;
		  case LOWER_SCORE:
			int sum_lower = 0;
			for(int i=THREE_OF_A_KIND; i<=CHANCE; i++) {
				sum_lower += scoreBoard[player-1][i-1];
			}
			score = sum_lower;
			scoreBoard[player-1][category-1] = score;
			break;
		  case TOTAL:			
			score = scoreBoard[player-1][UPPER_SCORE-1] +
					scoreBoard[player-1][UPPER_BONUS-1] +
					scoreBoard[player-1][LOWER_SCORE-1];
			scoreBoard[player-1][category-1] = score;
			break;
		  default:
			println("Invalid selection");
			break;
		}
		display.updateScorecard(category, player, score);
	}
	
	/**Calculates the score in the upper scorecard categories.*/
	private int upperScore_calculation(int category, int score) {
		score = 0;
		for(int i=0; i<N_DICE; i++) {
	    	if(dice[i] == category) {
	    		score += dice[i];
	    	}
	    }
		return score;
	}
	
	/**Returns true if minimum repetition of number happens.*/
	private boolean isRepetition(int repetition) {
		boolean flag = false;
		int[] counts = new int[6]; //to keep track of how many numbers we have of each kind from 1-6.
		for (int i=0; i<N_DICE; i++) {
		    //increase the relevant counter
		    counts[dice[i]-1]++;
		}
		
		for(int i=0; i<counts.length;  i++) {
			if(counts[i] >= repetition) {
					flag = true;
				}
		}
		return flag;
	}
	
	/**Returns true if the dice configuration presents a full house.*/
	private boolean isFullhouse() {
		int[] counts = new int[6]; //to keep track of how many numbers we have of each kind from 1-6.
		for (int i=0; i<N_DICE; i++) {
		    //increase the relevant counter
		    counts[dice[i]-1]++;
		}
		//check for pair and trio of a number
		boolean pair = false;
		boolean trio = false;
		for(int i=0; i<counts.length; i++) {
			if(counts[i] == 2) pair = true; //found 2 of a number
			if(counts[i] == 3) trio = true; //found 3 of a number
		}
		return (pair & trio);
	}
	
	/**Returns true if the dice configuration presents a straight of 4 or 5 consecutives.*/
	private boolean straight(int consecutives) {
		int[] counts = new int[6];
		for(int i=0; i<N_DICE; i++) {
			counts[dice[i]-1]++;
		}
		boolean straight = false;
		if(consecutives == 4) {
			for(int i=0; i<consecutives-1; i++){ //small straight is formed by 4 consecutive numbers
				if(counts[i] > 0 && counts[i+1] > 0 && counts[i+2] > 0 && counts[i+3] > 0) { //
					if(counts[i] <= 2 && counts[i+1] <= 2 && counts[i+2] <= 2 && counts[i+3] <= 2) {
						straight = true;
						break;
					}
				}
			}
		}
		if(consecutives == 5) {
			for(int i=0; i<consecutives-3; i++){ //large straight is formed by 5 consecutive numbers
				if(counts[i] == counts[i+1] && counts[i] == counts[i+2] &&
					counts[i] == counts[i+3] && counts[i] == counts[i+4]) {
					straight = true;
					break;
				}
			}
		}
		return straight;
	}
		
	/**Calculates final score from all players and display winner*/
	private void gameOver() {
		for(int player=1; player <= nPlayers; player++) {
			storeScore(UPPER_SCORE, player);
			storeScore(UPPER_BONUS, player);
			storeScore(LOWER_SCORE, player);
			storeScore(TOTAL, player);
		}
		int highScore = scoreBoard[0][TOTAL-1];
		String winner = playerNames[0];
		
		for(int i=1; i<nPlayers; i++) {
			int tempScore = scoreBoard[i][TOTAL-1];
			if(tempScore > highScore) {
				highScore = tempScore;
				winner = playerNames[i];
			}
		}
		display.printMessage("Congratulations, " + winner + 
							", you are the winner with a total score of " + highScore + "!");
	}
	
	/* Private instance variables */
	private int nPlayers;
	private String[] playerNames;
	private YahtzeeDisplay display;
	private RandomGenerator rgen = new RandomGenerator();
	private int[] dice;
	private int[][] scoreBoard;
}
