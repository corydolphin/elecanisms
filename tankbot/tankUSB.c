#include <p24FJ128GB206.h>
#include "config.h"
#include "common.h"
#include "ui.h"
#include "uart.h"
#include "timer.h"
#include "pin.h"
#include "oc.h"
#include "usb.h"
#include <stdio.h>
#include <math.h>


// Define the left and right pins
_PIN* PWM_L = &D[0];
_PIN* IN_LA = &D[1];
_PIN* IN_LB = &D[2];
_PIN* PWM_R = &D[11];
_PIN* IN_RA = &D[12];
_PIN* IN_RB = &D[13];

#define MAX_POS 32767
#define MAX_NEG (-32768)

#define HELLO       0
#define SET_MOTORS  1


void update_motors(int16_t lMotorSpeed, int16_t rMotorSpeed){
    // set direction
    if (lMotorSpeed < 0){
        pin_clear(IN_LB);
        pin_set(IN_LA);
        printf("left backwards\n");
    }else{
        pin_set(IN_LB);
        pin_clear(IN_LA);
        printf("left forwards\n");
    }

    if (rMotorSpeed < 0){
        pin_clear(IN_RB);
        pin_set(IN_RA);
        printf("right backwards\n");
    }else{
        pin_set(IN_RB);
        pin_clear(IN_RA);
        printf("right forwards\n");
    }

    // set speed
    // TODOL think about what will happen for MAX_NEG
    pin_write(PWM_L, abs(lMotorSpeed)*2);
    pin_write(PWM_R, abs(rMotorSpeed)*2);
}

void init(){
    init_clock();
    init_ui();
    init_uart();
    init_timer();
    init_pin();
    init_oc();
    InitUSB();

    // status light
    led_on(&led1);

    // initialize the motors to zero
    pin_digitalOut(IN_LA);
    pin_digitalOut(IN_LB);
    pin_digitalOut(IN_RA);
    pin_digitalOut(IN_RB);
    oc_pwm(&oc1, PWM_L, NULL, 10E3, 0);
    oc_pwm(&oc2, PWM_R, NULL, 10E3, 0);

    // timer for the blinking light
    timer_setPeriod(&timer2, 0.5);
    timer_start(&timer2);

    printf("\n\nInitialized PIC\n");
}

int16_t main(void) {

    init();
    while (USB_USWSTAT!=CONFIG_STATE) {     // while the peripheral is not configured...
        ServiceUSB();                       // ...service USB requests
    }
    while (1) {
        ServiceUSB();
    }

}

void VendorRequests(void) {
    WORD temp;
    int16_t lMotorSpeed, rMotorSpeed;

    switch (USB_setup.bRequest) {
        case HELLO:
            printf("Hello World!\n");
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit
            break;
        case SET_MOTORS:
            //extract data
            lMotorSpeed = USB_setup.wValue.w;
            rMotorSpeed = USB_setup.wIndex.w;
            BD[EP0IN].bytecount = 0;    // set EP0 IN byte count to 0 
            BD[EP0IN].status = 0xC8;    // send packet as DATA1, set UOWN bit

            update_motors(lMotorSpeed, rMotorSpeed);
            printf("Left Motor Speed: %6d Right Motor Speed: %6d\n", lMotorSpeed, rMotorSpeed);
            break;
        default:
            USB_error_flags |= 0x01;    // set Request Error Flag
    }
}

void VendorRequestsIn(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;                    // set Request Error Flag
    }
}

void VendorRequestsOut(void) {
    switch (USB_request.setup.bRequest) {
        default:
            USB_error_flags |= 0x01;                    // set Request Error Flag
    }
}