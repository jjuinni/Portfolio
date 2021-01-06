/*
 * File: HangmanLexicon.java
 * -------------------------
 * This file contains a stub implementation of the HangmanLexicon
 * class that you will reimplement for Part III of the assignment.
 */ 
import acm.util.*;
import java.io.*;
import java.util.*;

public class HangmanLexicon {

	/**HangmanLexicon constructor: open file .txt using BufferedReader that will allow to read it line by line.
	 * Reads the lines from the file into an ArrayList*/
	public HangmanLexicon() {	
		try {
        	File file = new File("HangmanLexicon.txt");
    		FileReader fr = new FileReader(file);
    		BufferedReader in = new BufferedReader(fr);		
    		for(String line = in.readLine(); line != null; line = in.readLine()) {
    			fileWords.add(line);
    		}
//    		OR
//    		while(true) {
//    			String line = in.readLine();
//    			if(line == null) break;
//    			fileWords.add(line);
//    		}
    		in.close();
    		fr.close();
        } catch (IOException e) {
            throw new ErrorException(e);
        }
	}
	
/** Returns the number of words in the lexicon. */
	public int getWordCount() {
		return fileWords.size();
	}

/** Returns the word at the specified index. */
	public String getWord(int index) {
		return fileWords.get(index);
	}
	
	/*Private instance variable*/
	private ArrayList <String> fileWords = new ArrayList <String> (); //array of words in file
	
}
