## Pain hallucination task

Pain conditioning variant of the task from Powers et al (Science, 2017) using electrical stimulation, implemented in PsychoPy.

To run from command line, set working directory to the task root directory and run `python pain_hallucination_task.py`

Trial settings are given in the `pain_hallucination_task_settings.yaml` config file.

By default, QUEST calibration is run however this can be turned off by unchecking the box when starting the task.

### Task order

1. Practice trials with yes/no responses
2. Confidence scale practice
3. Practice trials with confidence scale
4. QUEST calibration
5. Task (4 session, 4 blocks of 30 trials per session including one catch block)

### Trial order for main task

1. Stimulation and checkerboard/question mark stimuli fade in (ramp up period in config file)
2. Stimulation & visual stimulus intensity held constant (hold period in config)
3. Stimulation & visual stimuli fade out (ramp down period in config)
4. Subject makes a response and indicates confidence (maximum allowed response time given in config

### Changing instructions

Instructions for each stage are given in text files. Instruction blocks to be shown on consecutive screens are separated by asterisks.

### Requirements

Requires PyLibNIDAQmx (https://github.com/pearu/pylibnidaqmx) for DAQ interface
