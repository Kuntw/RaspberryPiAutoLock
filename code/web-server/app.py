import RPi.GPIO as GPIO

from flask import Flask, render_template, request, redirect, url_for
from time import sleep

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

cont = 'y'
blinktime = 0.1

pins = {
    17: {'name': 'GPIO 17', 'state': GPIO.LOW}
}

# Set each pin as an output and make it low
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary
    templateData = {
        'pins': pins
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer
    changePin = int(changePin)
    # Get the device name for the pin being changed
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on", execute the code indented below
    if action == "on":
        # Set the pin high
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    if action == "trigger":
        # Set the pin high
        GPIO.output(changePin, GPIO.HIGH)
        sleep(blinktime)
        GPIO.output(changePin, GPIO.LOW)
        message = "Triggered " + deviceName
    
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    templateData = {
        'pins': pins
    }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
