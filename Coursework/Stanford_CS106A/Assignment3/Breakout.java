/*
 * File: Breakout.java
 * -------------------
 * Name:
 * Section Leader:
 * 
 * This file will eventually implement the game of Breakout.
 */

import acm.graphics.*;
import acm.program.*;
import acm.util.*;

import java.applet.*;
import java.awt.*;
import java.awt.event.*;

public class Breakout extends GraphicsProgram {
	private static final long serialVersionUID = 1L;

/** Width and height of application window in pixels */
	public static final int APPLICATION_WIDTH = 400;
	public static final int APPLICATION_HEIGHT = 600;

/** Dimensions of game board (usually the same) */
	private static final int WIDTH = APPLICATION_WIDTH;
	private static final int HEIGHT = APPLICATION_HEIGHT;

/** Dimensions of the paddle */
	private static final int PADDLE_WIDTH = 60;
	private static final int PADDLE_HEIGHT = 10;

/** Offset of the paddle up from the bottom */
	private static final int PADDLE_Y_OFFSET = 30;

/** Number of bricks per row */
	private static final int NBRICKS_PER_ROW = 10;

/** Number of rows of bricks */
	private static final int NBRICK_ROWS = 10;

/** Separation between bricks */
	private static final int BRICK_SEP = 4;

/** Width of a brick */
	private static final int BRICK_WIDTH =
	  (WIDTH - (NBRICKS_PER_ROW - 1) * BRICK_SEP) / NBRICKS_PER_ROW;

/** Height of a brick */
	private static final int BRICK_HEIGHT = 8;

/** Radius of the ball in pixels */
	private static final int BALL_RADIUS = 5;

/** Offset of the top brick row from the top */
	private static final int BRICK_Y_OFFSET = 70;

/** Number of turns */
	private static final int NTURNS = 3;
	
/** Animation delay or pause time between ball moves */
	private static final int DELAY = 8;

/* Method: run() */
/** Runs the BreakOut program. */
	public void run() {
			setBricks();
			setPaddle();
			setBall();
			addMouseListeners();
			clickToStart();
			
			lifes = NTURNS;
			remainingBricks = NBRICK_ROWS*NBRICKS_PER_ROW;
			while (remainingBricks != 0 && lifes != 0) { //keeps ball moving in game
				moveBall();
				pause(DELAY);
				GObject collider = getCollidingObject();
				if(collider == paddle) {
					bounceClip.play();
					vy = -1 * Math.abs(vy); //prevents ball "glued" to paddle problem.
				}
				else if(collider != null) {
					remove(collider);
					bounceClip.play();
					remainingBricks--;
					vy = -vy;
				}
			}
			if(lifes == 0) {
				gameOver();
			}
			else if(remainingBricks == 0) {
				gameWin();
				remove(ball);
				setBall();
			}
	}
	
	/**Prompt start instruction and wait for click to start game*/
	private void clickToStart() {
		GLabel toStart = new GLabel("Click left mouse buttom to start playing!");
		toStart.setColor(Color.RED);
		toStart.setFont("SansSerift-20");
		toStart.setLocation((WIDTH - toStart.getWidth())/2, (HEIGHT - toStart.getHeight())/2);
		add(toStart);
		waitForClick();
		remove(toStart);
	}
	
	/**Prompt Game Over! when user loses the game*/
	private void gameOver() {
		GLabel gameOver = new GLabel("You lost three times. Game Over!");
		gameOver.setFont("SansSerift-26");
		gameOver.setLocation((WIDTH - gameOver.getWidth())/2, (HEIGHT - gameOver.getHeight())/2);
		gameOver.setColor(Color.RED);
		add(gameOver);
	}
	
	/**Prompt You won! when user wins the game*/
	private void gameWin() {
		GLabel gameWin = new GLabel("You won!");
		gameWin.setFont("SansSerift-26");
		gameWin.setLocation((WIDTH - gameWin.getWidth())/2, (HEIGHT - gameWin.getHeight())/2);
		gameWin.setColor(Color.RED);
		add(gameWin);
	}
	
