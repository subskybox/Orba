#! /usr/bin/env python

import unittest
from orba_sample_set_generator import SampleSet

# filename format is as follows:
#   namePart1<_namePart2_namePartn>_Note<_Velocity><_startLoop><_uuid>.wav

class SampleSetTests(unittest.TestCase):

    def test_name_only(self):
        self.ss = SampleSet('name.wav')
        self.assertEqual('name', self.ss.name)
        self.assertEqual('', self.ss.note)
        self.assertEqual(80, self.ss.velocity)
        self.assertEqual(None, self.ss.midi_note)
        self.assertEqual(None, self.ss.pitch)
        self.assertEqual(0, self.ss.loop_start)
        self.assertEqual(0, self.ss.loop_end)
        self.assertEqual(None, self.ss.uuid)

    def test_name_note_velocity_only(self):
        self.ss = SampleSet('name_C#1_80.wav')
        self.assertEqual('name', self.ss.name)
        self.assertEqual('C#1', self.ss.note)
        self.assertEqual(80, self.ss.velocity)
        self.assertEqual(25, self.ss.midi_note)
        self.assertEqual(34.64782887210901, self.ss.pitch)
        self.assertEqual(0, self.ss.loop_start)
        self.assertEqual(0, self.ss.loop_end)
        self.assertEqual(None, self.ss.uuid)

    def test_name_with_one_token(self):
        self.ss = SampleSet('freepats_A2_127_00c78732cd31bef755f6bfbf410bcae2.wav')
        self.assertEqual('freepats', self.ss.name)

    def test_name_with_two_tokens(self):
        self.ss = SampleSet('freepats_hang_A2_127_00c78732cd31bef755f6bfbf410bcae2.wav')
        self.assertEqual('freepats_hang', self.ss.name)

    def test_name_with_three_tokens(self):
        self.ss = SampleSet('freepats_hang_v2_A2_127_00c78732cd31bef755f6bfbf410bcae2.wav')
        self.assertEqual('freepats_hang_v2', self.ss.name)

    def test_missing_loopStart_loopEnd_uuid(self):
        self.ss = SampleSet('freepats_hang_v2_A2_127.wav')
        self.assertEqual('freepats_hang_v2', self.ss.name)
        self.assertEqual('A2', self.ss.note)
        self.assertEqual(127, self.ss.velocity)
        self.assertEqual(45, self.ss.midi_note)
        self.assertEqual(110.0, self.ss.pitch)
        self.assertEqual(0, self.ss.loop_start)
        self.assertEqual(0, self.ss.loop_end)
        self.assertEqual(None, self.ss.uuid)

    def test_missing_loopEnd(self):
        self.ss = SampleSet('freepats_hang_v2_A#3_001_1000_00c78732cd31bef755f6bfbf410bcae2.wav')
        self.assertEqual('freepats_hang_v2', self.ss.name)
        self.assertEqual('A#3', self.ss.note)
        self.assertEqual(1, self.ss.velocity)
        self.assertEqual(58, self.ss.midi_note)
        self.assertEqual(233.08188075904496, self.ss.pitch)
        self.assertEqual(1000, self.ss.loop_start)
        self.assertEqual(0, self.ss.loop_end)
        self.assertEqual("00c78732cd31bef755f6bfbf410bcae2", self.ss.uuid)

    def test_all_present(self):
        self.ss = SampleSet('freepats_hang_Bb3_050_1000_2000_00c78732cd31bef755f6bfbf410bcae2.wav')
        self.assertEqual('freepats_hang', self.ss.name)
        self.assertEqual('Bb3', self.ss.note)
        self.assertEqual(50, self.ss.velocity)
        self.assertEqual(58, self.ss.midi_note)
        self.assertEqual(233.08188075904496, self.ss.pitch)
        self.assertEqual(1000, self.ss.loop_start)
        self.assertEqual(2000, self.ss.loop_end)
        self.assertEqual("00c78732cd31bef755f6bfbf410bcae2", self.ss.uuid)

    def test_music_dynamic_to_velocity(self):
        self.ss = SampleSet('freepats_hang_Bb3_zf_1000_2000_00c78732cd31bef755f6bfbf410bcae2.wav')
        self.assertEqual('freepats_hang', self.ss.name)
        self.assertEqual('Bb3', self.ss.note)
        self.assertEqual(80, self.ss.velocity)
        self.assertEqual(58, self.ss.midi_note)
        self.assertEqual(233.08188075904496, self.ss.pitch)
        self.assertEqual(1000, self.ss.loop_start)
        self.assertEqual(2000, self.ss.loop_end)
        self.assertEqual("00c78732cd31bef755f6bfbf410bcae2", self.ss.uuid)


if __name__ == '__main__':
    unittest.main()
