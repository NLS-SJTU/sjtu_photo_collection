# SJTU Photos Collection
## Stage One
### About this mission
Everyone need to take **200** pictures of gendmark buildings in SJTU, and pre-processing then copy them to your group leader.
#### What do you need to do
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
## Stage Two
### About this mission
We need to filter the collected data from stage one, to make sure the data is trustable.
#### What do you need to do
1. Download [`drawPicturesOnMap.py`](https://github.com/NLS-SJTU/sjtu_photo_collection/blob/master/drawPicturesOnMap.py) along with the [sjtu_png.png](https://github.com/NLS-SJTU/sjtu_photo_collection/blob/master/sjtu_png.png) together. Put them into the same folder mentioned in Stage One step 3.
2.  Run this script using python3 (it relys on the package `matplotlib` so you may need to run `pip install matplotlib` first)
    - a. **Fisrt time running the script will have a processing time of 3-5 mins.** Give it some patience untill the UI pop-offs:![image](https://github.com/NLS-SJTU/sjtu_photo_collection/blob/readme-img/2018-09-03%2020-29-23%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)
    - b. Enlarge it and click on any blue point that you think the positioning is not correct. After selcetion it will turn red and the relative image will be shown on right side.![image](https://github.com/NLS-SJTU/sjtu_photo_collection/blob/readme-img/2018-09-03%2020-29-42%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE.png)
    - c. Click the "select into delete list" button to add the picture in to the deleting list
    - d. Repeat b-c untill all the outliers is added into the list.
    - e. If a point is miss-chosen, click the "recover from delete list" button to remove. 
    - f. Click "delete all photos in list" button to remove the unaccurate points.
3. Give your folder to your teamleader. 
