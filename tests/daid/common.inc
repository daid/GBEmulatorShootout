INCLUDE "hardware.inc"

SECTION "entry", ROM0[$100]
  jp start
  ds $0150 - @, 0

SECTION "lib", ROMX
disableLCD:
  ld   a, [rLCDC]
  bit  7, a
  ret  z
  ; Disable the LCD, needs to happen during VBlank, or else we damage hardware
.waitForVBlank:
  ld   a, [rLY]
  cp   144
  jr   c, .waitForVBlank

  xor  a
  ld   [rLCDC], a ; disable the LCD by writting zero to LCDC
  ret

;   HL target
;   DE source
;   BC length
memcpy:
  ld  a, b
  or  c
  ret z
  ld  a, [de]
  ld  [hl+], a
  inc de
  dec bc
  jr  memcpy

initFont:
  ld  hl, $9010
  ld  de, fontData
  ld  bc, fontData.end - fontData
  jp  memcpy

; DE = string
; HL = vram
print:
  ld  a, [de]
  inc de
  and a
  ret z
  ld  c, a
.statWait:
  ld  a, [rSTAT]
  and $03
  jr  nz, .statWait
  ld  [hl], c
  inc hl
  jr  print


SECTION "font", ROMX
fontData:
  incbin "font.bin"
.end:
