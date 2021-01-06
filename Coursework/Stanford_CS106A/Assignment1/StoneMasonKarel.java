/*
 * File: StoneMasonKarel.java
 * --------------------------
 * The StoneMasonKarel subclass solves the "repair the quad"
 * problem from Assignment 1.  
 */

import stanford.karel.*;

public class StoneMasonKarel extends SuperKarel {

	private static final long serialVersionUID = 1L;

	public void run() {
		while(frontIsClear()) {
			repairColumn();
		}
	}
	
	/* METHOD: repairColumn()
	 * pre-condition:
	 * Column is damaged by quake.
	 * 
	 * post-condition:
	 * Column is repaired.
	 */
	private void repairColumn() {
		turnLeft();
	    ascendColumn();
	    turnAround();
	    descendColumn();
	    turnLeft();
	    if(frontIsClear()) {
	    	moveToNextColumn();
	        repairColumn();
	        }
	 }
	            
	/* METHOD:ascendColumn()
	 * pre-condition: 
	 * Karel is at the bottom of the column facing north.
	 * 
	 * post-condition: 
	 * Karel fixed the column and is at the top of it.
	 */
	private void ascendColumn() {
		while(frontIsClear()) {
            if(noBeepersPresent()) {
                putBeeper();
            }
            move();
        }
        if(noBeepersPresent()) {
            putBeeper();
        }
	}
	
	/* METHOD:descendColumn()
	 * pre-condition: 
	 * Karel is at the top of the column facing south.
	 * 
	 * post-condition: 
	 * Karel is at the bottom of the column facing the wall.
	 */
	private void descendColumn() {
		while(frontIsClear()) {
            move();
        }
	}
	
	/*METHOD:MoveToNextColumns()
	 * pre-condition:
	 * Karel finished repairing current column and its facing east.
	 * 
	 * post-condition:
	 * Karel moved to the next column and its facing east.
	 */
	private void moveToNextColumn() {
			for(int i=0; i<4; i++) {
				move();
			}
		}	
}