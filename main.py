from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

pins = (15, 16, 18)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins, GPIO.OUT)
GPIO.output(pins, GPIO.LOW)

p_B = GPIO.PWM(pins[0], 2000)
p_R = GPIO.PWM(pins[1], 2000)
p_G = GPIO.PWM(pins[2], 2000)

def map_color(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def setColor(col):
    B_val = col >> 8
    G_val = col & 0x00FF

    R_val = map_color(B_val, 0, 255, 0, 100)
    G_val = map_color(G_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(R_val)
    p_G.ChangeDutyCycle(G_val)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/on')
def on():
    p_B.start(0)
    p_G.start(0)
    setColor(0x0000ff)
    return render_template('on.html')


@app.route('/off')
def off():
    p_B.stop()
    p_G.stop()
    GPIO.output(pins, GPIO.LOW)
    return render_template('off.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
