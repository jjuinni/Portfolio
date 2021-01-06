import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.*;

import acm.util.ErrorException;

/*
 * File: NameSurferDataBase.java
 * -----------------------------
 * This class keeps track of the complete database of names.
 * The constructor reads in the database from a file, and
 * the only public method makes it possible to look up a
 * name and get back the corresponding NameSurferEntry.
 * Names are matched independent of case, so that "Eric"
 * and "ERIC" are the same names.
 */

public class NameSurferDataBase implements NameSurferConstants {
	
/* Constructor: NameSurferDataBase(filename) */
/**
 * Creates a new NameSurferDataBase and initializes it using the
 * data in the specified file.  The constructor throws an error
 * exception if the requested file does not exist or if an error
 * occurs as the file is being read.
 */
	public NameSurferDataBase(String filename) {
		try {
			BufferedReader in = new BufferedReader(new FileReader(filename));
			while(true) {
				String line = in.readLine();
				if(line==null)break;
				NameSurferEntry entry = new NameSurferEntry(line);
				dataBase.put(entry.getName(), entry);
			}
			in.close();
        } catch (IOException e) {
            throw new ErrorException(e);
        }
	}
	
/* Method: findEntry(name) */
/**
 * Returns the NameSurferEntry associated with this name, if one
 * exists.  If the name does not appear in the database, this
 * method returns null.
 */
	public NameSurferEntry findEntry(String name) {
		char ch1 = name.charAt(0);
		if(Character.isLowerCase(ch1)) {
			ch1 = Character.toUpperCase(ch1);
		}
		name = ch1 + name.substring(1).toLowerCase(); 
		if(dataBase.containsKey(name)) {
			return dataBase.get(name);
		} else { return null; }
	}
	
	/*Private Instance Variables*/
	private Map <String, NameSurferEntry> dataBase = new HashMap <String, NameSurferEntry>();
}

