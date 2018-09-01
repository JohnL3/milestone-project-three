# All about Testing both automated and manual will be covered in this file.

I will discuss automated tests first for which the test file can be found at ['Test_functions.py'](./tests/test_functions.py)

This uses unittest which was imported and sys ... which i needed for sys.path.append('..') so i could access my functions

I created 8 functions that I needed to test to be sure they did what was expected of them. I used an approach where i tried
to write function and test it as I created the function.

To run the tests you would use bash in cloud9 ... first you would need to move to the folder, this would be done by typing cd tests

To run the tests you would type python3 -m unittest

## Manual Testing

I will start with how website should look on various screens


On desktop index page should be opened full size with a panel on the left containing navagation (leaderboard), and right section containing
text. For game page it will have panel on left containing navagation (leaderboard home), welcome section with username, mini leaderboard
display and a online users display, and right section game panel. For leaderboard page it will have panel on left with navigation(game pange, home)
and right section leaderboard.

If destop browser is reszied down at small screen size left panel should collapse to the left leaving a small vertical section showing
with a hamburger icon which when clicked slides panel in and if clicked again slides panel out. If rezied to full screen with side panel in
collasped mode it should reset panel to full width.

In tablet on landscape view you should get the same screen as on destop full left panel with section on right, in portrait you should
get the collasped left panel view.

on mobiles you should get the collasped view with hamburger but also if mobile is looked at in landscape screen should rotate. 

This is done using an orientation landscape media query, which will need more work as I am not used to doing something like this, and
it is the first time I have attempted it. So I have a feeling it may not look right on all the various mobile screen sizes out there.



### Starting with the index.html page (landing page)

1. On landing page there are two parts to test first there is a link to the leaderboard page.
  * I clicked this link and it brings me to the leaderboard page: True
2. On landing page there is a input for getting your username and it has a 12 characther limit
  * I can only create a username with max 12 characthers: True
  * I cannot submit an empty input value: True
3. When i click the button it shuould submit my username and direct me to the game page: True
4. When I return to the landing page my username should be in the input box saving me having to remember it even if i have closed down
website and returned later: True
5. As a person who hasnt created a username yet i can visit leaderboard page: True


### Game page testing
1. I should not be able to click anything while information screen is open only the close button: True
2. I should be able to close information screen via clicking a button: True
3. I should be able to navigate to the home page via a link: True
4. I should be able to navigate to the leaderboard page via a link: True
5. I should be able to do this without a promt appearing: True
6. If I tab back or try to close tab after information screen closes I should get a promt asking if I want to do this: True

Note on this, as I am using socketIo for showing when users are online and when they leave and there scores. soketIo requires some
sort of interaction before it works for tab back and tab closing.

This was one problem I encountered, while removing users from online list when they clicked the home or leaderboard link is quite easy,
if they tabbed back or closed tab I would be left with there name in the user list. To overcome this problem i used an onbeforeunload
function in javascript which prompts them to check if they are sure the wish to leave, giving socketIo the opportunity to remove them
from the user list plus clearing game board and details section should they decide not to. Cant have them stay and play after clearing
there user name from list but also not allowed redirect them to another page.

This is also why i have an instructions section when game page loads as socketIo requires some interaction before it works for tab backs
and closing tabs. By clicking the close button at the start when they arrive on game page im able to get socketIo to fire if they then
tab back or close tab.

7. I should see my name in welcome section: True
8. I should see my name in online user section: True
9. I should see usernames of others in online user section if they are on game page: True
10. If another user who is on the game page leaves I should see there name removed: True
11. If I or another player answers a question correctly i should see mine or others score update: True
12. If I leave game and my score is in the top 3 it should appear in mini leaderboard: true
  * I would have to come back to game page to see this: True
13. If another user scores and leaves game page and there score is in the top 3 I should see there name appear in the mini leaderboard: True

Note: A little word on how socketIo works
socketIo works by emmiting events from both server and from the client. When a user visits the game page the online user
section is handled by flask jinja templateing but socketIo emits to other pages that have being opened by other users an updated list
of users online and other pages receive this message and javascript updates the online user section.

when a user leaves a page socketIo emits from the client side the name of the user that has left, server recieves this works out whos
online and emits a new list to all game pages that are opened and javascript picks up on this and displays the updated list.

This is similiar to what happens when a user gets a question right and there score changes, the server emits the updated score and
on the client side this message is recieved and score updated in the display.

And again for the mini leaderboard and leaderboard page socketIo is emmiting when things change.

With regards to checking that this works the way I entended, I checked this by opening two browsers in chrome one in incognito mode.
I created two users and went to game page and i would observe the second players username appear in user list when they
joined the game page. I would observe the users name disappear from the user list when they left the game page. I would observe the 
scores change when they answered a question correctly and observe the mini leaderboard change when they left the game page and there
score was high enough to get on the mini leaderboard, I alos went to the leaderboard and observed that this would also update when they
left or finished the game.

14. I should get a question to answer when I click on a panel: True
15. I should get a pop up screen with either check boxes to click or an input to fill in: True
16. I should not be able to submit a question with no answers: True
17. If I attempt to submit a question without answering it, it should not submit and a warning modal should appear stating this: True
18. This modal should disappear after 3 seconds: True
19. If I get a question correct the border of the panel clicked to get the question should turn green: True
20. If I get a question correct the score should update in the display section: True
21. If I get a question wrong the border of the panel clicked to get the questition should turn red: True
22. If I leave the game before all questions have being answered my score is added to leaderboard in apporpriate position and to the mini
leaderboard if high enough: True
24. I can appear on both mini and full leaderboard more than once but only when my scores are different: True


Note: This is one area I would like to improve ... at present if two people score the same eg both get all questions right I would
like both to be given a rank of 1 but as it stands its not a rank they actually get but a index position so one will be 1 other will be 2


25. When I answer last question I will get a congratulations screen informing me I have finished the game and my final score: True
26. When a question is answered either correctly or incorrectly clicking on a panel will no longer call a question: True
27. When I leave the game page my score should be reset to 0 and I have to start game again: True


### Leaderboard page testing

1. I should be able to navigate to the home page by clicking a link: True
2. I should be able to navigate to the game page if I have a username and click a link: True
3. I should be redirected to home page if I click game link and I dont have a username: True
4. I should see my username and score on the Leaderboard if I have answered a question correctly: True
5. If I have more than one attempts with different scores I should see these on leaderboard: True
6. I should see usernames and scores of other players who have answered questions correctly: True







