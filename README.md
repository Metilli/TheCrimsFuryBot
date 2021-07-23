# TheCrims Robbery Bot

TheCrims is browser crime game. In this game you can make some robberies. This script's goal is making robberies automatically.

## What does bot do?

- Automatically doing robbery.
- Filling stamina in your night club.
- Making detox when your addiction is between 20%-50%(Randomly selecting between 20%-50%).
- If there is an error at robbery automatically do failed robberies again.

## Bot Features

- User can select robbery.
- User can select how many robbery will be done.
- User can decide delays at clicking actions.
- Clicking positions selecting randomly depending on element size.
- Automatically send mail when all the robberies done.
- User can stop bot with "ctrl+c" keys on python shell or cmd screen.

# Installing

## Prerequisites

What things you need to install the software

- pip
- python 3.8
- pynput
- selenium

First install selenium
```
pip install selenium
```

Second install pynput
```
pip install pynput
```

## Configuring

Open config.txt and you will find:
```
"username": "",
"password": "", 
"emailAddress": "",
"emailPassword": "",
"robberyPageMin": 2,
"robberyPageMax": 2.5,
"robMin": 0.60,
"robMax": 1,
"nightClubMin": 0.6,
"nightClubMax": 1.5,
"enterClubMin": 0.5,
"enterClubMax": 1.3,
"buyMin": 0.1,
"buyMax": 0.25,
"exitMin": 0.1,
"exitMax": 0.25,
"hospitalMin": 1,
"hospitalMax": 1.75,
"detoxMin": 1,
"detoxMax": 2.4
```
- username: Put your username here
- password: Put your password here
- emailAddress: Put your email address here (it's optional)
- emailPassword: Put your email password here (it's optional)
- All of the other variables are delay times. Script does delays random between min and max values.

#### IMPORTANT

Buy a nightclub from buildings > bussiness that you can join and has at least 1 drug or 1 hooker available

# Running

1. Python shell or cmd will ask you "Do you select robbery?". In this step you have to select which robbery you want to do. After that you have can select use all stamina checkbox (Optional). After that you can hit Enter.
2. Python shell or cmd will ask you "How many tickets do you want to use?". In this step you have to enter ticket count. It has to be integer.
3. Bot will give you some reports while running.
4. After all of the tickets have been used, Python shell or cmd will ask you "Do you want to continue?". If you type "y" and enter bot will run again, otherwise bot will exit.

# Authors

Emre Metilli
