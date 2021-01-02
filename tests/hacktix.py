from test import Test


all = [
    Test("hacktix/bully.gb (DMG)", rom="hacktix/bully.gb", runtime=0.5,
        description="DMA bus conflict to execute code.", url="https://github.com/Hacktix/BullyGB"),
    Test("hacktix/bully.gb (GBC)", rom="hacktix/bully.gb", runtime=0.5, gbc=True,
        description="DMA bus conflict to execute code.", url="https://github.com/Hacktix/BullyGB"),
]
