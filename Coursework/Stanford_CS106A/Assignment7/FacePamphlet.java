/* 
 * File: FacePamphlet.java
 * -----------------------
 * When it is finished, this program will implement a basic social network
 * management system.
 */

import acm.program.*;
import acm.graphics.*;
import acm.util.*;
import java.awt.event.*;
import java.util.Iterator;

import javax.swing.*;

public class FacePamphlet extends Program implements FacePamphletConstants {

	/**
	 * This method has the responsibility for initializing the 
	 * interactors in the application, and taking care of any other 
	 * initialization that needs to be performed.
	 */
	public void init() {
		activeProfile = null;
		database = new FacePamphletDatabase();
		canvas  = new FacePamphletCanvas();
		add(canvas);
		leftInteractors();
		upperInteractors();
		addActionListeners();
    }
    
	
	/**Create and add east side interactors.
	 * interactors addes are: status change, 
	 * 						  picture change 
	 * 					      and adding friend
	 * */
	private void leftInteractors() {
		status = new JButton("Change Status");
		picture = new JButton("Change Picture");
		friend = new JButton("Add Friend");
		statusField  = new JTextField(TEXT_FIELD_SIZE);
		statusField.addActionListener(this);
		pictureField = new JTextField(TEXT_FIELD_SIZE);
		pictureField.addActionListener(this);
		friendField = new JTextField(TEXT_FIELD_SIZE);
		friendField.addActionListener(this);
		
		add(statusField, WEST);
		add(status, WEST);
		add(pictureField, WEST);
		add(picture, WEST);
		add(friendField, WEST);
		add(friend, WEST);
	}
	
	/**Create and add north side interactors.
	 * interactors addes are: add, 
	 * 						  delete 
	 * 					      and look up
	 * */
	private void upperInteractors() {
		add = new JButton("Add");
		delete = new JButton("Delete");
		lookup = new JButton("Look Up");
		nameField = new JTextField(TEXT_FIELD_SIZE);
		nameField.addActionListener(this);
		
		add(new JLabel("Name"), NORTH);
		add(nameField, NORTH);
		add(add, NORTH);
		add(delete, NORTH);
		add(lookup, NORTH);
	}
  
    /**
     * This class is responsible for detecting when the buttons are
     * clicked or interactors are used, so you will have to add code
     * to respond to these actions.
     */
    public void actionPerformed(ActionEvent e) {
		Object source =  e.getSource();
		String entry;
		if(source == status || source == statusField) {
			entry = statusField.getText();
			if(entry != null) {
				if(activeProfile != null) {
					activeProfile.setStatus(entry);
					canvas.displayProfile(activeProfile);
					canvas.showMessage("Status updated to" + entry);
				}else {
					canvas.showMessage("Select a profile to change status of.");
				}
			}
		}
		else if(source == picture || source == pictureField) {
			entry = pictureField.getText();
			if(entry != null) {
				if(activeProfile != null) {
					GImage image = null;
					try {
						image = new GImage(entry);
						activeProfile.setImage(image);
					} catch (ErrorException ex) {
						image = null;
					}
					canvas.displayProfile(activeProfile);
					if(image != null) {
						canvas.showMessage("Image updated.");
					}else {
						canvas.showMessage("Unable to open image file.");
					}
				}else {
					canvas.showMessage("Select a profile to change image of.");
				}
			}
		}
		else if(source == friend || source == friendField) {
			entry = friendField.getText();
			if(entry != null) {
				if(activeProfile != null  && database.containsProfile(entry)) {
					boolean flag = activeProfile.addFriend(entry);
					if(!flag) { 
						canvas.showMessage("Already friends with " + entry);
					}else { 
						FacePamphletProfile subProfile = database.getProfile(entry);
						subProfile.addFriend(activeProfile.getName());
						canvas.displayProfile(activeProfile);
						canvas.showMessage("Add Friend: " + entry);
					}		
				}else {
					canvas.showMessage(entry + " not in social network.");
				}
			}		
		}
		else if(source == add) {
			entry = nameField.getText();
			if(entry != null) {
				if(database.containsProfile(entry)) {
					FacePamphletProfile profile = database.getProfile(entry);
					canvas.displayProfile(profile);
					canvas.showMessage("Profile with name " + entry + " already exists.");
					activeProfile = profile;
				}else {
					FacePamphletProfile profile = new FacePamphletProfile(entry);
					database.addProfile(profile);
					canvas.displayProfile(profile);
					canvas.showMessage("New profile added.");
					activeProfile = profile;
				}
			}
		}
		else if(source == delete) {
			entry = nameField.getText();
			if(entry != null) {
				if(database.containsProfile(entry)) {			
					database.deleteProfile(entry);
					canvas.showMessage("Profile of " + entry + " deleted.");
					canvas.removeAll();
				}else {
					canvas.showMessage("A profile with name " + entry + " does not exist.");
				}
			}
		}
		else if(source == lookup) {
			entry = nameField.getText();
			if(entry != null) {
				if(database.containsProfile(entry)) {
					FacePamphletProfile profile = database.getProfile(entry);
					canvas.displayProfile(profile);
					canvas.showMessage("Displaying " + entry);
					activeProfile = profile;
				}else {
					activeProfile = null;
					canvas.showMessage("A profile with name " + entry + " does not exist.");
				}
			}
		}
	}
    
    /*Private instance variables*/
    private FacePamphletCanvas canvas;
    private FacePamphletDatabase database;
    private FacePamphletProfile activeProfile;
    
    private JButton status;
    private JButton picture;
    private JButton friend;
    private JButton add;
    private JButton delete;
    private JButton lookup;
    
    private JTextField statusField;
    private JTextField pictureField;
    private JTextField friendField;
    private JTextField nameField;
}
