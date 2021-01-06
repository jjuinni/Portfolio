/*
 * File: CheckerboardKarel.java
 * ----------------------------
 * The CheckerboardKarel class should draw
 * a checkerboard using beepers, as described in Assignment 1.  
 */

import stanford.karel.*;

public class CheckerboardKarel extends SuperKarel {

	private static final long serialVersionUID = 1L;

    public void run() {
        if (frontIsBlocked()) { //checks for a single-count column world.
        	turnLeft();       
        }
        while (frontIsClear()) {
            if (noBeepersPresent()) {
            	putBeeper();
            }
            moveKarelForward();
            if (frontIsClear()) { //checks for even-count columns in Karel’s world.
                moveKarelForward();
                if (noBeepersPresent()) { //puts a last beeper for odd-count column worlds.
                	putBeeper();
                }
            }
        }
    }
     
    /*METHOD: moveKarelForward()
     * pre-condition:
     * Karel needs to move to a direction.
     * 
     * post-condition: 
     * Karel moves forward in the set direction.
     */
    private void moveKarelForward() {
        move();
        setKarelsDirection();
    }
     
    /*METHOD: setKarelsDirection()
     * pre-condition: 
     * Karel with no clear direction.
     * 
     * post-condition: 
     * Karel with direction set when facing east, west or north. Karel never faces south.
     */
    private void setKarelsDirection() { 
        if (facingEast()) {
            if (frontIsBlocked()) {
                turnLeft();
            }
        } 
        else if (facingWest()) {
            if (frontIsBlocked()) {
                turnRight();
            }
        } 
        else if (facingNorth()) {
            if (rightIsBlocked()) {
                if (leftIsClear()) {
                    turnLeft(); 
                }               
            } 
            else if (leftIsBlocked()) {
                turnRight();
            }
        }
    }
}