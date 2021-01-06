/*
 * File: PythagoreanTheorem.java
 * -----------------------------
 * This program solves an equation using pythagorean theorem.
 */

import acm.program.*;

public class PythagoreanTheorem extends ConsoleProgram {
	
	private static final long serialVersionUID = 1L;
	
	public void run() {
		
		println("Enter values to compute Pythagorean theorem");
		solvePythagoras();
	}
	
	/*Gives result of pythagorean theorem*/
	private void solvePythagoras() {
		int value_a = readInt("a: ");
		int value_b = readInt("b: ");
		double result_c = Math.sqrt(value_a*value_a + value_b*value_b);
		println("c = " + result_c);
	}
}
