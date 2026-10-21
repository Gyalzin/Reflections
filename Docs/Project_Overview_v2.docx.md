# **Project Overview**

## **1\. Project Name: Reflections**

Relaxed Daily Personal Activity Tracker

## **2\. Problem Statement**

As days turn into weeks and months, people can lose awareness of how they have spent their time and the experiences that have shaped their lives. Existing approaches to tracking activities and measuring progress can feel overly structured, analytical, or focused on productivity, making personal reflection feel like another task to complete.

The proposed application aims to provide a calm, inviting space where users can gently record their daily activities and reflections, revisit their experiences, and discover patterns in how they spend their time. Through a cozy and meditative experience, the application encourages self-awareness and appreciation of everyday life without the pressure of constant productivity or performance.

## **3\. Project Objectives**

### **Core Vision**

To create a cozy, reflective, and meditative personal activity tracker that helps people reconnect with their everyday lives.

The application allows users to gently record their activities and experiences, revisit their past days and months, and discover patterns in how they spend their time. Through a calm and non-judgmental experience, users can recognise what they have experienced, better understand themselves, and appreciate how they have spent their time, regardless of how productive they have been.

### **Design Philosophy**

1. Gentle, not demanding: Recording activities should feel effortless, not like completing daily administrative tasks.  
2. Reflective, not competitive: Present patterns and memories without streak pressure, leaderboards, or guilt.  
3. Meaningful, not data-heavy: Present activity history through calm timelines, visual summaries, and gentle insights rather than overwhelming users with statistics.

### **Objectives**

1. Encourage reflection: Make it easy for users to record their daily activities and experiences.  
2. Improve time awareness: Help users understand how they have spent their days by revisiting them on a calm timeline. Summaries over longer periods are planned for a future version.  
3. Preserve personal history: Allow users to revisit past activities, experiences, and memories.  
4. Reveal patterns: Help users notice changes in their routines, interests, and activities over time. The initial version supports this by letting users browse past days; summaries and insights are planned for a future version.  
5. Promote self-awareness without pressure: Present activity history in a cozy, non-judgmental way rather than focusing on productivity scores.

## **4\. Target Users**

People who want greater awareness of how they spend their time, remember their everyday experiences, and better understand their routines and interests.

The application is intended for users who prefer a flexible, reflective approach to activity tracking rather than a strict productivity-focused system.

## **5\. Project Scope**

This section defines the features and capabilities intended for the initial version of the application, as well as features that will be excluded or considered for future development.

### **Included in the Initial Version (MVP)**

The initial version will be a web application that allows users to record their daily activities on a flexible, calm timeline designed to encourage reflection and awareness of everyday life.

The application will include the following features:

1. Activity Logging: Users can create an activity block by selecting a position on the timeline, which sets its start time, and then entering an activity name. They can set an approximate start time and duration in the activity form (a default duration is used if none is entered), and optionally add a note and a mood chosen from a small set of options.

2. Timeline: Activities are displayed on a single, continuous 24-hour timeline. Each block’s position and length reflect its start time and duration, so users can see how their day unfolded.

3. Flexible Time Representation: The application uses underlying time values to position and size activity blocks, while the interface displays subtle background labels such as Midnight, Morning, Afternoon, Evening, and Night rather than prominent clock times.

4. Overlapping Activities: Users can record activities that occur simultaneously, such as cleaning while doing laundry. Overlapping activities are displayed side by side so that each one stays readable.

5. Activity Management: Users can edit and delete existing activity blocks (deleting asks for confirmation). Changes are saved automatically with a gentle confirmation message, and entries are checked for missing or invalid information before they are saved.

6. Historical Review: Users can move to the previous or next day, revisit past days to see the activities they recorded, and return to today’s timeline at any time.

7. Personal Reflection: Users can optionally record notes and a mood for their activities and revisit them later.

8. Quality: A calm, consistent interface; reliable storage in SQLite; a single-user application with no login, where data stays in the application’s own database; and support for the latest versions of Chrome and Firefox with basic keyboard accessibility.

The interface will prioritise simplicity, comfort, and flexibility. Users will be able to record their activities at their own pace without pressure to account for every minute or meet productivity targets.

**Planned for Future Versions:**

1. Interactive Timeline: Dragging activity blocks to a new time and resizing them to change their duration, including dragging blocks into overlapping positions.

2. Daily and Period Summaries: A summary of a single day and of a selected period, presented calmly and without productivity scores.

3. Extended History: Browsing activity history by week or month.

4. Insights: Showing which activities are recorded frequently, to help users recognise their interests and habits.

**Out of Scope:**

1. Reminders and notifications

2. User accounts and login (the initial version is single-user)

## **6\. Proposed Technology**

1. Programming language: Python  
2. Backend framework: Flask  
3. Frontend: HTML, CSS, and JavaScript (JavaScript handles the timeline interaction and automatic saving)  
4. Database: SQLite

## **7\. Success Criteria**

The project will be considered successful when:

1. Users can record, edit, and delete their activities.

