# Text-To-Latex

This is the ITSP project for our Team Textify-import freSHE

Aim- we aim to detect text in scene images and convert it into digital format. Also, if there is any mathematical expression in the text, we aim to make it into latex formatted text. 

How to Use-
* The OCR and formatting part are separate as of now. 
* To run the OCR part, run `python ocr.py`. To use custom image, change the path of image in `ocr.py`.
* To run the formatting part, run `python main.py` inside the regex folder in the repo. The text is set in `data.txt` file. 

* For prediction of handwritten text, follow:
	- `cd src`
	- For sample test, uncomment the last two lines of the file **predict.py**, change *image_path* variable to one of the images in `src/images/` directory and run `python predict.py`.
	- For deployment, use function *predictions* in **predict.py**.    