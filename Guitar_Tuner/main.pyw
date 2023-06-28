from models.stream import Stream, TuningStatus
from models.tunings import TUNINGS

import sys

from PySide2.QtCore import QRect, QSize, Qt, Signal, Slot
from PySide2.QtWidgets import *


class MainWindow(QMainWindow):
    freq_changed = Signal(int)
    freq_diff_changed = Signal(float)
    closest_pitch_changed = Signal(str)
    strings_changed = Signal(list)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(QSize(700, 600))
        self.setMinimumSize(QSize(700, 600))
        self.setMaximumSize(QSize(700, 600))
        self.setWindowTitle('Tuner')

        self.freq_changed.connect(self.update_freq)
        self.freq_diff_changed.connect(self.update_freq_diff)
        self.closest_pitch_changed.connect(self.update_closest_pitch)
        self.strings_changed.connect(self.update_strings)

        self.initialize_window()

    def initialize_window(self):
        self.initialize_central_widget()

        self.initialize_closest_pitch()

        self.initialize_freq()

        self.initialize_buttons_grid()

        self.initialize_over_and_under_tone()

        self.initialize_strings_grid()

        self.setCentralWidget(self.central_widget)

    def initialize_central_widget(self):
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('central_widget')
        self.central_widget.setStyleSheet(
            """
            #central_widget {
                background: #011936;
            }

            * {
                color: #fff;
            }
            """
        )

    def initialize_strings_grid(self):
        self.strings_grid = QWidget(self.central_widget)
        self.strings_grid.setObjectName('strings_grid')
        self.strings_grid.setGeometry(QRect(50, 304, 601, 126))
        self.strings_grid.setStyleSheet(
            """
            #strings_grid QPushButton {
                background: rgba(98, 139, 72, 0.3);
                border: 1px solid rgb(98, 139, 72);
                border-radius: 17px;
                font: 14px 'Montserrat';
                font-weight: 450;
                margin: 15px;
                padding: 10px;
            }
            """
        )
        self.strings = QHBoxLayout(self.strings_grid)
        self.strings.setObjectName('strings')
        self.strings.setContentsMargins(9, 9, 9, 9)
        for i, pitch in enumerate(TUNINGS['guitar standard']):
            attr = f'string_{i}'
            setattr(self, attr, QPushButton(self.strings_grid))
            getattr(self, attr).setObjectName(attr)
            getattr(self, attr).setText(str(pitch))
            self.strings.addWidget(getattr(self, attr))

    def initialize_over_and_under_tone(self):
        self.over_tone = QFrame(self.central_widget)
        self.over_tone.setObjectName('over_tone')
        self.over_tone.setGeometry(QRect(0, 0, 0, 0))
        self.over_tone.setAutoFillBackground(True)
        self.over_tone.setStyleSheet(
            """
            #over_tone {
                color: rgb(98, 139, 72);
            }
            """
        )
        self.over_tone.setFrameShadow(QFrame.Plain)
        self.over_tone.setLineWidth(20)
        self.over_tone.setFrameShape(QFrame.HLine)
        self.under_tone = QFrame(self.central_widget)
        self.under_tone.setObjectName('under_tone')
        self.under_tone.setGeometry(QRect(0, 0, 0, 0))
        self.under_tone.setAutoFillBackground(True)
        self.under_tone.setStyleSheet(
            """
            #under_tone {
                color: rgb(237, 37, 78);
            }
            """
        )
        self.under_tone.setFrameShadow(QFrame.Plain)
        self.under_tone.setLineWidth(20)
        self.under_tone.setFrameShape(QFrame.HLine)

    def initialize_buttons_grid(self):
        self.buttons_grid = QWidget(self.central_widget)
        self.buttons_grid.setObjectName('buttons_grid')
        self.buttons_grid.setGeometry(QRect(50, 425, 601, 126))
        self.buttons_grid.setStyleSheet(
            """
            #buttons_grid QPushButton {
                background: rgba(237, 37, 78, 0.3);
                border: 1px solid rgba(237, 37, 78, 0.5);
                border-radius: 16px;
                font: 14px 'Montserrat';
                font-weight: 450;
                margin: 5px;
                padding: 8px 5px;
                }
            #buttons_grid QPushButton:pressed {
                background: rgba(237, 37, 78, 0.8);
            }
            """
        )
        self.buttons = QVBoxLayout(self.buttons_grid)
        self.buttons.setObjectName('buttons')
        self.buttons_row1 = QHBoxLayout()
        self.buttons_row1.setObjectName('buttons_row1')
        self.buttons_row2 = QHBoxLayout()
        self.buttons_row2.setObjectName('buttons_row2')
        for i, tuning in enumerate(TUNINGS):
            attr = '_'.join(tuning.split())
            setattr(self, attr, QPushButton(self.buttons_grid))
            getattr(self, attr).setObjectName(attr)
            getattr(self, attr).setText(tuning)

            if i % 2 == 0:
                self.buttons_row1.addWidget(getattr(self, attr))
            else:
                self.buttons_row2.addWidget(getattr(self, attr))
        self.buttons.addLayout(self.buttons_row1)
        self.buttons.addLayout(self.buttons_row2)

    def initialize_freq(self):
        self.freq = QLabel(self.central_widget)
        self.freq.setObjectName('freq')
        self.freq.setGeometry(QRect(50, 50, 601, 126))
        self.freq.setAlignment(Qt.AlignCenter)
        self.freq.setText('440 Hz')
        self.freq.setStyleSheet(
            """
            #freq {
                background: qlineargradient(spread:pad, x1:0.5, y1:0.45, x2:0.5, y2:1, stop:0 rgba(31, 31, 31, 0), stop:0.001 rgba(237, 37,78, 255));
                font-family: 'Montserrat';
                font-size: 90px;
                font-weight: 700;
                margin: 0 auto;
            }
            """
        )

    def initialize_closest_pitch(self):
        self.closest_pitch = QLabel(self.central_widget)
        self.closest_pitch.setObjectName('closest_pitch')
        self.closest_pitch.setGeometry(QRect(50, 200, 601, 76))
        self.closest_pitch.setText('A4')
        self.closest_pitch.setAlignment(Qt.AlignCenter)
        self.closest_pitch.setStyleSheet(
            """
            #closest_pitch {
                background: #ecbc4c;
                font-family: 'Montserrat Black';
                font-size: 48px;
            }
            """
        )

    @Slot(int)
    def update_freq(self, freq):
        self.freq.setText(f'{str(freq)} Hz')

    @Slot(str)
    def update_closest_pitch(self, pitch):
        self.closest_pitch.setText(pitch)

    @Slot(float)
    def update_freq_diff(self, freq_diff):
        if freq_diff == 0:
            win.over_tone.resize(0, win.over_tone.height())
            win.under_tone.resize(0, win.under_tone.height())

        if freq_diff > 0:
            win.over_tone.setGeometry(QRect(
                350,
                276,
                int(301 * abs(freq_diff)),
                20
            ))
            win.under_tone.resize(0, win.under_tone.height())

        if freq_diff < 0:
            win.under_tone.setGeometry(QRect(
                50 + (301 - int(301 * abs(freq_diff))),
                276,
                int(301 * abs(freq_diff)),
                20
            ))
            win.over_tone.resize(0, win.under_tone.height())

    @Slot(list)
    def update_strings(self, strings):
        if len(strings) == 4:
            win.string_4.hide()
            win.string_5.hide()

        else:
            win.string_4.show()
            win.string_5.show()

        for (i, (pitch, freq)) in enumerate(strings):
            getattr(win, f'string_{i}').setText(str(pitch))
            getattr(win, f'string_{i}').setStyleSheet(
                f"""
                #string_{str(i)} {{
                    background: qlineargradient(spread:pad, x1:0.5, y1:{'%.2f' % (1 - freq)}, x2:0.5, y2:1, stop:0 rgba(98, 139, 72, 0.3), stop:0.001 rgba(98, 139, 72, 1));
                }}
                """
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()


    def update_view(ts: TuningStatus):
        win.freq_changed.emit(int(ts.freq))
        win.closest_pitch_changed.emit(str(ts.closest_pitch))
        win.freq_diff_changed.emit(ts.freq_diff_normalized)
        win.strings_changed.emit(ts.strings)


    stream = Stream(update_view)
    stream.start()

    win.guitar_standard.clicked.connect(lambda: stream.update_instrument(TUNINGS['guitar standard']))
    win.guitar_half_step_down.clicked.connect(lambda: stream.update_instrument(TUNINGS['guitar half step down']))
    win.mandolin_standard.clicked.connect(lambda: stream.update_instrument(TUNINGS['mandolin standard']))
    win.baritone_ukulele.clicked.connect(lambda: stream.update_instrument(TUNINGS['baritone ukulele']))
    win.soprano_ukulele.clicked.connect(lambda: stream.update_instrument(TUNINGS['soprano ukulele']))
    win.four_string_bass.clicked.connect(lambda: stream.update_instrument(TUNINGS['four string bass']))

    sys.exit(app.exec_())
