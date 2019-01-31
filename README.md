# PyHomeNotifications

This project is a work in progress.

Currently the google home can only speak if triggered by the key words "Ok Google" or "Hey Google". This means that the home can't speak notifications. Luckily, the google home also supports the chromecastAPI meaning you can cast music to the speaker to play.

This python script utulizes the Google TTS api to convert messages to an mp3 file of the google home voice. These mp3 files are then casted to the google home. This can mean full notification support if used alongside a service like IFTTT.

The idea is to have this script constantly running on a raspberryPi. Messages can be sent to an HTTP server on the pi.
