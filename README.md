# Portable Challenges Plugin

Compatable with Splunk CTF Scoreboard (https://github.com/splunk/SA-ctf_scoreboard)

This plugin provides the ability to import and export challneges in a portable, human-readble format (currently YAML).

### Objectives:
* Allow challenges to be saved outside of the database
* Allow for source control on challenges
* Allow for easy human editing of challenges offline
* Enable rapid deployment of challenges to a Splunk CTF instance

### Installation:
Simple clone this repsitory into a working folder

#### Command line interface:
The `importer.py` scripts can be called directly from the CLI.

The help dialog follows:
```
usage: importer.py [-h] [-s SRC_FILE] [-d DEST_DIR] [--skip-on-error]
```

#### YAML Specification:
Each challenge is a single document. Multiple documents can be present in one YAML file, separated by “---”, as specified by YAML 1.1.

Following is a list of top level keys with their usage.

**name**
* Type: Single line text
* Usage: Specify the title which will appear to the user at the top of the challenge and on the challenge page

**category**
* Type: Single line text
* Usage: Specify the category the challenge will appear a part of

**value**
* Type: Positive integer
* Usage: The amount of point awarded for completion of the problem

**description**
* Type: Multiline text
* Usage: The the body text of the challenge.

**flag**
* Type: Single line text
* Usage: The flag/key text

**hints** (optional)
* Type: List of hint objects

  **id**
  * Type: Positive integer
  * Usage: Hint ID unique to this challenge. Used internally to enable hint updates.

  **hint**
  * Type: Multiline text
  * Usage: The body text of the hint in markdown. If HTML tags are used, they will be rendered.

  **cost**
  * Type: Positive integer
  * Usage: The amount of points that will be deducted for using the hint

**start_time** (optional)
* Type: posative int
* Usage: The epoch time that this question becomes valid (defaults to 1 if no value given)

**end_time** (optional)
* Type: posative int
* Usage: The epoch time that this question becomes invalid (defaults to 1893456000 [1 Jan 2030] if no value given)

**bonus_instructions** (optional)
* Type: Multiline string
* Usage: Instructions for additional points for the problem

**bonus_points** (optional)
* Type: Posative int
* Usage: The point value for the bonus points

##### Example YAML File
```YAML
---
---
name: QR Part Deux
category: Forensics
value: 80
description: Yet another QR code challenge
files:
  - QRPartDeux/QRPartDeux.zip
flag: acsc2017{a_little_like_last_year_is_ok}
hints:
  - id: 1
    hint: dotcode, codablock F, Scanner, CortexScan test
    cost: 60
---
name: animate_me
category: Forensics
value: 40
description: Tear apart the GIF file and find the flag
flag: acsc2017{FrameByFrame}
---
name: broken_rsa
category: Cryptography
value: 90
description: Exploit broken RSA implementation.
  This is a test multiline description
  Testing with a blank line.
flag: acsc2017{LooseLipsSinkShips}
hints:
  - id: 1
    hint: Are all the fields of the public key meant to be public?
    cost: 25
  - id: 2
    hint: Look for where d is calculated (gen_keypair) for how to calculate it.
    cost: 25
  - id: 3
    hint: |
      If the known modules n is the result of a known prime multiplied with
      an unknown prime, how can you figure out the unknown prime?
    cost: 25
---
name: checker1
category: Reverse Engineering
value: 100
description: Reverse the binary
flag: acsc2017{arent_interpreters_great?}
---
name: checker2
category: Reverse Engineering
value: 150
description: Reverse the binary
flag: acsc2017{mg8gj7GnONlolhIrwN2p}
---
name: cyber_haiku
category: Pwnable
value: 60
description: Exploit the program.
  nc challenge.acsc17.us 5000
flag: acsc2017{user_input_is_evil}
start_time: 1503
end_time: 42323
---
name: find_the_flag
category: Forensics
value: 30
description: Find the flag the in the telnet session
files:
  - find_the_flag/find_the_flag.pcap
flag: acsc2017{UseSSHDummy}
---
name: forgot_to_patch
category: Web Exploitation
value: 55
description: You know that the flag is located at www.fake-wordpress-site.us/flag.txt...
  Now just get the answer.
flag: acsc2017{UpdateYourPlugins}
bonus_instructions: This has a points value.
bonus_points: 10
---
name: helloworld_c
category: Pwnable
value: 40
description: Exploit the program.
  ssh -p 2222 helloworld-c@challenge.acsc17.us
  Password: helloworld
flag: acsc2017{setuid_and_call_system_what_could_possibly_go_wrong}
bonus_instructions: This has no value.
---
name: helloworld_c2
category: Pwnable
value: 50
description: Exploit the program
  ssh -p 2222 helloworld-c2@challenge.acsc17.us
  Password: helloworld
flag: acsc2017{bad_sanitization_is_bad_and_should_feel_bad}
```

Thanks to https://github.com/shareef12/ctfd-portable-challenges-plugin for the original idea and some of the framework.
