/*
 * File: NameSurferGraph.java
 * ---------------------------
 * This class represents the canvas on which the graph of
 * names is drawn. This class is responsible for updating
 * (redrawing) the graphs whenever the list of entries changes or the window is resized.
 */

import acm.graphics.*;
import java.awt.event.*;
import java.util.*;
import java.awt.*;

public class NameSurferGraph extends GCanvas
	implements NameSurferConstants, ComponentListener {

	/**Creates a new NameSurferGraph object that displays the data.*/
	public NameSurferGraph() {
		addComponentListener(this);
		displayEntries = new ArrayList <NameSurferEntry>();
	}
	
	/**Clears the list of name surfer entries stored inside this class.*/
	public void clear() {
		displayEntries.clear();
	}
	
	/* Method: addEntry(entry) */
	/**
	* Adds a new NameSurferEntry to the list of entries on the display.
	* Note that this method does not actually draw the graph, but
	* simply stores the entry; the graph is drawn by calling update.
	*/
	public void addEntry(NameSurferEntry entry) {
		displayEntries.add(entry);
	}
	
	/**
	* Updates the display image by deleting all the graphical objects
	* from the canvas and then reassembling the display according to
	* the list of entries. Your application must call update after
	* calling either clear or addEntry; update is also called whenever
	* the size of the canvas changes.
	*/
	public void update() {
		removeAll();
		BackGrid();
		if(displayEntries.size() != 0) {
			for(int i=0; i< displayEntries.size(); i++) {
				graphEntry(displayEntries.get(i), i);
			}
		}
	}
	
	/**Creates the background grid with the decade labels*/
	private void BackGrid() {
		//draws the outer rectangle
		int x = getWidth();
		int y = getHeight();
		add(new GRect(x, y));
		
		//draws horizontal margin lines
		add(new GLine(0, GRAPH_MARGIN_SIZE, x, GRAPH_MARGIN_SIZE));
		add(new GLine(0, y-GRAPH_MARGIN_SIZE, x, y-GRAPH_MARGIN_SIZE));
		
		//draws vertical lines and labels
		int space = x/NDECADES;
		for(int i=0; i< NDECADES; i++) {
			add(new GLine(i*space, 0, i*space, y));
			add(new GLabel(String.valueOf(START_DECADE+i*10), i*space, y-GRAPH_MARGIN_SIZE/10)); //graph_margin_size/10 is just a small offset so label is not on the bottom line.
		}
	}
	
	/*Draws graphical lines in canvas and labels*/
	private void graphEntry(NameSurferEntry entry, int entryIndex) {
		for(int i=0; i< NDECADES - 1; i++) {
			int rank0 = entry.getRank(i); 
			int rank1 = entry.getRank(i+1);
			
			double x0 = i*getWidth()/NDECADES;
			double x = (i+1)*getWidth()/NDECADES;
			double y = 0, y0 = 0; 
			
			if(rank0 != 0 && rank1 != 0) {
				y0 = GRAPH_MARGIN_SIZE + (getHeight()-GRAPH_MARGIN_SIZE*2)*rank0/MAX_RANK;
				y = GRAPH_MARGIN_SIZE + (getHeight()-GRAPH_MARGIN_SIZE*2)*rank1/MAX_RANK;
			}
			else if(rank0  == 0 && rank1 == 0) {
				y0 = getHeight() - GRAPH_MARGIN_SIZE;
				y = getHeight() - GRAPH_MARGIN_SIZE;
			}
			else if(rank0 == 0) {
				y0 = getHeight() - GRAPH_MARGIN_SIZE;
				y = GRAPH_MARGIN_SIZE + (getHeight()-GRAPH_MARGIN_SIZE*2)*rank1/MAX_RANK;
			}
			else if(rank1 == 0) {
				y0 = GRAPH_MARGIN_SIZE + (getHeight()-GRAPH_MARGIN_SIZE*2)*rank0/MAX_RANK;
				y = getHeight() - GRAPH_MARGIN_SIZE;
			}
			GLine line  = new GLine(x0, y0, x, y);
			colorRotation(line, entryIndex);
			add(line);
		}
		
		//add labels with name and rank
		for(int i=0; i<NDECADES; i++) {
			String name = entry.getName();
			int rank = entry.getRank(i);
			
			String rank_str = Integer.toString(rank);
			String label_str = name + " " + rank_str;
			
			double x = i*(getWidth()/NDECADES) + 2;
			double y = 0;
			if(rank != 0) {
				y = GRAPH_MARGIN_SIZE + (getHeight() - GRAPH_MARGIN_SIZE*2) * rank/MAX_RANK - 2;
			}
			else{
				label_str = name + " *";
				y = getHeight() - GRAPH_MARGIN_SIZE - 2;
			}
			GLabel label = new GLabel(label_str, x, y);
			colorRotation(label, entryIndex);
			add(label);
		}
	}
	
	/*Rotation of line colors: BLACK, RED, BLUE, MAGENTA*/
	private void colorRotation(GObject line, int entryIndex) {
		if(entryIndex%4 == 1) {
			line.setColor(Color.RED);
		}
		else if(entryIndex%4 == 2) {
			line.setColor(Color.BLUE);
		}
		else if(entryIndex%4 == 3) {
			line.setColor(Color.MAGENTA);
		}
	}

	/* Implementation of the ComponentListener interface */
	public void componentHidden(ComponentEvent e) { }
	public void componentMoved(ComponentEvent e) { }
	public void componentResized(ComponentEvent e) { update(); }
	public void componentShown(ComponentEvent e) { }
	
	/*Private instance variable*/
	private ArrayList <NameSurferEntry> displayEntries;
}
