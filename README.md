# Pendulum Video Maker
This repo is to create short video files of two pendulums side by side so that the spectator can easy compare different features of the different settings

Using examples:
```
# Single pendulum
python main.py --path "pendulum.mp4" --pend1 0.25 0.075 0.03 0.4 9.81 5.0 -0.785 0.0

# Compare two pendulums  
python main.py --path "comparison.mp4" \
  --pend1 0.25 0.075 0.03 0.4 9.81 5.0 -0.785 0.0 \
  --pend2 0.5 0.075 0.03 0.4 9.81 8.0 -0.785 0.0

# Custom duration and FPS
python main.py --path "custom.mp4" --pend1 0.25 0.075 0.03 0.4 9.81 5.0 -0.785 0.0 --t_end 15.0 --fps 30
```
