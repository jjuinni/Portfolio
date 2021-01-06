/*
 * File: FacePamphletCanvas.java
 * -----------------------------
 * This class represents the canvas on which the profiles in the social
 * network are displayed.  NOTE: This class does NOT need to update the
 * display when the window is resized.
 */


import acm.graphics.*;
import java.awt.*;
import java.util.*;

public class FacePamphletCanvas extends GCanvas 
					implements FacePamphletConstants {
	/** 
	 * Constructor
	 * This method takes care of any initialization needed for 
	 * the display
	 */
	public FacePamphletCanvas() {
		bottom_msg = new GLabel(EMPTY_LABEL_TEXT);
	}
	
	/** 
	 * This method displays a message string near the bottom of the 
	 * canvas.  Every time this method is called, the previously 
	 * displayed message (if any) is replaced by the new message text 
	 * passed in.
	 */
	public void showMessage(String msg) {
		remove(bottom_msg);
		bottom_msg = new GLabel(msg);
		double x = (getWidth() - bottom_msg.getWidth())/2;
		double y = getHeight() - BOTTOM_MESSAGE_MARGIN;
		bottom_msg.setLocation(x, y);
		bottom_msg.setFont(MESSAGE_FONT);
		add(bottom_msg);
	}
	
	/** 
	 * This method displays the given profile on the canvas.  The 
	 * canvas is first cleared of all existing items (including 
	 * messages displayed near the bottom of the screen) and then the 
	 * given profile is displayed.  The profile display includes the 
	 * name of the user from the profile, the corresponding image 
	 * (or an indication that an image does not exist), the status of
	 * the user, and a list of the user's friends in the social network.
	 */
	public void displayProfile(FacePamphletProfile profile) {
		removeAll();
		addName(profile.getName());
		addImage(profile.getImage());
		addStatus(profile.getStatus());
		addFriends(profile.getFriends());
	}
		
	/**
	 * Helper code: add profile name to canvas 
	 * @param str: name to be added
	 */
	private void addName(String str) {
		double x = LEFT_MARGIN;
		double y = TOP_MARGIN;
		GLabel name = new GLabel(str);
		name.setFont(PROFILE_NAME_FONT);
		name.setColor(Color.BLUE);
		add(name, x, y);
	}
		
	/**
	 * Helper code:add profile image to canvas
	 * @param image: image to be added
	 */
	private void addImage(GImage image) {
		double x = LEFT_MARGIN;
		double y = TOP_MARGIN + IMAGE_MARGIN ;
		GRect imagebox = new GRect(IMAGE_WIDTH, IMAGE_HEIGHT); 
		add(imagebox, x, y);
		if(image == null) {
			GLabel noimage = new GLabel("No image");
			double noimage_x = x + IMAGE_WIDTH/2 - noimage.getWidth();
			double noimage_y = y + IMAGE_HEIGHT/2;
			noimage.setFont(PROFILE_IMAGE_FONT);
			add(noimage, noimage_x, noimage_y);
		}else {
			image.setBounds(x, y, IMAGE_WIDTH, IMAGE_HEIGHT);
			add(image);
		}
	}
		
	/**
	 * Helper code: add status related to profile 
	 * @param str: status to be added
	 */
	private void addStatus(String str) {
		double x = LEFT_MARGIN;
		double y = TOP_MARGIN + IMAGE_MARGIN + IMAGE_HEIGHT + STATUS_MARGIN;
		GLabel status = new GLabel(str);
		status.setFont(PROFILE_STATUS_FONT);
		add(status, x, y);
	}
		
	/**
	 * Helper code: add friend to profile and also update on the related friend's profile too
	 * @param it: iterator
	 */
	private void addFriends(Iterator<String> it) {
		double x = getWidth()/2;
		double y = TOP_MARGIN;
		GLabel friendlist = new GLabel("Friends:");
		friendlist.setFont(PROFILE_FRIEND_LABEL_FONT);
		add(friendlist, x, y);
		
		for(int i=1; it.hasNext(); i++) {
			String friendname = it.next();
			GLabel friend = new GLabel(friendname);
			add(friend, x, y + friendlist.getHeight()*i);
		}
	}

	/*Private instance variables*/
	private GLabel bottom_msg;
}
