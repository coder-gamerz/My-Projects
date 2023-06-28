from models.pitch import Note, Pitch

TUNINGS = {
    'guitar standard': [
        Pitch(Note.E, 2),
        Pitch(Note.A, 2),
        Pitch(Note.D, 3),
        Pitch(Note.G, 3),
        Pitch(Note.B, 3),
        Pitch(Note.E, 4)
    ],
    'guitar half step down': [
        Pitch(Note.DSharp, 2),
        Pitch(Note.GSharp, 2),
        Pitch(Note.CSharp, 3),
        Pitch(Note.FSharp, 3),
        Pitch(Note.ASharp, 3),
        Pitch(Note.DSharp, 4)
    ],
    'mandolin standard': [
        Pitch(Note.G, 3),
        Pitch(Note.D, 4),
        Pitch(Note.A, 4),
        Pitch(Note.E, 5)
    ],
    'soprano ukulele': [
        Pitch(Note.G, 4),
        Pitch(Note.C, 4),
        Pitch(Note.E, 4),
        Pitch(Note.A, 4)
    ],
    'baritone ukulele': [
        Pitch(Note.D, 3),
        Pitch(Note.G, 3),
        Pitch(Note.B, 3),
        Pitch(Note.E, 4)
    ],
    'four string bass': [
        Pitch(Note.E, 1),
        Pitch(Note.A, 1),
        Pitch(Note.D, 2),
        Pitch(Note.G, 2)
    ]
}