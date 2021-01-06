/*
 * File: Hailstone.java
 * --------------------
 * Prompt illustration of the Hailstone problem.
 */

import acm.program.*;

public class Hailstone extends ConsoleProgram {
	private static final long serialVersionUID = 1L;
	
	private static final int SENTINEL = 1; 
	
	public void run() {

		int n = readInt("Enter a number: ");

		int stepCounter = 0;
		while(n != SENTINEL) {
			/*If number is even will divide by two + show the result*/
			if(n%2 == 0) {
				int evenNoResult = n/2;
				stepCounter++;
				println(n + " is even so I take half: " + evenNoResult);
				n = evenNoResult; //new n.
			}
			/*If number is odd will multiply by 3 and add one + show the result*/
			else if(n%2 != 0) {
				int oddNoResult  = 3*n+1;
				stepCounter++;
				println(n + " is odd, so I make 3n + 1: " + oddNoResult);
				n = oddNoResult; //new n.
			}
		}
		println("The process took " + stepCounter + " to reach " + SENTINEL);
	}
	

}

