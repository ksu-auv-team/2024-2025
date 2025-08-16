# 2024-2025
AUV Software for 2024-2025 school year

# Discuss with Sam 
Ensure there is at least a minimum of an hour between raffle and time slot we take. Makes sure that you have practice time. 

## Notes for Ryan
Plug my router into the battery pack to power it before you go to the big pool to ensure that its powered and working before you go to the pool side.

Make sure to practice unplugging the tether and getting the timing right (in the root run.py file near the bottom) for the replay functionality. 
Recommend someone has a timer going. Timer is 60 seconds right now, increase or decrease it as you see fit. It's just a sleep function before the process gets started.

What I need you to do,

1. Use the kiddy pool to pilot the sub manually to get used to the controls.
To run the manual controls you will need two terminals open and the controller connected to your computer.
On the orin
```bash
python3 run.py --real-world --print-debug
```

On your computer
```bash
python3 controller_rewrite.py --sendDB --debug
```
Controller:
Hold controller normally
Top Right switch labelled H is the arm. Up = Arm Down = Disarm
Controller code will exit after you disarm so rerun it if needed.

2. After you feel comfortable, go for manual piloting through the gate in the big pool lane.
Commands same as before

## Reference run with Judge
3. After you complete going through the gate (Step 2) get them to reset the sub and call a judge
```bash
python3 run.py --to-qualify --print-debug
```

Make sure to run the above in a screen or it will stop running when tether is disconnected. 
If you want to test the replay functionality in the kiddy pool as well you can. Just send the sub forward for like 3 seconds and then rerun the code in replay. 

Call me if any questions, phone is on ringer.