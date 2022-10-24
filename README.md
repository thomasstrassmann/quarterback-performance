# Quarterback performance app
## A python command-line application for American Football lovers


![](./assets "")

[Click here for the full website access](https://quarterback-performance.herokuapp.com/)



## Table of contents
1. [Introduction](#introduction) 
2. [Preparation - UX and UXD](#preparation)
3. [Features](#features)
4. [Testing](#testing)
5. [Deployment](#deployment) 
6. [Credits / attributes](#credits) 



## Introduction 
The Quarterback Performance app (or for further purposes: "QPA" ), is a tool for passionate american football fans to measure the performance of quarterbacks. It is designed to solve the following problem: In isolation, statistics from football games are not meaningful and can therefore give a distorted picture of reality. Furthermore, the QPA should disprove or support the subjective perception of a player's performance by numbers. 

## Preparation - UX and UXD

The Python app is aimed at all football fans who also love statistics. In American sports, statistics are treated very differently than, for example, soccer in Europe and therefore have a much higher value. It may sound like a bold, exaggerated statement but: Football fans who don't like statistics don't exist. This also explains the hype surrounding so-called fantasy leagues, in which players can put together their own team. 

In terms of user experience, it is definitely more difficult to design an attractive interface or the like for a pure command-line tool, since the resources for this are not available. Nevertheless, it makes sense to deal with this topic, since there is also an input and output in the terminal. 
It is important with the inputs that it is clearly communicated which values or data types are expected and if these do not meet the requirements, the user also receives direct feedback with a note. 

The output should of course also be easy to understand and quickly accessible to the user through a structured listing of the relevant information. 

The **UXD - User Experience Design** was declared and described in advance and includes the 3 panels strategy, scope & structure. Skeleton and Surface are omitted because wireframes, layouts, color palettes, typographies etc. are not found in the command-line. 

### Strategy 
An application about a sport, in connection with statistics is (culturally) appropriate, almost goes without saying and not for nothing there is the expression: "Football is Family".

Internet sites on statistics are a dime a dozen. So what makes the QPA special? First of all, it encourages users to collect the statistics of a match day themselves and to deal with them. Similar to a scrapbook with stickers. By specifying its own statistics, this app is also highly customized, which makes it different from complete rankings of a league. The user can therefore create his own leaderboard with his favorite players. 

In addition, the generation of information is very exciting, which is almost unavailable anywhere else, because: A quarterback's averages are not only compared to those of other quarterbacks, creating a leaderboard, but they are also compared to the default quarterback position from the previous year (i.e., averages). Thus, the user has a means of comparison that goes beyond traditional statistic rankings. 

To manage and use the data, google sheets is used as the "data store". Users with access rights can read this data store, but not edit it, in order to keep the application intact. It should be avoided that unintentionally columns or rows are swapped with each other or values are deleted, which are necessary for a smooth process. 

---
### Scope 
What is feasible? 

In terms of requirements and functional specifications, a command-line tool is also certainly to be planned differently than an app with a real frontend.  The following points are included in the app as features: 

* The user can enter the eight most important statistics into the terminal himself. These are: Last name of the quarterback, game day, passes completed, passes thrown, yards thrown, touchdowns, interceptions, sacks.
* After entering the data, the user receives a detailed list of how much a quarterback deviates from the standard values of a quarterback from last year. 
* Based on the deviations, a rating algorithm will give the player an American grade in letters, where the grade "C" corresponds to the values of the average player. 
* In addition, the values of the respective quarterback are compared with those of other entered values to create an own NFL Leaderboard.
* The data is stored in Google Sheets. Once the user has entered all the data that is important to him, he can return next week to continue exactly where he left off. This makes the application more interesting as it shows the changes over the season. 
* From this point of view, the user also decides for himself which data he wants to collect and which players appear in his leaderboard. 


What is not feasible? 

It is definitely to avoid that the user has to enter too many statistics by himself. Eight may be a lot for outsiders at first glance, but these are really the most important ones. Theoretically, you could enter more than 30 statistics, but no one would bother. Therefore, the query is based on the minimum number of required information. 

For time reasons, no more than two outputs are aimed at, namely the comparison to the standard of the last season and to other players. 


--- 
### Structure 
The navigation is self-explanatory due to the input details. 
The organization of functionality and content is best described with a flow diagram.
![Function flow](./ "Function flow")



As already mentioned, Skeleton and Surface are not required. However, something can be summarized to the division and the representation also in the command-line: 
* All input fields and error messages are clearly formulated.
* The data must be listed cleanly one below the other.
* Line breaks, hashtags or other characters can be used for visual delimitation.
* An orderd list can be used to display the leaderboard. 



## Features
The following features were a decisive factor during the creation and they should help the Python app compile useful data.
* 
![](./assets "")


### Features for the future 
The following features would be ideas for further development...
* 
* 
* 



## Testing 



## Deployment 



[You can access the website right here](https:/)


## Credits