	/** Sets up the bricks of the game */
	private void setBricks() {
		int rowNo = 0; //Keeps track of current row.
		for(int i=0; i<NBRICK_ROWS; i++) {
			double x = (WIDTH - 10*BRICK_WIDTH -  9*BRICK_SEP)/2;
			double y = BRICK_Y_OFFSET + (BRICK_HEIGHT + BRICK_SEP)*rowNo; 
			
			for(int j=0; j<NBRICKS_PER_ROW; j++) {//add bricks in the row.
				if(rowNo == 0 || rowNo == 1) {
					GRect brick = new GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT);
					brick.setFilled(true);
					brick.setColor(Color.RED);
					add(brick);
					brick.move((BRICK_WIDTH + BRICK_SEP)*j, 0);
				}
				else if(rowNo == 2 || rowNo == 3) {
					GRect brick = new GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT);
					brick.setFilled(true);
					brick.setColor(Color.ORANGE);
					add(brick);
					brick.move((BRICK_WIDTH + BRICK_SEP)*j, 0);
				}
				else if(rowNo == 4 || rowNo == 5) {
					GRect brick = new GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT);
					brick.setFilled(true);
					brick.setColor(Color.YELLOW);
					add(brick);
					brick.move((BRICK_WIDTH + BRICK_SEP)*j, 0);
				}
				else if(rowNo == 6 || rowNo == 7) {
					GRect brick = new GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT);
					brick.setFilled(true);
					brick.setColor(Color.GREEN);
					add(brick);
					brick.move((BRICK_WIDTH + BRICK_SEP)*j, 0);
				}
				else if(rowNo == 8 || rowNo == 9) {
					GRect brick = new GRect(x, y, BRICK_WIDTH, BRICK_HEIGHT);
					brick.setFilled(true);
					brick.setColor(Color.CYAN);
					add(brick);
					brick.move((BRICK_WIDTH + BRICK_SEP)*j, 0);
				}
			}
			rowNo++;
		}
	}

	/**Sets up the paddle of the game*/
	private void setPaddle() {
		double x = (WIDTH - PADDLE_WIDTH)/2;
		double y = (HEIGHT - PADDLE_Y_OFFSET);
		paddle = new GRect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT);
		paddle.setFilled(true);
		add(paddle);
	}
	
	/**tracks paddle location*/
	public void mouseMoved(MouseEvent e) {
		double y = (HEIGHT - PADDLE_Y_OFFSET);
		double x = e.getX();
		if(x < WIDTH - PADDLE_WIDTH) {
			paddle.setLocation(x, y);
		} else {
			paddle.setLocation(WIDTH - PADDLE_WIDTH, y);
		}	
	}
	
	/**Sets ball and it's initial values*/
	private void setBall() {
		double x = WIDTH/2 - BALL_RADIUS;
		double y = HEIGHT/2 - BALL_RADIUS;
		ball = new GOval(x, y, 2*BALL_RADIUS, 2*BALL_RADIUS);
		ball.setFilled(true);
		add(ball);
		
		vx = rgen.nextDouble(1.0, 3.0); //initial x velocity
		if (rgen.nextBoolean(0.5)) vx = -vx;
		vy = 3.0; //initial y velocity
	}
	
	/**Move the ball and bounces the ball accordingly*/
	private void moveBall() {
		ball.move(vx, vy);
		
		/*IF ball have gone beyond boundary*/
		if (ball.getY() > HEIGHT - 2*BALL_RADIUS) { 
			// change ball's Y velocity to now bounce upwards
			lifes--;
			remove(ball);
			setBall();
			
			GLabel currentLife = new GLabel(lifes + " remaining changes!");
			currentLife.setColor(Color.RED);
			currentLife.setFont("SansSerift-26");
			currentLife.setLocation((WIDTH - currentLife.getWidth())/2, (HEIGHT - currentLife.getHeight())/2);
			add(currentLife);
			pause(1500);
			remove(currentLife);
			
			waitForClick();
		}
		if (ball.getY() < 0) {
			vy = -vy;
		}
		if(ball.getX() < 0) {
			vx = -vx;
		}
		if(ball.getX() > WIDTH - 2*BALL_RADIUS) {
			vx = -vx;
		}
	}
	
	/** Check a few carefully chosen points on the outside of the ball and see whether any of those
	 * points has collided with anything */
	private GObject getCollidingObject() {
		if(getElementAt(ball.getX(), ball.getY()) != null) {
			return getElementAt(ball.getX(), ball.getY());
		}
		else if(getElementAt(ball.getX()+ 2*BALL_RADIUS, ball.getY()) != null) {
			return getElementAt(ball.getX() + 2*BALL_RADIUS, ball.getY());
		}
		else if(getElementAt(ball.getX() + 2*BALL_RADIUS, ball.getY() + 2*BALL_RADIUS) != null) {
			return getElementAt(ball.getX() + 2*BALL_RADIUS, ball.getY() + 2*BALL_RADIUS);
		}
		else if(getElementAt(ball.getX(), ball.getY() + 2*BALL_RADIUS) != null) {
			return getElementAt(ball.getX(), ball.getY() + 2*BALL_RADIUS);
		}
		else {
			return null;
		}
	}
	
	/* Private instance variables */
	private GRect paddle; //keep track of paddle
	private GOval ball; //keep track of ball
	private int lifes; //keep track of remaining lifes
	private int remainingBricks; //keep track of remaining bricks
	private double vx, vy; //keep track of the velocity of the ball
	private RandomGenerator rgen = RandomGenerator.getInstance();
	
	// MediaTools class and its AudioClip method add a sound effect for ball collisions
    private AudioClip bounceClip = MediaTools.loadAudioClip("bounce.au");   
}
