README:


Note: Additional image and music folders will be submitted via Google drive, and they need to be placed in the same directory as these files at runtime. :)


Game Description:
The name of this project is Interstellar, which is an airplane battle game. The project is mainly to establish an online game with the background of aircraft air combat. There are two kinds of play modes, one player mode and two players mode, with different difficulty levels. In the two players mode, two players can play the same game round connected by server. Players can choose the difficulty level recommended by the game based on their play history or by themselves. In the game, players use the keyboard operation to realize the movement and achieve different skill functions to destroy the enemy aircraft. The enemy aircraft are different airplanes with different health volume, speed and flight route, which can also speed up. The game has a boss character with different shooting capabilities and meteorites that rotate constantly. In the game, players needs to avoid the enemy's bullets and impacts, destroy the boss, and receive higher points to get a higher ranking on the leaderboard. 


How to run the Project:

The project folder has image folder, music folder, score folder, client.py, network.py, server.py, Readme.txt. They should be placed in the same folder.

1. How to run the one player mode:
In one player mode, you only need to run client.py to open the game. After watching the animation at the beginning of the game, you can choose Enter name button, and then the system will recommend the difficulty level for you, you can also adjust according to this level. Finally, you can enter the game by clicking the one player button.

2. How to open the two players mode: 
(1) First run the server.py file, server.py will prompt you if the server was successfully created;
(2) Open two client.py files through the terminal.;
(3) Select the 2 players mode in two client.py files seperately;
(4) After starting a 2 players mode in one file, the game will automatically wait for another player to join. 
(5) The first one to enter the game defaults to player No. 1 and controls the blue plane; the second one to enter the game controls player No. 2 and controls the rose red plane.

3. When the game is over, the game will remind you if you want to record your current game results. You can check if you are in the top ten of the overall leaderboard by clicking the Ranking Button.

4.
Player No. 1 operation keys:
UP: move forward; 
DOWN: move backward; 
LEFT: move left; 
RIGHT: move right;
SPACE: shooting; 
z: shield; 
x: space jump; 
c: rocket.

Player No. 2 operation keys:
w: moveforward; 
s: move backward; 
a: move left; 
d: move right;
n: shooting; 
j: shield; 
k: space jump; 
l: rocket.

t: pause, and show the help interface;
ESC: quit the current game round.


Which libraries you're using that need to be installed:
Pygame, socket.


A list of any shortcut commands that exist:
When you don't move, you will end this round of the game quickly, because the enemy's bullet will automatically fly towards your airplane.


Hope you like my project.  :)