/*
 * File: Target.java
 * Name: 
 * Section Leader: 
 * -----------------
 * Target supermarket logo symbol is drawn.
 */

import acm.graphics.*;
import acm.program.*;
import java.awt.*;

public class Target extends GraphicsProgram {	
	
	private static final long serialVersionUID = 1L;
	
	public void run() {	
		outterCircle();
		middleCircle();
		innerCircle();
		}
	
	/*Returns pixels equivalent to inches*/
	private double InchToPixel (double inch) {
		return 72*inch;
	}
	
	/*Draws the outterCircle*/
	private void outterCircle() {
		double r1 = InchToPixel(1);
		
		double x = getWidth()/2 - r1;
		double y = getHeight()/2 - r1;
		
		GOval outterCircle = new GOval(x, y, 2*r1, 2*r1);
		outterCircle.setColor(Color.RED);
		outterCircle.setFilled(true);
		add(outterCircle); 
	}
	
	/*Draws the middleCircle*/
	private void middleCircle() {
		double r1 = InchToPixel(1);
		double r2 = InchToPixel(0.65);
		
		double x = getWidth()/2 - r1;
		double y = getHeight()/2 - r1;
		
		GOval middleCircle = new GOval(x+r1-r2, y+r1-r2, 2*r2, 2*r2);
		middleCircle.setColor(Color.WHITE);
		middleCircle.setFilled(true);
		add(middleCircle);
	}
	
	/*Draws the innerCircle*/
	private void innerCircle() {
		double r1 = InchToPixel(1);
		double r3 = InchToPixel(0.3);
		
		double x = getWidth()/2 - r1;
		double y = getHeight()/2 - r1;
		
		GOval innerCircle = new GOval(x+r1-r3, y+r1-r3, 2*r3, 2*r3);
		innerCircle.setColor(Color.RED);
		innerCircle.setFilled(true);
		add(innerCircle);
	}
}
