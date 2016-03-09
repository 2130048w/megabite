# Zombie: A Search Game

The purpose of this web application is to provide the frontend interface for a game of search and survival. The web application needs to interface with a series of classes that create the world in which the player needs to survive. 

The game is as follows:

  - A player starts on day one of the zombie apocalypse. Their goal is to survive as long as possible (i.e. number of days).
  - Their party size is 1. They have 3 units of food and 2 units of ammunition.
  - They enter a street. A street contains a number of houses. Each house has a number of rooms.
  - A room may contain other survivors, zombies, food and/or ammunition.
  - The player has a number of moves available to them, depending on where they are..

On the street:
  1. a player can chooses which house to move to
  2. a player can enter the house they are in front of

In a house:
  1. enter room
  2. move to next room
  3. leave house

In a room:
  1. search room
  2. leave room
  3. if zombies are present, they have to either fight or run. 
    a.	if they run, they leave the house and return to the street (but may lose some people)
    b.	if they fight, they might lose the fight (lose party members, kill zombies, etc), win, in which case they claim whatever is in the room (survivors, food, ammo), or if after the fight zombies still remain, they have to fight or run again, etc.

The game mechanic for win/loss is based on the number of zombies, the amount of ammo and the size of the party.

During a day, the player has X units of time. Each action costs time. The day ends when they run out of time. At the end of the day, the game mechanic, decreases the amount of food depending on the size of the party. If there is not enough food, then party members might leave. Party size and food is updated, then they start the next day. The *game* object handles this, but it can be configured.



## Code
In the *engine* folder is a set of classes that provide the game mechanic for the Zombie search game.

To run, install the packages in the *requirements.txt* and then run:

```
  python main.py
```

Follow the instructions to play the game. 

The interface is crude and text based - but in *main.py* you can see how to instantiate the game object and what methods you need to call. Note the game loop is composed of two parts, checking if game is over, and then checking if the day or game is over.
