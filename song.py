import pygame

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust the tick rate as needed

    pygame.mixer.quit()

if __name__ == "__main__":
    mp3_file = "ChristmasTrain2.mp3"  # Replace with the path to your MP3 file
    play_mp3(mp3_file)
