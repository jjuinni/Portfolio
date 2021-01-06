/*
 * File: FindRange.java
 * Name: 
 * Section Leader: 
 * --------------------
 * Will read user input to evaluate largest && smallest numbers till it stops.
 */

import acm.program.*;

public class FindRange extends ConsoleProgram {
	
	private static final long serialVersionUID = 1L;
	
	private static final int SENTINEL = 0;
	
	public void run() {
		println("This program finds the largest and smallest numbers.");
		findRange();
	}
	
	/*Will read user number and evaluate if its largest && smallest until the SENTINEL is signaled to stop*/
	private void findRange() {
		int firstNo = readInt("?");
		if(firstNo == SENTINEL) {
			println("No values have been entered!");
		}
		//initially, largest and smallest number are the same first number entered.
		int smallestNo = firstNo; 
		int largestNo = firstNo;
		
		/*WHILE LOOP
		* Pre-condition: 
		* First User input is not equal to the SENTINEL(==0).
		* Need to compare each new number User enters to the previews smallest and largest numbers. 
		* 
		* Post-condition: 
		* Stores the smallest or largest if they are smallest or largest.
		* Prompt results after SENTINEL is signaled.
		* Prompt special condition when the second User input is SENTINEL.
		*/
		int secondNoCounter = 0; //only used for 1st if case condition on while loop.
		while(firstNo != SENTINEL) {
			int secondNo = readInt("?");
			secondNoCounter++;
			if(secondNo == SENTINEL && secondNoCounter == 1) {
				println(firstNo + " is both the largest and smallest number.");
			}
			if(smallestNo < secondNo && secondNo != SENTINEL) { 
					smallestNo = secondNo;
			}
			if(largestNo > secondNo && secondNo != SENTINEL) {
					largestNo = secondNo;
			}
			if(secondNo == SENTINEL) { 
				println ("smallest: " + smallestNo); 
				println ("largest: " + largestNo); 
				break;
			}
		}
	}
}

