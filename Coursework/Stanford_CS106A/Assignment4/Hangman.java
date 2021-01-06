/*
 * File: Hangman.java
 * ------------------
 * This program will eventually play the Hangman game from
 * Assignment #4.
 */

import acm.graphics.*;
import acm.program.*;
import acm.util.*;

import java.awt.*;

public class Hangman extends ConsoleProgram {

	//initializes the canvas and adds it to the	window prior to the run method being executed.
	public void init() {
		canvas = new HangmanCanvas();
		add(canvas);
		}
	
	public void run() {
    	//choose random word  to use as secret word
    	secret_word = lexicon.getWord(rgen.nextInt(0, lexicon.getWordCount()-1));
    	//println(secret_word); //just for debugging
    	for(int i=0; i<secret_word.length(); i++) { //initial display of guessed_word
    		guessed_word += "-";
    	}
    	
    	//control structure
    	println("Welcome to Hangman!");
    	canvas.reset();
    		
    	while(guesses != 0 && secret_word.equals(guessed_word) == false){
    		println("The word now  looks like this: " + guessed_word);
    		canvas.displayWord(guessed_word);
    		
    		if(guesses != 1) {
    			println("You have " + guesses + " left.");
    		}else {
    			println("Youn have only one guess left.");
    		}
    		String str = readLine("Your guess: ");
    		str = str.toUpperCase();
    		if(str.length() != 1){ //allows only single character guess.
    			println("Illegal guess.");
    			str = readLine("Try a new valid guess: ");
    			str = str.toUpperCase();
    		}
    		for(int i=0; i<secret_word.length(); i++) {  //check if there is a match
    			if(str.equals(String.valueOf(secret_word.charAt(i)))){ //replace 
    				guessed_word = guessed_word.substring(0, i) + 
    								str + 
    								guessed_word.substring(i+1, guessed_word.length());
    				guessed = true;
    			}
    		}
    		if(guessed == false && str.length() == 1) {
    			println("There are no " + str + "'s in the word.");
    			canvas.noteIncorrectGuess(str.charAt(0));
    			guesses -= 1;
    		}else {
    			println("That guess is correct.");
    			guessed = false; //resets guessed to false
    		}
    	}
    	if(secret_word.equals(guessed_word)) {
    		println("You guessed the word: " + secret_word);
    		canvas.displayWord(guessed_word);
    		println("You win.");
    	}else {
    		println("You're completely hung.");
    		println("The word was: " + secret_word);
    		canvas.displayWord(guessed_word);
    		println("You lose.");
    	}
	}

    /*Private instance variables*/
	private HangmanLexicon lexicon =  new HangmanLexicon();
    private RandomGenerator rgen = RandomGenerator.getInstance();
    private String guessed_word = ""; //keep track of user's partially guessed word
    private int guesses = 8; //keep track of guesses made by user
    private String secret_word; //secret_word
    private boolean guessed = false; //keep track if there was a correct guess in a try
    private HangmanCanvas canvas;
}