2. Users can add personal reflections, including notes and a mood, to their activities.

3. Users can revisit their activity history by moving between days and returning to today.

4. All Must-have requirements for the initial version meet their acceptance criteria in the Requirement Analysis.

5. The interface provides a comfortable, intuitive, and non-judgmental experience, confirmed by feedback from a small group of test users (about 3–5 people).

6. The core features function reliably and the application stores and retrieves user data correctly, including after a page refresh, a browser restart, and a server restart.

Visual summaries, weekly and monthly views, and activity insights are planned for a future version and are not part of the success criteria for the initial version.

## **8\. Constraints**

1. Time: Development must be completed within the available project timeframe. Target completion date: January 15, 2027

2. Build order: (1) timeline basics with saving – create, edit, delete, start time and duration, time-of-day labels, and automatic saving; (2) day navigation and history; (3) notes, mood, save confirmation, and input validation; (4) styling, testing, and polish.

3. Budget: The project should primarily use free and open-source tools.

4. Technical limitations: The initial version will focus on a manageable set of features using Python, Flask, HTML/CSS, JavaScript, and SQLite.

5. Development resources: The scope must remain realistic for a solo developer.

6. Scope control: If time runs short, “Should have” and “Could have” requirements are deferred before any “Must have” requirement.

## **9\. Project Outcome**

The application aims to help users:

1. Become more aware of how they spend their time.  
2. Recognise and appreciate the activities and experiences that make up their lives.  
3. Understand their routines, interests, and changes over time.

   Ultimately, the application should help users feel that they have experienced more than they realised and encourage a greater appreciation of everyday life, without making productivity the measure of a meaningful day.

## **10\. Stakeholders**

Developer \- Designs, builds, tests and maintains the application.  
End Users \- Use the applications to record activities, reflect on their activities and revisit their history

## **11\. User Stories**

Each story is tagged \[MVP\] for the initial version or \[Future\] for a later version. Story numbers match the Story Ref column in the Requirement Analysis spreadsheet. Reminders are out of scope (see Section 5).

1\. As a user, I want to create an activity block directly on the timeline so that I can record my activities quickly and intuitively. **\[MVP\]**

2\. As a user, I want to give an activity block a name so that I can identify the activity I performed. **\[MVP\]**

3\. As a user, I want to update an existing activity block so that I can correct information or add details later. **\[MVP\]**

4\. As a user, I want to delete an activity block so that I can remove activities I entered incorrectly or no longer need. **\[MVP\]**

5\. As a user, I want to adjust the duration of an activity block so that I can represent approximately how long I spent on an activity. **\[Future\]**

6\. As a user, I want to drag an activity block along the timeline so that I can represent approximately when I performed an activity. **\[Future\]**

7\. As a user, I want activity blocks to overlap so that I can represent activities that happened simultaneously. **\[MVP: overlapping activities are shown side by side. Future: creating overlaps by dragging and resizing.\]**

8\. As a user, I want to see subtle time-of-day labels on the timeline so that I can orient my activities throughout the day. **\[MVP\]**

9\. As a user, I want to add an optional note to an activity so that I can record important details or memories about it. **\[MVP\]**

10\. As a user, I want to record my mood or feelings about an activity so that I can reflect on how the experience made me feel. **\[MVP\]**

11\. As a user, I want to view my past activities so that I can remember what I did on previous days. **\[MVP\]**

12\. As a user, I want to view summaries of my activities over a selected period so that I can understand how I have spent my days and weeks. **\[Future\]**

13\. As a user, I want to return to today’s timeline so that I can quickly access my current day’s activities. **\[MVP\]**

14\. As a user, I want my activities to be saved automatically so that I don’t lose my records when I leave the page. **\[MVP\]**

15\. As a user, I want to see my activities positioned on the timeline in the order they happened so that I can understand how my day unfolded. **\[MVP\]**

16\. As a user, I want to view a summary of my activities for a specific day so that I can reflect on how I spent that day. **\[Future\]**

17\. As a user, I want to view my activity history over weeks or months so that I can remember past experiences and notice changes in my routines. **\[Future\]**

18\. As a user, I want to see which activities I do frequently so that I can better understand my interests and habits. **\[Future\]**

19\. As a user, I want to use the application without having to record every minute of my day so that activity tracking remains flexible and pressure-free. **\[MVP\]**

20\. As a user, I want the application to present my activity history in a calm and visually appealing way so that reflecting on my experiences feels enjoyable. **\[MVP\]**

21\. As a user, I want to leave an activity’s notes or mood unspecified so that I can record an activity without filling in unnecessary details. **\[MVP\]**

22\. As a user, I want to set and later correct when an activity started and how long it lasted so that I can adjust my timeline as I remember more about my day. **\[MVP\]**

23\. As a user, I want to see a helpful indication when an activity has been saved so that I know my record has been stored successfully. **\[MVP\]**

24\. As a user, I want the system to validate the information I enter so that I can correct invalid information before saving an activity. **\[MVP\]**

