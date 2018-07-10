# SJTU Photos Collection
## About this mission
Everyone need to take **200** pictures of landmark buildings in SJTU, and pre-processing then copy them to your group leader.
## What do you need to do
1. Ask for your group leaders for your responsible regions
    - For group leaders, please refer to [this map](http://www.ldmap.net/map.html?id=af4c396e-c313-45ae-9c93-d30980e1dfe0) for group assignments.
2. Take pictures. 200 pics per person, with these requirements:
    - **Make sure you enabled the positioning functions on your cell phone while taking photos.** We NEED the `EXIF` positionning information in your pictures.
    - Focus on landmark buildings, objects, statues, logos, etc. Diversify as much as possible, such as daytime, evening, sunny, cloudy, rainy, frontal view, side view, featured landmarks with different perspectives etc.
    - No specific 'example' is given here. Because we want the photos as diversify and ramdom as possible. Therefore just taking photos as you are visiting an attractions that you've never seen.
3. Transfer all the pics on your computer in **one** folder, then download the [`rename_photos.py`](https://github.com/NLS-SJTU/sjtu_photo_collection/blob/master/rename_photos.py) from this repo in the same folder. Run this script using python (it relys on the package `exifread` so you may need to run `pip install exifread` first):
```
python ./rename_photos.py
```
4. Copy the entire folder to your teamleader.
