from test import Test


all = [
    Test("daid/ppu_scanline_bgp.gb", runtime=0.5, result=["daid/ppu_scanline_bgp_0.png", "daid/ppu_scanline_bgp_1.png"],
        description="Mid scanline BGP register changes. Requires accurate PPU timing. Changing the BGP register can causes one pixel to be the OR result of the previous and next BGP colors, resulting in a black line. This seems hardware dependend as not all DMGs do this."),
    Test("daid/stop_instr.gb (DMG)", runtime=0.5, rom="daid/stop_instr.gb", result="daid/stop_instr.dmg.png", gbc=False,
        description="STOP instruction is usually not used, but it should blank out the screen on classic Gameboy. As the PPU is stopped. NOTE: Running this on real hardware might damage the hardware, as the screen should be turned off before STOP on DMG."),
    Test("daid/stop_instr.gb (GBC)", runtime=0.5, rom="daid/stop_instr.gb", result="daid/stop_instr.gbc.png", gbc=True,
        description="STOP instruction is usually not used, but it should make the screen go black on Color Gameboy. The PPU is still running, but it cannot access VRAM, so it reads all black"),
    Test("daid/stop_instr_gbc_mode3.gb", runtime=0.5, gbc=True,
        description="STOP instruction is usually not used, but doing a STOP during mode 3 on Color Gameboy will keep the screen displaying the same data, as the PPU keeps running, and during mode3 it can access VRAM."),
    Test("daid/speed_switch_timing_div.gbc", runtime=0.5, gbc=True,
        description="Executing a STOP for a speed switch should reset the DIV register. Not doing this could cause problems with RNG for games, failing this will most certainly desync a TAS."),
    Test("daid/speed_switch_timing_ly.gbc", runtime=0.5, gbc=True),
    Test("daid/speed_switch_timing_stat.gbc", runtime=0.5, gbc=True),
    Test("daid/rom_and_ram.gb", runtime=0.5),
]
