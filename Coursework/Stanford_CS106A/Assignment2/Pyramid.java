/*
 * File: Pyramid.java
 * ------------------
 * stack equal size bricks in a symmetric Pyramid shape and prompt it.
 */

import acm.graphics.*;
import acm.program.*;


public class Pyramid extends GraphicsProgram {

	private static final long serialVersionUID = 1L;
	
/** Width of each brick in pixels */
	private static final int BRICK_WIDTH = 30;

/** Width of each brick in pixels */
	private static final int BRICK_HEIGHT = 12;

/** Number of bricks in the base of the pyramid */
	private static final int BRICKS_IN_BASE = 14;
	
	public void run() {
		for(int i=0; i<BRICKS_IN_BASE; i++) {
			addBrick();
		}
	}

	/*METHOD:addBrick()
	 * pre-condition: -
	 * 
	 * post-condition:
	 * Bricks added row by row in pyramid placed in the center of the screen.
	 */
	private void addBrick() {
		int rowNo = 0;
		int x = getWidth()/2 - BRICK_WIDTH*7;
		int y = getHeight() - BRICK_HEIGHT;

			for(int i=0; i<(BRICKS_IN_BASE - rowNo);i++) {
				GRect brick = new GRect(x+BRICK_WIDTH/2*rowNo, y-BRICK_HEIGHT*rowNo, 30, 12);
				add(brick);
				brick.move(BRICK_WIDTH*i, 0);
			}
			rowNo++;
	}
	

}

