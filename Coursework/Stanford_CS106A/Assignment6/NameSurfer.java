/*
 * File: NameSurfer.java
 * ---------------------
 * When it is finished, this program will implements the viewer for
 * the baby-name database described in the assignment handout.
 */

import acm.program.*;
import java.awt.event.*;
import javax.swing.*;

public class NameSurfer extends Program implements NameSurferConstants {

	/*for export as a JAR file*/
	public static void main(String[] args) {
		new NameSurfer().start(args);
	}
	
	/*Constructor: NameSurfer()*/
	/**
	 * The constructor has the job of setting up the data structures for
	 * the application and putting things up on the screen.
	 */
	public NameSurfer() {
	
	}
	
/* Method: init() */
/**
 * This method has the responsibility for reading in the data base
 * and initializing the interactors at the bottom of the window.
 */
	public void init() {
		graph = new JButton("Graph");
		clear = new JButton("Clear");
		nameField = new JTextField(10);
		display = new NameSurferGraph();
			    
		add(new JLabel("Name"), SOUTH);
		add(nameField, SOUTH);
		add(graph, SOUTH);
	    add(clear, SOUTH);
	    add(display);
	      
	    nameField.addActionListener(this);
	    addActionListeners();
	    
	    //read in file and store its information
	    data = new NameSurferDataBase(NAMES_DATA_FILE);		  
	}
	
/* Method: actionPerformed(e) */
/**
 * This class is responsible for detecting when the buttons are
 * clicked, so you will have to define a method to respond to
 * button actions.
 */
	public void actionPerformed(ActionEvent e) {
		if(e.getSource() == clear) {
			display.clear();
			display.update();
		} else {
			entry = data.findEntry(nameField.getText());
			if(entry != null) {
				display.addEntry(entry);
				display.update();
			}
		}
	}
	
	/*Private instance variables*/
	private JButton graph;
	private JButton clear;
	private JTextField nameField;
	
	private NameSurferEntry entry;
	private NameSurferDataBase data;	
	private NameSurferGraph display;
}

