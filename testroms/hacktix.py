from test import *


all = [
    Test("hacktix/bully.gb (DMG)", rom="hacktix/bully.gb", runtime=0.5,
        description="A collection of multiple test cases testing a variety of behaviors. (See Repository for Details)", url="https://github.com/Hacktix/BullyGB"),
    Test("hacktix/bully.gb (GBC)", rom="hacktix/bully.gb", runtime=0.5, model=CGB,
        description="A collection of multiple test cases testing a variety of behaviors. (See Repository for Details)", url="https://github.com/Hacktix/BullyGB"),
    Test("hacktix/strikethrough.gb", rom="hacktix/strikethrough.gb", runtime=0.5,
        description="Abuse of OAM DMA transfers during PPU modes 2 and 3 causing interference with data reads from the PPU."),
]
