# FastAPI-Dice-APP



An API for uploading and converting pictures into a dice mosiac via Dice_Me https://github.com/Chantland/Dice_Me

<kbd>
  <img src="https://github.com/Chantland/Chantland.github.io/blob/master/img/FastAPI_Dice_Ex.png" width="1000" style="border:1px solid black" alt="Before Dice">
</kbd>

Current implementation allows for changing of dice dimensions and may allow for optional imputs later. For full optional inputs, check out the original Dice_Me at Dice_Me https://github.com/Chantland/Dice_Me. You can also use the Dice_Me.py included here, however, NOTE that this Dice_ME.py has been altered slightly to work better with the API and may easily allow for all the optional inputs.

## Setup
1. Make sure that you have the required packages listed in `requirements.txt`. Use `pip install -r requirements.txt` if unsure. Additionally, sometimes some requirements are left out and require separate pip installations. If this is the case, consider using `pip install fastapi uvicorn SQLalchemy opencv-python python-multipart` 
2. In the repository path open a terminal and use `uvicorn main:app --reload` to set up temporary server.
3. If application startup is completed, go to your home address, usually `http://127.0.0.1:8000/` to see the running app.


## Running

- The application allows for uploading of **ANY** image and will give the possible permutations of dice which the image can be made out of. If the image cannot be subdivided (for example the included demo image J&E_With_Vicky.jpg), it will not work. 
- Once you upload a successful image, it will create itself in the "image" and allow for the choice of dice dimensions. Note that the larger the dimensions, the longer the application will take to run so it is recommended to use smaller dimensions (like ones around 100x100 or smaller).
- Once a choice is made, the image will appear and will be stored in the "image-Output" folder. 
- When you are done with the images, you can click the `Delete` button to delete the images from here and in the database SQLight file. 
- You may process as many images at a time as you like and may redo current loaded images by simply choosing a new dice dimension via the dropdown and then clicking submit.
- For the sake of space, it is recommended to delete any images in the "image" and "image-Output" folder you no longer care about.  Additionally, the data is stored in a SQLight database file and will become gradually larger even when images have been deleted from it. Therefore, you can use a cleaning tool through a database IDE or simply delete the database file without any issue.
- As a reminder, the current images in the "image" folder when you download this repository are simply there as an example and are not required to use nor do you need to put your desired images in that folder. They can be uploaded from anywhere.
