/*
 * File: HangmanCanvas.java
 * ------------------------
 * This file keeps track of the Hangman display.
 */

import acm.graphics.*;
import acm.util.ErrorException;

public class HangmanCanvas extends GCanvas {

/** Resets the display so that only the scaffold appears */
	public void reset() {
		//HIPS(height) && BODY(width) are the middle of the Canvas 
		int offset = ROPE_LENGTH + HEAD_RADIUS + BODY_LENGTH; //hips height is the middle of screen
		int x0 = getWidth()/2 - BEAM_LENGTH;
		int y0 = getHeight()/2 - offset;
		GLine scaffold = new GLine(x0, y0, x0, y0+SCAFFOLD_HEIGHT);
		GLine beam = new GLine(x0, y0, getWidth()/2, y0);
		GLine rope = new GLine(getWidth()/2, y0, getWidth()/2, y0+ROPE_LENGTH);
		add(scaffold);
		add(beam);
		add(rope);
	}

/**
 * Updates the word on the screen to correspond to the current
 * state of the game.  The argument string shows what letters have
 * been guessed so far; unguessed letters are indicated by hyphens.
 */
	public void displayWord(String word) {
		guessed_word.setLabel(word);
		guessed_word.setLocation(getWidth()/2 - BEAM_LENGTH,
									getHeight()/2 + SCAFFOLD_HEIGHT/2 + 10); //10 is a random offset
		guessed_word.setFont("Times New Roman-30");
		remove(guessed_word);
		add(guessed_word);
	}

/**
 * Updates the display to correspond to an incorrect guess by the
 * user.  Calling this method causes the next body part to appear
 * on the scaffold and adds the letter to the list of incorrect
 * guesses that appears at the bottom of the window.
 */
	/*Helper private methods: create ivars of each body part to be added*/
	/*Add head*/
	private void head() {
		GOval circle = new GOval((getWidth()-HEAD_RADIUS)/2,
									getHeight()/2-BODY_LENGTH-HEAD_RADIUS,
									HEAD_RADIUS, HEAD_RADIUS);
		add(circle);
	}
	/*Add body*/
	private void body() {
		GLine body = new GLine(getWidth()/2, getHeight()/2-BODY_LENGTH,
								getWidth()/2, getHeight()/2);
		add(body);
	}
	/*Add left arm*/
	private void leftArm() {
		int x = getWidth()/2 - UPPER_ARM_LENGTH;
		int y = getHeight()/2 - BODY_LENGTH + ARM_OFFSET_FROM_HEAD;
		GLine leftArm = new GLine(x, y,	getWidth()/2, y);
		GLine leftHand = new GLine(x, y, x, y+LOWER_ARM_LENGTH);
		add(leftHand);
		add(leftArm);
	}
	/*Add right arm*/
	private void rightArm() {
		int x = getWidth()/2 + UPPER_ARM_LENGTH;
		int y = getHeight()/2 - BODY_LENGTH + ARM_OFFSET_FROM_HEAD;
		GLine rightArm = new GLine(getWidth()/2, y,	getWidth()/2+UPPER_ARM_LENGTH, y);
		GLine rightHand = new GLine(x, y, x, y+LOWER_ARM_LENGTH);
		add(rightHand);
		add(rightArm);
	}
	/*Add left leg*/
	private void leftLeg() {
		int x = (getWidth() - HIP_WIDTH)/2;
		int y = getHeight()/2;
		GLine leftLeg = new GLine(x, y, x, y+LEG_LENGTH);
		GLine hips = new GLine(x, y, x+HIP_WIDTH/2, y);
		add(hips);
		add(leftLeg);
	}
	/*Add right leg*/
	private void rightLeg() {
		int x = (getWidth() + HIP_WIDTH)/2;
		int y = getHeight()/2;
		GLine rightLeg = new GLine(x, y, x, y+LEG_LENGTH);
		GLine hips = new GLine(x-HIP_WIDTH/2, y, x, y);
		add(hips);
		add(rightLeg);
	}
	/*Add left foot*/
	private void leftFoot() {
		int x = (getWidth() - HIP_WIDTH)/2 - FOOT_LENGTH;
		int y = getHeight()/2 + LEG_LENGTH;
		GLine leftFoot = new GLine(x, y, x+FOOT_LENGTH, y);
		add(leftFoot);
	}
	/*Add right foot*/
	private void rightFoot() {
		int x = (getWidth() + HIP_WIDTH)/2;
		int y = getHeight()/2 + LEG_LENGTH;
		GLine rightFoot = new GLine(x, y, x+FOOT_LENGTH, y);
		add(rightFoot);
	}
	
	public void noteIncorrectGuess(char letter) {
		incorrect += String.valueOf(letter).toUpperCase();
		GLabel incorrectLetters = new GLabel(incorrect, 
											getWidth()/2 - BEAM_LENGTH,
											getHeight()/2 + SCAFFOLD_HEIGHT/2 + 30); //30 is an offsets
		incorrectLetters.setFont("Times New Roman-20");
		add(incorrectLetters);

		switch (incorrect.length()) {
			case 1:  head(); break;
			case 2:  body(); break;
			case 3:  leftArm(); break;
			case 4:  rightArm(); break;
			case 5:  leftLeg(); break;
			case 6:  rightLeg(); break;
			case 7:  leftFoot(); break;
			case 8:  rightFoot(); break;
		}
	}

/* Constants for the simple version of the picture (in pixels) */
	private static final int SCAFFOLD_HEIGHT = 360;
	private static final int BEAM_LENGTH = 144;
	private static final int ROPE_LENGTH = 18;
	private static final int HEAD_RADIUS = 36;
	private static final int BODY_LENGTH = 144;
	private static final int ARM_OFFSET_FROM_HEAD = 28;
	private static final int UPPER_ARM_LENGTH = 72;
	private static final int LOWER_ARM_LENGTH = 44;
	private static final int HIP_WIDTH = 36;
	private static final int LEG_LENGTH = 108;
	private static final int FOOT_LENGTH = 28;
	
	/*Private instance variable*/
	private String incorrect = ""; //keep track of incorrect guesses
	private GLabel guessed_word = new GLabel(""); //keep track/update guessed_word displayed in Canvas
}
