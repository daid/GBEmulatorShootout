from test import Test


all = [
    Test("daid/ppu_scanline_bgp.gb", runtime=0.5),
    Test("daid/stop_instr.gb (DMG)", runtime=0.5, rom="daid/stop_instr.gb", result="daid/stop_instr.dmg.png", gbc=False),
    Test("daid/stop_instr.gb (GBC)", runtime=0.5, rom="daid/stop_instr.gb", result="daid/stop_instr.gbc.png", gbc=True),
    Test("daid/stop_instr_gbc_mode3.gb", runtime=0.5, gbc=True),
    Test("daid/speed_switch_timing_div.gbc", runtime=0.5, gbc=True),
    Test("daid/speed_switch_timing_ly.gbc", runtime=0.5, gbc=True),
    Test("daid/speed_switch_timing_stat.gbc", runtime=0.5, gbc=True),
]
