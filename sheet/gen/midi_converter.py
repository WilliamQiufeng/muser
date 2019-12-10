
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /williamye/program/pyxel_projects/muser/sheet/gen/midi_converter.py    #
# Project: /williamye/program/pyxel_projects/muser/sheet/gen                   #
# Created Date: Tuesday, December 3rd 2019, 12:05:52 pm                        #
# Author : Qiufeng54321                                                        #
# Email : williamcraft@163.com                                                 #
#                                                                              #
# Copyright (C) 2019  Qiufeng54321                                             #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
# You should have received a copy of the GNU General Public License            #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.       #
# -----                                                                        #
# Description:                                                                 #
#   Converts midi file to muser sheet format.                                  #
#                                                                              #
*------------------------------------------------------------------------------*
'''


import sys
import json
import mido
from mido import MidiFile
import io
from sheet.gen.abs_output import *
import time
from .rel_input import *

out = io.open("/williamye/program/pyxel_projects/muser/test/out.txt", "w")
debug = io.open("/williamye/program/pyxel_projects/muser/test/debug.txt", "w")

INDEX_OFFSET = 0
INDEX_LENGTH = 1
INDEX_NOTE = 2

def midifile_to_dict(mid, tempo_index: int, indexes: list):
    tracks = []
    for track in mid.tracks:
        tracks.append([vars(msg).copy() for msg in track])
    res = {}
    tempo_changes = []
    tempo_tick_buf = 0
    for x in tracks[tempo_index]:
        tempo_tick_buf += x["time"]
        if x["type"] == "set_tempo":
            tempo_changes.append((tempo_tick_buf, x["tempo"]))
    res[tempo_index] = tempo_changes
    for index in indexes:
        tick = 0
        tick_sec = 0
        tempo_change_index = -1
        cur_tempo = 500000
        track_res_array = []
        note_on_buffer = {}
        for x in tracks[index]:
            debug.write("------------------------------------------------\n")
            debug.write(f"{x}\n")
            # Change tempo
            tempo_change_interval_tick = 0
            before_tempo = cur_tempo
            while tempo_change_index < len(tempo_changes) - 1:
                if tick >= tempo_changes[tempo_change_index + 1][0]:
                    tempo_change_index += 1
                    cur_tempo = tempo_changes[tempo_change_index][1]
                    tempo_change_interval_tick = tick - tempo_changes[tempo_change_index][0]
                    debug.write(f"Changed tempo from {before_tempo} to {cur_tempo}\n")
                    debug.write(f"  Tempo Change Tick: {tempo_change_interval_tick}\n")
                else:
                    break
            if "time" in x.keys():
                note_change_interval_tick = x["time"] - tempo_change_interval_tick
                tempo_change_interval_sec = mido.tick2second(tempo_change_interval_tick, mid.ticks_per_beat, before_tempo)
                note_change_interval_sec = mido.tick2second(note_change_interval_tick, mid.ticks_per_beat, cur_tempo)
                total_interval_sec = tempo_change_interval_sec + note_change_interval_sec
                tick_sec += total_interval_sec
                tick += x["time"]
                debug.write(f"Time Change:               {x['time']}\n")
                debug.write(f"Note Change Interval Tick: {note_change_interval_tick}\n")
                debug.write(f"Tempo Change Interval Tick:{tempo_change_interval_tick}\n")
                debug.write(f"Note Change Interval Sec:  {note_change_interval_sec}\n")
                debug.write(f"Tempo Change Interval Sec: {tempo_change_interval_sec}\n")
                debug.write(f"Total:                     {total_interval_sec}\n")
                debug.write(f"Tick Sec:                  {tick_sec}\n")
            if x["type"] not in ["note_on", "note_off"]:
                continue
            if x["type"] == "note_on":
                if x["note"] not in note_on_buffer.keys():
                    note_on_buffer[x["note"]]: list = []
                note_on_buffer[x["note"]].append(tick_sec)
            elif x["type"] == "note_off":
                note_array: list = note_on_buffer[x["note"]]
                offset: float = note_array[len(note_array) - 1]
                length_sec = tick_sec - offset
                track_res_array.append((offset, length_sec, x["note"]))
            debug.write("------------------------------------------------\n")
        res[index] = track_res_array
    return res


def to_json(file, tempo_index = 0, indexes = [1], simulate = False):
    mid = mido.MidiFile(file)
    res: dict = midifile_to_dict(mid, tempo_index, indexes)
    out.write(json.dumps(res, indent=4))
    face_dict = {}
    face_gen_ind = 0
    abs_notes = []
    #print(json.dumps(res, indent=2))
    for ind in indexes:
        x = res[ind]
        for tmp in x:
            face = 0
            if tmp[INDEX_NOTE] not in face_dict:
                face_dict[tmp[INDEX_NOTE]] = face_gen_ind
                face_gen_ind += 1
                if face_gen_ind > 3:
                    face_gen_ind = 0
            face = face_dict[tmp[INDEX_NOTE]]
            abs_notes.append(
                AbsNote(tmp[INDEX_OFFSET] * 1000,
                0,# tmp["length"],
                NoteSpeed.SLOW, True, face))
    abs_notes.sort(key=lambda t: t.offset)
    if simulate:
        #NEWLINE = "\n"
        #print(NEWLINE.join([str(x) for x in abs_notes]))
        print("Start simulating...")
        for x in range(len(abs_notes)):
            print(abs_notes[x])
            if x < len(abs_notes) - 1:
                time.sleep((abs_notes[x + 1].offset - abs_notes[x].offset) / 1000)
    return abs_notes
def print_json(file):

    midi_file = MidiFile(file)

    for i, track in enumerate(midi_file.tracks):
        out.write('=== Track {}\n'.format(i))
        for message in track:
            out.write('  {!r}\n'.format(message))

class MidiToAbsSheet:
    def __init__(self, filename, tempo_index = 0, indexes = [1], simulate = False):
        self.abs_notes = to_json(filename, tempo_index, indexes, simulate)
    def to_abs_sheet(self, meta = {}):
        self.sheet = SourceSheetInput()
        self.sheet.preprocess = meta
        self.sheet.process()
        self.sheet.abs_notes = self.abs_notes
        self.sheet.music_offset = 2000
        return self.sheet.to_abs()
