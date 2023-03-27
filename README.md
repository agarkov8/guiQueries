# guiQueries
Implementation of a GUI reporting tool for evaluating employee authorizations

# guiQueries
Implementation of a GUI reporting tool for evaluating employee authorizations

The entries can then be confirmed with "Enter" or also by mouse click on the login button (See photo)!

 ![image009](https://user-images.githubusercontent.com/55351778/227943320-c7beb99f-f7b4-48ee-960e-f1c94cd4d36c.png)

Now the window should close and a new window should open -> Talias queries:
There you can enter the desired ID of the role in the field behind "Please enter role ID:" (See photo):
IMPORTANT:
Even if the ID does not exist, a (then empty) file will be created!
After the role has been entered, click with the left mouse button on the search button (See photo):
 
 ![image002](https://user-images.githubusercontent.com/55351778/227943633-8b9c6b72-9fba-42a7-b9b8-4e0346d31eef.png)

 
The following message appears:
 
 ![image001](https://user-images.githubusercontent.com/55351778/227943689-2bdad901-56f7-415d-8c03-242a9341443b.png)
 
  
There is now a .csv file named " MemberTaliasRole-(entered RoleID).csv in the mentioned folder.

 ![image010](https://user-images.githubusercontent.com/55351778/227943757-54862cc0-ba0e-49da-a536-4a6f1e1be24b.png)
 
 
If a role ID is searched, which already exists, the old file is overwritten by a new current file!
 
Structure of the file

![image003](https://user-images.githubusercontent.com/55351778/227943846-06df2372-5507-4fc6-8b80-0cbcaa634715.png)
 
1. Talias's role ID that was searched for (identical in all lines).
2. Last name of the user
3. First name of the user
4. Personnel number (important: add 0 in the first place where there are only 5 digits)
5. E-mail address of the user
6. Status of the user
  1 -> User is authorized to the role
  2 -> User is owner of the role

