from halloween import *

def do_blink():
    clear_led()
    set_led(1, 100)
    set_led(0, 500)
    set_led(1, 1)

def do_cab_arm_pos():
    cab_arm(100)

def do_cab_arm_neg():
    cab_arm(-100)

def do_cab_head_pos():
    cab_head(100)

def do_cab_head_neg():
    cab_head(-100)

def do_turn_head():
    clear_head()
    set_head(1000, 0, 3)
    set_head(0, 0, 3)

def do_head_0():
    clear_head()
    set_head(0, 0, 3)

def do_head_p1():
    clear_head()
    set_head(100, 0, 3)

def do_head_p2():
    clear_head()
    set_head(200, 0, 3)

def do_head_p3():
    clear_head()
    set_head(300, 0, 3)

def do_head_n1():
    clear_head()
    set_head(-100, 0, 3)

def do_head_n2():
    clear_head()
    set_head(-200, 0, 3)

def do_head_n3():
    clear_head()
    set_head(-300, 0, 3)

def do_turn_head():
    clear_head()
    set_head(500, 0, 3)
    set_head(-500, 0, 3)
    set_head(0, 0, 3)

def do_cast_curse():
    clear_arm()
    set_arm(1200, 0, 0)
    set_arm(0, 0, 0)

def do_music():
    play_sound('hp.wav')

def do_parsel1():
    play_sound('parsel1.wav')

def do_parsel2():
    play_sound('parsel2.wav')

def do_havecandy():
    clear_head()
    set_head(-300, 0, 3)
    sleep(1)
    play_sound('havecandy.wav')

def do_cutecostume():
    clear_head()
    set_head(-300, 0, 3)
    sleep(1)
    play_sound('cutecostume.wav')

def do_haveyouseen():
    clear_head()
    set_head(-300, 0, 3)
    sleep(1)
    play_sound('haveyouseen.wav')

