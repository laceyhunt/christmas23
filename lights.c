#include <stdio.h>
#include <pigpio.h>
#include <unistd.h>
#include <stdlib.h>

#define GPIO_PIN 17  // Replace with your desired GPIO pin
#define AUDIO_FILE "your_audio_file.wav"  // Replace with the path to your audio file

void playAudio() {
    char command[256];
    snprintf(command, sizeof(command), "aplay %s", AUDIO_FILE);
    system(command);
}

int main() {
    if (gpioInitialise() < 0) {
        fprintf(stderr, "Error: pigpio initialization failed.\n");
        return 1;
    }

    if (gpioSetMode(GPIO_PIN, PI_INPUT) != 0) {
        fprintf(stderr, "Error: Failed to set GPIO pin mode.\n");
        gpioTerminate();
        return 1;
    }

    if (gpioSetPullUpDown(GPIO_PIN, PI_PUD_DOWN) != 0) {
        fprintf(stderr, "Error: Failed to set pull-up/pull-down resistor.\n");
        gpioTerminate();
        return 1;
    }

    while (1) {
        if (gpioRead(GPIO_PIN) == 1) {
            // GPIO pin is set (e.g., connected to a button press)
            playAudio();
            usleep(500000);  // Wait for 500ms to debounce
        }
    }

    gpioTerminate();
    return 0;
}