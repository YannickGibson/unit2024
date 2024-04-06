# UnIT 2024 Best-Prague Hackathon
This is a winning solution that was ranked 2. place on the UnIT hackathon organized by the organization [Best Prague](https://bestprague.cz/).

The goal of this competition was to create an interface to be used in integration with robot Pepper. The robot will be capable leading conversation with students, precisely to communicate to students that might be on the fence about deciding which university programme will they enroll in. The result of the student bot interaction is that the robot suggests a programme that best suits the students needs. The robot also needs to account for the students emotional state.

For details about this challenge check the [assignment pdf](hackathon_assignment.pdf) in repository.


# Demo messages in role of student:
```
Chtěl bych pomoct s výběrem specializace.

Zajímá mě assembly a hraju si s FPGA.

😡
```

# Setup
## Script for TTS
For text to speach to work properly (TTS), you need to ensure that there is a script on the robot Pepper machine that gets message as input and issues robot Pepper to speak the message.
### Private key
The script uses ssh to connect to robot Pepper machine, this file needs to be supplied.

## Environmental variable
You need to set the `OPENAI_API_KEY` environment variable to your OPEN AI account.
```sh
export OPENAI_API_KEY=<your key>
```
## Run gradio
```sh
python gradio_example.py
```
The website will be available at http://localhost:7860/