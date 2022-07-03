# Pico-LCD-1.14_Flagman
### How to run Flagman
Open the files in **Library**, and save them to your Raspberry Pi Pico.
Then, run **Flagman.py** in Thonny.

### How to add your images
Save your image in 24 bmp. Run **henkan_linux** (in Linux) or **henkan_windows.exe** (in Windows). In the *henkan* program, select mode **8** (bmp -> python bytearray) and write the path to the image. Finally, copy the content of the output file, and use it as a string variable in **Library/ImageData.py**.

### Updates
Notice that the number you should choose in the *henkan* programs is changed from 9 to **8**!
There will probably be some updates on them. 