/*
 * File: ProgramHierarchy.java
 * ---------------------------
 * This file draws the program hierarchy illustration.
 */

import acm.graphics.*;
import acm.program.*;

public class ProgramHierarchy extends GraphicsProgram {	
	private static final long serialVersionUID = 1L;
	
	private static final int BOX_WIDTH = 120;

	private static final int BOX_HEIGHT = 40;
	
	private static final int a = 30; //horizontal space between boxes.
	private static final int b = 40; //vertical space between boxes.
	
	public void run() {
		textBox1();
		textBox2();
		textBox3();
		textBox4();
		line1();
		line2();
		line3();
	}
	
	/*METHODS: textBox1_4()
	 * pre-condition: No box&text.
	 * post-condition: centered box and label.
	 */
	private void textBox1()  {
		double x = getWidth()/2 - BOX_WIDTH/2;
		double y = getHeight()/2 - b/2 - BOX_HEIGHT;
		
		GRect box = new GRect(x, y, BOX_WIDTH, BOX_HEIGHT);
		GLabel text = new GLabel ("Program", x, y);
		
		add(box);
		add(text);	//adds the "Program" string, but in the wrong location(x,y).	
		
		double textWidth = text.getWidth()/2;
		double textAscent = text.getAscent()/2;
		
		text.move(BOX_WIDTH/2 - textWidth, BOX_HEIGHT/2 + textAscent); //label centered inside the box.

	}
	
	private void textBox2()  {
		double x = getWidth()/2 - BOX_WIDTH*3/2 - a;
		double y = getHeight()/2 + b/2;
		
		GRect box = new GRect(x, y, BOX_WIDTH, BOX_HEIGHT);
		GLabel text = new GLabel("GraphicsProgram", x, y);
		
		add(box);
		add(text);
		
		double textWidth = text.getWidth()/2;
		double textAscent = text.getAscent()/2;
		
		text.move(BOX_WIDTH/2 - textWidth, BOX_HEIGHT/2 + textAscent);
	}
	
	private void textBox3()  {
		double x = getWidth()/2 - BOX_WIDTH/2;
		double y = getHeight()/2 + b/2;
		
		GRect box = new GRect(x, y, BOX_WIDTH, BOX_HEIGHT);
		GLabel text = new GLabel("ConsoleProgram", x, y);
		
		add(box);
		add(text);
		
		double textWidth = text.getWidth()/2;
		double textAscent = text.getAscent()/2;
		
		text.move(BOX_WIDTH/2 - textWidth, BOX_HEIGHT/2 + textAscent);
	}
	
	private void textBox4()  {
		double x = getWidth()/2 + BOX_WIDTH/2 + a;
		double y = getHeight()/2 + b/2;
		
		GRect box = new GRect(x, y, BOX_WIDTH, BOX_HEIGHT);
		GLabel text = new GLabel("DialogProgram", x, y);
		
		add(box);
		add(text);	
		
		double textWidth = text.getWidth()/2;
		double textAscent = text.getAscent()/2;
		
		text.move(BOX_WIDTH/2 - textWidth, BOX_HEIGHT/2 + textAscent);
	}
	
	/*METHODs:line1_3()
	 * pre-condition: no line.
	 * post-condition: lines from upper box to all three lower boxes. Centered to connect the middle of the line.
	 */
	private void line1() {
		double x0 = getWidth()/2;
		double y0 = getHeight()/2 - b/2;
		double x =  getWidth()/2;
		double y = getHeight()/2 + b/2;
		
		GLine line = new GLine(x0, y0, x, y);
		add(line);
	}
	
	private void line2() {
		double x0 = getWidth()/2;
		double y0 = getHeight()/2 - b/2;
		double x =  getWidth()/2 - BOX_WIDTH - a;
		double y = getHeight()/2 + b/2;
		
		GLine line = new GLine(x0, y0, x, y);
		add(line);
	}
	
	private void line3() {
		double x0 = getWidth()/2;
		double y0 = getHeight()/2 - b/2;
		double x =  getWidth()/2 + BOX_WIDTH + a;
		double y = getHeight()/2 + b/2;
		
		GLine line = new GLine(x0, y0, x, y);
		add(line);
	}
}

