from unittest import TestCase
from pitch import Pitch, Note


class TestPitch(TestCase):
    def test_half_steps_distance(self):
        self.assertEqual(Pitch(Note.C, 5).half_steps_distance(Pitch(Note.A, 4)), 3)
        self.assertEqual(Pitch(Note.DSharp, 3).half_steps_distance(Pitch(Note.DSharp, 1)), 24)
        self.assertEqual(Pitch(Note.G, 4).half_steps_distance(Pitch(Note.A, 3)), 10)

    def test_frequency(self):
        self.assertAlmostEqual(Pitch(Note.A, 4).frequency, 440, places=2)
        self.assertAlmostEqual(Pitch(Note.B, 0).frequency, 30.87, places=2)
        self.assertAlmostEqual(Pitch(Note.D, 4).frequency, 293.66, places=2)

    def test_shift(self):
        self.assertEqual(Pitch(Note.C, 5).shift(-3), Pitch(Note.A, 4))
        self.assertEqual(Pitch(Note.A, 1).shift(2), Pitch(Note.B, 1))
        self.assertEqual(Pitch(Note.CSharp, 5).shift(12), Pitch(Note.CSharp, 6))
        self.assertEqual(Pitch(Note.DSharp, 6).shift(-25), Pitch(Note.D, 4))

    def test_from_frequency(self):
        self.assertEqual(Pitch.from_frequency(442), Pitch(Note.A, 4))
        self.assertEqual(Pitch.from_frequency(37), Pitch(Note.D, 1))
        self.assertEqual(Pitch.from_frequency(112.25), Pitch(Note.A, 2))
        self.assertEqual(Pitch.from_frequency(16.4), Pitch(Note.C, 0))
        self.assertEqual(Pitch.from_frequency(109), Pitch(Note.A, 2))
