#!/usr/bin/env python3
import xpc
# from time import sleep

import rtmidi

midiin = rtmidi.RtMidiIn()

def print_midi_message(midi):
    if midi.isNoteOn():
        print('NoteOn: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('NoteOff:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('ControlChange', midi.getControllerNumber(), midi.getControllerValue(), f"(unipolar={normalize_to_zero_one(midi.getControllerValue())} bipolar={normalize_to_minus_one_one(midi.getControllerValue())})")

def normalize_to_minus_one_one(integer):
    if 0 <= integer <= 127:
        return (integer - 63.5) / 63.5
    else:
        return None

def normalize_to_zero_one(integer):
    return integer / 127.0 if integer >= 0 and integer <= 127 else None

print("X-Plane MIDI interface")

with xpc.XPlaneConnect() as xplane:
    try:
        # If X-Plane does not respond to the request, a timeout error
        # will be raised.
        xplane.getDREF("sim/test/test_float")
    except:
        print("Error establishing connection to X-Plane, exiting..")
        exit();

    ports = range(midiin.getPortCount())
    novation = None
    if ports:
        for i in ports:
            port = midiin.getPortName(i)
            print(f"{i} {port}")
            if (port == "Launchpad Mini MK3 LPMiniMK3 MIDI Out"):
                novation = i
                print(f"Novation Launchpad Mini MK3 found at port {i}")

        if novation:
            midiin.openPort(i)

            while True:
                m = midiin.getMessage(250) # some timeout in ms
                if m:
                    print_midi_message(m)

                    ccn = m.getControllerNumber()
                    ccv = m.getControllerValue()
                    unipolar=normalize_to_zero_one(ccv)
                    bipolar=normalize_to_minus_one_one(ccv)

                    if ccn == 0:
                        # Throttle
                        dref = "sim/cockpit2/engine/actuators/throttle_ratio_all"
                        value = unipolar
                    elif ccn == 1:
                        # Yoke pitch
                        dref = "sim/cockpit2/controls/yoke_pitch_ratio"
                        value = bipolar
                    elif ccn == 2:
                        # Yoke roll
                        dref = "sim/cockpit2/controls/yoke_roll_ratio"
                        value = bipolar
                    elif ccn == 3:
                        # Yoke roll
                        dref = "sim/cockpit2/controls/yoke_heading_ratio"
                        value = bipolar
                    elif ccn == 10:
                        dref = "sim/cockpit2/controls/parking_brake_ratio"
                        value = unipolar
                    elif ccn == 11:
                        dref = "sim/cockpit/electrical/taxi_light_on"
                        value = unipolar
                    elif ccn == 12:
                        dref = "sim/cockpit/electrical/battery_on"
                        value = unipolar
                        

                    print (f"Setting {dref} to {value}")
                    xplane.sendDREF(dref, value)

        else:
            print('No MIDI input ports found, exiting..')
            exit();
    


#         # # Set position of the player aircraft
#         # print("Setting position")
#         # #       Lat     Lon         Alt   Pitch Roll Yaw Gear
#         # posi = [37.524, -122.06899, 2500, 0,    0,   0,  1]
#         # client.sendPOSI(posi)
        
#         # # Set position of a non-player aircraft
#         # print("Setting NPC position")
#         # #       Lat       Lon         Alt   Pitch Roll Yaw Gear
#         # posi = [37.52465, -122.06899, 2500, 0,    20,   0,  1]
#         # client.sendPOSI(posi, 1)

#         # # Set angle of attack, velocity, and orientation using the DATA command
#         # print("Setting orientation")
#         # data = [\
#         #     [18,   0, -998,   0, -998, -998, -998, -998, -998],\
#         #     [ 3, 130,  130, 130,  130, -998, -998, -998, -998],\
#         #     [16,   0,    0,   0, -998, -998, -998, -998, -998]\
#         #     ]
#         # client.sendDATA(data)

#         # # Set control surfaces and throttle of the player aircraft using sendCTRL
#         # print("Setting controls")
#         # ctrl = [0.0, 0.0, 0.0, 0.8]
#         # client.sendCTRL(ctrl)

#         # # Pause the sim
#         # print("Pausing")
#         # client.pauseSim(True)
#         # sleep(2)

#         # # Toggle pause state to resume
#         # print("Resuming")
#         # client.pauseSim(False)

#         # # Stow landing gear using a dataref
#         # print("Stowing gear")
#         # gear_dref = "sim/cockpit/switches/gear_handle_status"
#         # client.sendDREF(gear_dref, 0)

#         # # Let the sim run for a bit.
#         # sleep(4)

#         # # Make sure gear was stowed successfully
#         # gear_status = client.getDREF(gear_dref)
#         # if gear_status[0] == 0:
#         #     print("Gear stowed")
#         # else:
#         #     print("Error stowing gear")

#         # gear_dref = "sim/cockpit/switches/gear_handle_status"
#         # client.sendDREF(gear_dref, 0)

#         dref_taxi_light = "sim/cockpit/electrical/taxi_light_on"
#         client.sendDREF(dref_taxi_light, 1)
#         sleep(2)
#         client.sendDREF(dref_taxi_light, 0)
#         sleep(2)
#         client.sendDREF(dref_taxi_light, 1)
#         sleep(2)
#         client.sendDREF(dref_taxi_light, 0)
#         sleep(2)
#         client.sendDREF(dref_taxi_light, 1)
#         sleep(2)
#         client.sendDREF(dref_taxi_light, 0)

#         dref_throttle = "sim/cockpit2/engine/actuators/throttle_ratio_all"
#         dref_pitch = "sim/cockpit2/controls/yoke_pitch_ratio"
#         dref_roll = "sim/cockpit2/controls/yoke_roll_ratio"
#         dref_heading = "sim/cockpit2/controls/yoke_heading_ratio"
#         dref_parking_brake = "sim/cockpit2/controls/parking_brake_ratio"



#         print("End of Python client example")
#         input("Press any key to exit...")


# # sim/cockpit2/controls/motorbrake_ratio
# # sim/cockpit2/controls/speedbrake_ratio
# # sim/cockpit2/controls/aileron_trim
# # sim/cockpit2/controls/elevator_trim
# # sim/cockpit2/controls/rudder_trim
# # sim/cockpit2/engine/actuators/ignition_key
# # sim/cockpit2/engine/actuators/ignition_on
# # sim/cockpit/electrical/battery_on