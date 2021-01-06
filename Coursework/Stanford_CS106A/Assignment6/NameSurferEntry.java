/*
 * File: NameSurferEntry.java
 * --------------------------
 * This class represents a single entry in the database.  Each
 * NameSurferEntry contains a name and a list giving the popularity
 * of that name for each decade stretching back to 1900.
 */

import acm.util.*;
import java.util.*;

public class NameSurferEntry implements NameSurferConstants {

/* Constructor: NameSurferEntry(line) */
/**
 * Creates a new NameSurferEntry from a data line as it appears
 * in the data file.  Each line begins with the name, which is
 * followed by integers giving the rank of that name for each
 * decade.
 */
	public NameSurferEntry(String line) {	
		String[] lineA = line.split(" ");
		name = lineA[0];
		for(int i=1; i<lineA.length; i++) { //Parse ranks from String to integer
			ranks[i-1] = Integer.parseInt(lineA[i]);
		}
	}

/* Method: getName() */
/**
 * Returns the name associated with this entry.
 */
	public String getName() {
		return name;
	}

/* Method: getRank(decade) */
/**
 * Returns the rank associated with an entry for a particular
 * decade.  The decade value is an integer indicating how many
 * decades have passed since the first year in the database,
 * which is given by the constant START_DECADE.  If a name does
 * not appear in a decade, the rank value is 0.
 */
	public int getRank(int decade) {
		for(int i=0; i<ranks.length; i++) {
			if(decade == i) {
				return ranks[decade];
			}
		}
		return ranks[decade];
	}

/* Method: toString() */
/**
 * Returns a string that makes it easy to see the value of a
 * NameSurferEntry.
 */
	public String toString() {
		String str = name + " [";
		for(int i=0; i<NDECADES; i++) {
			str += getRank(i) + " ";
		}
		str += "]";
		return str;
	}
	
	/*Private Instance Variables*/
	private String name;
	private int[] ranks = new int[NDECADES];
}

