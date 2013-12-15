#include <p24FJ128GB206.h>
#include "config.h"
#include "common.h"
#include "ui.h"
#include "timer.h"
#include "pin.h"
#include "oc.h"


_PIN* PWM_1 = &D[0];
_PIN* IN_1A = &D[1];
_PIN* IN_1B = &D[2];
_PIN* PWM_2 = &D[11];
_PIN* IN_2A = &D[12];
_PIN* IN_2B = &D[13];

int16_t main(void) {

    init_clock();
    init_ui();
    init_timer();
    init_pin();
    init_oc();

    led_on(&led1);
    pin_digitalOut(IN_1A);
    pin_digitalOut(IN_1B);
    pin_digitalOut(IN_2A);
    pin_digitalOut(IN_2B);

    timer_setPeriod(&timer2, 0.5);
    timer_start(&timer2);

    uint16_t analog_0, command;
    oc_pwm(&oc1, PWM_1, NULL, 10E3, 65535);
    oc_pwm(&oc2, PWM_2, NULL, 10E3, 65535);

    while (1) {
        if (timer_flag(&timer2)) {
            timer_lower(&timer2);
            led_toggle(&led1);
            led_toggle(&led2);
        }
        pin_clear(IN_1B);
        pin_set(IN_1A);
        pin_clear(IN_2B);
        pin_set(IN_2A);
    }

}

