# Microphone AppIndicator for Ubuntu
This Appindicator allows you to see if the microphone is currently muted and also to mute or unmute it.

# Preview
![Microphone Indicator Preview](./docs/preview.gif)

# Running
To start the indicator just execute the python script:

```bash
python micindicator.py
```

# Auto start application after login
 - run the `gnome-session-properties` command
 - Click `Add`
 - Pass the path of `micindicator.py` as command
 - Give the name you want

# Changing the keyboard shortcut
To change the global keyboard shortcut used to mute / unmute the microphone change keystroke combination in `keystr` variable in `micindicator.py` script and run the application again:

```python
keystr = "<Ctrl><Alt><Shift>M"
```

# Credits 
Icon made by [Smashicons](https://www.flaticon.com/authors/smashicons) from www.flaticon.com (modified version)

# To-do list
- [ ] Change the icon when the microphone is muted outside the application
- [ ] Icons for dark and light theme