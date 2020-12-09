INCLUDE "hardware.inc"

SECTION "vblankInt", ROM0[$040]
  jp vblankInt

SECTION "statInt", ROM0[$048]
  jp statInt

SECTION "entry", ROM0[$100]
  jp start

SECTION "main", ROM0[$150]
start:
  ld a, [rLY]
  cp 145
  jr nz, start
  ld a, 1
  ld hl, $9000
  ld [hl+], a

  ld a, LCDCF_BGON | LCDCF_ON
  ld [rLCDC], a
  ld a, STATF_LYC
  ld [rSTAT], a
  ld a, IEF_LCDC | IEF_VBLANK
  ld [rIE], a
  xor a
  ld [rLYC], a
  ld c, low(rBGP)
  ei
  halt

vblankInt:
  pop hl
  ei
  halt

statInt:
  pop hl
  ei
  nop
  ld hl, data
loop:
REPT 10
  ld a, [hl+]
  ld [c], a
ENDR
REPT 98 - 12 - 16
  nop
ENDR
  jp loop

data:
REPT 8
  db $e4, $e4, $e4, $e4, $e4, $e4, $e4, $e4, $e4, $e4
ENDR
REPT 16
  db $e4, $e4, $ff, $ff, $ff, $ff, $ff, $ff, $e4, $e4
ENDR
REPT 16
  db $e4, $ff, $55, $55, $55, $55, $55, $55, $ff, $e4
ENDR
REPT 16
  db $e4, $ff, $55, $ff, $55, $55, $ff, $55, $ff, $e4
ENDR
REPT 16
  db $e4, $ff, $55, $55, $55, $55, $55, $55, $ff, $e4
ENDR
REPT 16
  db $e4, $ff, $55, $55, $55, $55, $55, $55, $ff, $e4
ENDR
REPT 16
  db $e4, $ff, $55, $ff, $ff, $ff, $ff, $55, $ff, $e4
ENDR
REPT 16
  db $e4, $ff, $55, $55, $55, $55, $55, $55, $ff, $e4
ENDR
REPT 16
  db $e4, $e4, $ff, $ff, $ff, $ff, $ff, $ff, $e4, $e4
ENDR
REPT 16
  db $e4, $e4, $e4, $e4, $e4, $e4, $e4, $e4, $e4, $e4
ENDR