TEST_BOLT_FX = { 
    'delay': 0, 
    'lifetime': 1000, 
    'start': { 'position': 150, 'length': 5, 'spread': 1, 'r': 255, 'g': 0, 'b': 0 },
    'velocity': { 'position': -2, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_bolt_test():
    strip_add_fx(STRIP_BOLT, TEST_BOLT_FX)

VOLDY_HIT_FAST_FX = { 
    'delay': 300, 
    'lifetime': 10, 
    'start': { 'position': 0, 'length': 150, 'spread': 1, 'r': 120, 'g': 120, 'b': 120 },
    'velocity': { 'position': 0, 'length': 0, 'spread': 0, 'r': -4, 'g': -4, 'b': -4 }
}

VOLDY_HIT_FX = { 
    'delay': 800, 
    'lifetime': 10, 
    'start': { 'position': 0, 'length': 150, 'spread': 1, 'r': 120, 'g': 120, 'b': 120 },
    'velocity': { 'position': 0, 'length': 0, 'spread': 0, 'r': -4, 'g': -4, 'b': -4 }
}

KID_RED_FX = { 
    'delay': 0, 
    'lifetime': 1000, 
    'start': { 'position': 150, 'length': 5, 'spread': 1, 'r': 255, 'g': 0, 'b': 0 },
    'velocity': { 'position': -2, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_kid_curse_red():
    strip_add_fx(STRIP_FLASH, VOLDY_HIT_FX)
    strip_add_fx(STRIP_BOLT, KID_RED_FX)
    play_sound('swoosh.wav')

KID_RIDICULO_FX = { 
    'delay': 0, 
    'lifetime': 1000, 
    'start': { 'position': 150, 'length': 5, 'spread': 1, 'r': 255, 'g': 0, 'b': 0 },
    'velocity': { 'position': -2, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_kid_curse_ridiculo():
    strip_add_fx(STRIP_FLASH, VOLDY_HIT_FX)
    strip_add_fx(STRIP_BOLT, KID_RIDICULO_FX)
    play_sound('ridiculo.wav')

KID_BLUE_FX = { 
    'delay': 0, 
    'lifetime': 1000, 
    'start': { 'position': 150, 'length': 5, 'spread': 1, 'r': 120, 'g': 80, 'b': 255 },
    'velocity': { 'position': -2, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_kid_curse_blue():
    strip_add_fx(STRIP_FLASH, VOLDY_HIT_FX)
    strip_add_fx(STRIP_BOLT, KID_BLUE_FX)
    play_sound('swoosh.wav')

KID_WHITE_FAST_FX = { 
    'delay': 0, 
    'lifetime': 1000, 
    'start': { 'position': 150, 'length': 5, 'spread': 1, 'r': 120, 'g': 80, 'b': 255 },
    'velocity': { 'position': -3, 'length': 0, 'spread': 0, 'r': 255, 'g': 255, 'b': 255 }
}

def do_kid_curse_white_fast():
    strip_add_fx(STRIP_FLASH, VOLDY_HIT_FAST_FX)
    strip_add_fx(STRIP_BOLT, KID_WHITE_FAST_FX)
    play_sound('swoosh.wav')

VOLDY_RED_FX = { 
    'delay': 500, 
    'lifetime': 1000, 
    'start': { 'position': 0, 'length': 5, 'spread': 1, 'r': 255, 'g': 0, 'b': 0 },
    'velocity': { 'position': 2, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_voldy_curse_red():
    clear_head()
    set_head(300, 0, 3)
    sleep(1)
    clear_arm()
    set_arm(1200, 0, 0)
    set_arm(600, 0, 0)
    #set_head(-300, 0, 3)
    play_sound('impervio.wav')
    strip_add_fx(STRIP_BOLT, VOLDY_RED_FX)
    #sleep(3)
    play_sound('downwave.wav')

VOLDY_BLUE_FX = { 
    'delay': 500, 
    'lifetime': 1000, 
    'start': { 'position': 0, 'length': 5, 'spread': 1, 'r': 120, 'g': 80, 'b': 255 },
    'velocity': { 'position': 2, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_voldy_curse_blue():
    clear_head()
    set_head(300, 0, 3)
    sleep(1)
    clear_arm()
    set_arm(1200, 0, 0)
    set_arm(600, 0, 0)
    #cab_arm(600)
    play_sound('sectum.wav')
    strip_add_fx(STRIP_BOLT, VOLDY_BLUE_FX)
    play_sound('downwave.wav')

VOLDY_LUMOS_FX = { 
    'delay': 500, 
    'lifetime': 100, 
    'start': { 'position': 0, 'length': 150, 'spread': 1, 'r': 255, 'g': 250, 'b': 255 },
    'velocity': { 'position': 0, 'length': 0, 'spread': 0, 'r': 0, 'g': 0, 'b': 0 }
}

def do_voldy_lumos():
    clear_head()
    set_head(300, 0, 3)
    sleep(1)
    clear_arm()
    set_arm(1200, 0, 0)
    set_arm(600, 0, 0)
    #cab_arm(600)
    play_sound('lumos.wav')
    strip_add_fx(STRIP_FLASH, VOLDY_LUMOS_FX)
    strip_add_fx(STRIP_BOLT, VOLDY_LUMOS_FX)

EFFECTS = {
    'music': do_music,
    'have you seen': do_haveyouseen,
    'have candy': do_havecandy,
    'cute costume': do_cutecostume,
    'parsel a': do_parsel1,
    'parsel b': do_parsel2,
    'blink': do_blink,
    'kid curse red': do_kid_curse_red,
    'kid curse blue': do_kid_curse_blue,
    'kid curse white fast': do_kid_curse_white_fast,
    'voldy curse red impervio': do_voldy_curse_red,
    'voldy curse blue sectum': do_voldy_curse_blue,
    'voldy lumos': do_voldy_lumos,
}
