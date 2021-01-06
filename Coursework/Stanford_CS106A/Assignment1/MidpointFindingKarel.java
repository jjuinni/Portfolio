/*
 * File: MidpointFindingKarel.java
 * -------------------------------
 * the MidpointFindingKarel class should
 * leave a beeper on the corner closest to the center of 1st Street
 * (or either of the two central corners if 1st Street has an even
 * number of corners).  Karel puts down additional beepers as it
 * looks for the midpoint, but also pick them up again before it
 * stops.  The world may be of any size, but you are allowed to
 * assume that it is at least as tall as it is wide.
 */

import stanford.karel.*;

public class MidpointFindingKarel extends SuperKarel {

	private static final long serialVersionUID = 1L;

	public void run() {
		checkWidthOfWorld();
		cleanBeepers();
		if(frontIsClear()) {
			goToMiddle();
		}
		putBeeper();
		widthCount = 0; //reset counter
		
	}
		
	/*METHOD:checkWidthOfWorld()
	 * pre-condition:
	 * World's width is not known.
	 * 
	 * post-condition:
	 * Karel puts 1 Beeper for every column. Number of Beepers dropped indicate width of the world.
	 * Karel is facing the east wall.
	 */
	private void checkWidthOfWorld() {
		widthCount = 0;
		while(frontIsClear()) {
			putBeeper();
			move();	
			widthCount++;
		}
		putBeeper();
		widthCount++;
		
	}
	
	/*METHOD:cleanBeepers()
	 * pre-condition:
	 * 1st row full with Beepers.
	 * 
	 * post-condition:
	 * 1st row with no Beepers. Karel is at 1st Avenue and 1st Street facing east.
	 */
	private void cleanBeepers() {
		turnAround();
		while(beepersPresent() & frontIsClear()) {
			pickBeeper();
			move();	
		}
		if(frontIsBlocked()) {
			pickBeeper();
			turnAround();
		}
		
	}
	
	/*METHOD:goToMiddle()
	 * pre-condition: No Beepers present.
	 * 
	 * post-condition: Karel moves to the midpoint of 1st Street.
	 */
	private void goToMiddle() {
		widthCount = 0;
		if(widthCount % 2 == 0) { //even
			for(int i=0; i<widthCount/2; i++) {
				move();
			}
		} 
		
		else if(widthCount % 2 != 0) { //odd
			for(double i=0; i<(widthCount/2-0.5); i++) {
				move();
			}
			
		}
	
	}
	
	/*Private instance variable*/
	private int widthCount; //used on METHODS:checkWidthOfWorld() & goToMiddle(). 
}
