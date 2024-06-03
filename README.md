# PRODUCTIVITY WEB APP
#### Video Demo :  <https://youtu.be/FrOClMU7O2s>
## Description :
Welcome to my project ! As part of the course "CS50's Introduction to Computer Science", I created this web app that allows the user to create an account and navigate through three inside-app : To-do, Notes and Planning.

## What's inside the folder ?
1. "static" : is a folder in which you will find my CSS file
2. "templates" : is the folder that contains every page of the website
3. "app.py" : is the python file that contains all of the logic behind the website using Flask
4. "helpers.py" : is the python file that contains a library of functions used in app.py
5. "database.db" : is the database used in my project
6. "requirements.txt"
7. "tailwind.config.js"
8. "README.md"

## Features :
1. Main Menu
    - create an account
    - login
2. Manage your account
3. To-do
    - Lists
    - Tasks
    - Menu "Completed Tasks"
4. Notes
5. Planning

### 1. Main menu
When you launches the website, you can either create a new account or log in the account you already created.
#### a. Create an account
To create an account, you must click on the "Sign in" Button. Then, you will have to provide several informations such as : First and Last name, Username, Email Adress and Password (with confirmation) for your registering to be accepted. You will also have to accept the terms and conditions. From this page, you can also choose to be redirected to the login page.
The program checks if the information you provided are correct and if you missed giving one.
#### b. Log in
To log in your account, you will have to provide your username and password, and if the informations are correct, you will be redirected to your account. From this page, you can also choose to be redirected to the "Sign in" Page.
### 2. Manage your account
Once you are logged in, you can access to the page "My account" from the menu at the top right (where you can also log out). In this page you will find your account's informations (First and Last name, username and email adress) from where you can choose to edit some of those. You can either edit an information or edit your password and when you valid your modification, the program updates the database with the new informations you provided.
### 3. To-do
From the main menu of the app, you can choose the option "To-do" to enter the To-do application. In the main menu of this app you have two options : if you already created lists, they will appear in a table in the main menu, but if it's your first time on the app and you never have created a list, a welcome message will be displayed, to guide you and help you use the app.
#### a. Lists
First of all, you will have to create a list which will contains different tasks in the future. To do so, you can use the menu at the bottom right and select "Create a list". The app will ask you to provide a name for your list and a first task to create it. The program will then check that you entered all the informations required and update the database with your list. Once it's created, it will then appear in the To-do's main menu. In the tab, you will be able to either edit the name of your task  or delete it. When you click on the name of the list, you then have access to all the details of the list and every task that are in it.
#### b. Tasks
Once you have created a list, you can then create a task. To do so, you can use the menu at the bottom right an select "Create a task". The app will ask you to provide the content of your task and it will ask you to choose the list in which you want it to be with a combo box. Then, once the program checked that the information are correct, your task will be created and seen in the list's menu. From there, you can either edit the content of your task, delete it, or mark it to be done. If you do so, it will disappear from the list and be moved to the "completed tasks" menu.
#### c. Completed tasks
Every tasks that you marked as "done" will appear in the third menu at the bottom right named "completed task". Here, in the same way as the other menus, you will see a table in which every tasks that has be done are written. For each of those, you will be able to know the content of the task, the list it was in, the date and time it was done and you will also be able to definitely delete the task. You will also find a button at the top of the menu where it is written "delete all my completed tasks" for you to empty this table.

### 4. Notes
From the main menu of the app, you can choose the option "Notes" to enter the Notes application. With the menu at the bottom right, you can select the option "Create a note". Then you will have to provide a title for your note, a content and a color (White, Yellow, Green, Blue and Pink). Once the program says that your informations are correct, your note is though created. In the main menu of your app, you will either see a welcome message if no notes were created or you will see your notes as post-it displayed in the menu if you already created one or more. For each note you have three option :
    - you can edit the note : a popup window appears and offers you to edit informations (title, content or color)
    - you can archive the note
    - you can maximize the note : meaning that the note will then appears in a new page where it appears alone. You will find the same infos but in another way.
For each note, you can also see the date of creation.
To see your archived note you can select the second option in the menu at the bottom right "Archived notes". From there, you can either get the note back or delete it.

### 5. Planning
From the main menu of the app, you can choose the option "Planning" to enter the Planning application. With the menu at the bottom right, you can select the option "Create an event". Then you will have to provide several informations : the title of your event, the category of your event(Personal, Professional, Appointment, Birthday, Other; and each category is associated to a color), a beggining and ending date, a beggining and ending times and the possibility or not to add details about your event. This last option is optional. Once the program validates your informations, your event will be created. From the main menu of this app you will then see all the notes you have created (otherwise you will see a welcome message). Each event will then be displayed such as the notes : in cards. If in the specificites of your event you entered the same begginning and ending date, the date on the outcome will appears only one time as a single-day event. It's the same for the time. At the top of the page you will have the possibility to only display a specific category or display them all depending on what you want. For each event, you can either edit the informations or delete the event. In the main menu, only the upcoming or current event will appear. To see all the event that happened before today's date, you will have to select the option "past event" with the menu at the bottom right. The page will appear exactly the same as the main page but only with the events that happenned in the past.

## Specificities :
The app adapts itself to different devices such as computer, tabs or phones. And it is also compatible with dark mode.

## Credit :
This program was created and coded with Visual Studio Code using Python. It was created thanks to Harvard's and EDX's online course : "CS50's Introduction to programming with Python"

## Note :
I apologize if there is any grammatical error inside this README file but as a french student, I do not speak a perfectly fluent english so I might risk to miss language errors.