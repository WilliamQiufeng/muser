#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
*------------------------------------------------------------------------------*
# File: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/playthrough/criteria_manager.py #
# Project: /Users/Shared/williamye/program/pyxel_projects/muser/muser/game/playthrough #
# Created Date: Tuesday, June 9th 2020, 08:51:11 am                            #
# Author : Qiufeng54321                                                        #
# Email : williamcraft@163.com                                                 #
#                                                                              #
# Copyright (C) 2020  Qiufeng54321                                             #
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
#                                                                              #
#                                                                              #
*------------------------------------------------------------------------------*
'''

from . import note
import game.playthrough.effect.effect_controller as ec

criterias = [None] * 8


class CenterNote:
    note_prop = {
        "offset_pos": [128, 128],
        "size": [0, 0]
    }

def set_criteria(lock_effect_identity: int, sides: list):
    """
    set_criteria set / add criteria area for a specific side

    Stores to criteria[side[0]] for each side with value of start position.
    criterias[side_id] = [lock_effect, relative start position]

    Args:
        lock_effect_identity (int): effect identity for the center position
        sides (list): [side_id, start position relative to the center position]
    """
    for side in sides:
        criterias[side[0]] = [
            CenterNote 
                if lock_effect_identity == -1 
                else ec.EffectController.pool[lock_effect_identity],
            side[1],
            side[2] if len(side) >= 3 else 5
        ]

set_criteria(-1, [
    [0, [0    , -128]],
    [1, [0    , 128]],
    [2, [-128 , 0]],
    [3, [128  , 0]]
])

def get_pos_in_progress(note_target, progress: float):
    """
    get_pos_in_progress returns the position the note should be at by the progress provided.

    might be used in the note position deduction

    Args:
        note_target (note.PositionedNote): the note to be calculated
        progress (float): the progress provided

    Returns:
        coord (tuple): position calculated by the progress and the note's side
    """
    
    side        = note_target.prop["side"]
    criteria    = criterias[side]
    lock_effect = criteria[0]
    lock_effect_offset_x, lock_effect_offset_y = lock_effect.note_prop["offset_pos"]
    lock_effect_size_x, lock_effect_size_y = lock_effect.note_prop["size"]
    center_x, center_y = lock_effect_offset_x + lock_effect_size_x / 2, \
                            lock_effect_offset_y + lock_effect_size_y / 2
                            
    
    note_offset_x, note_offset_y = criteria[1]
    note_offset_x = center_x - note_offset_x
    note_offset_y = center_y - note_offset_y
    
    # From math stackexchange: https://math.stackexchange.com/a/1269705
    progress_position = ((1 - progress) * note_offset_x + progress * center_x,
                        (1 - progress) * note_offset_y + progress * center_y)
    
    return progress_position
    
def get_color(note_target):
    """
    get_color Returns the color of the note

    Args:
        note_target ([Note]): note to get color
    """

    return criterias[note_target.prop["side"]][2]
    