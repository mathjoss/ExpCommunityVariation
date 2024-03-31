In this folder, you can find the data and code supporting the analysis of the paper. 

## Explanation of the folders and files

 - In the folder `SupplementaryMaterials_files`, you will find additional formatting files automatically created by quarto and which enables to load the images inside the html file of the SupplementaryMaterials.
 
 - The folder `figures` shows the automatically generated pictures from the RMarkdown file

 - The folder `Pictures` shows the pictures as well as the illustrations made for the paper (on Inkscape or Powerpoint)

 - The folder `InputFiles` shows all data. More information is available in the README.md file inside this folder.

 - The folder `Program_Experiment` contains the program made to perform the experiment.

The file `SupplementaryMaterials.qmd` is the RMarkdown file used to perform the analysis and generate the Supplementary Materials. The output can be visualized in the file `SupplementaryMaterials.html`.


## ADDING NEW GROUPS

If you want to add new groups, you should have a setup similar to the one you can see in `Photo_Design` in the `Pictures` folder. 

**Materials:**
- four tables
- four computers (no specific requirement)
- four rotating "thinggy" (not sure how it should be called; basically you put your computer on these things and it makes it easier to rotate your computer)
- something to prevent participants sitting face to face to see participants next to them (a curtain would do)
No internet connection needed.
- some little black sticker or paste to put on the keyboard to make it evident which letter they can use
- print the files that indicates on which table to sit
- print the files for debriefing and for consent

**Procedure:**
- First, download the `Program_Experiment` folder. Then, ... (write infos that I wrote to Oxana)

- Gather the files obtained on all computers in a single folder, that you should name "GroupNUMBERTYPE" so for example "Group4HT" (if heterogenous= or "Group5HM" (if control/homogenous). Put this folder inside the `Raw` folder in the `InputFiles` folder.

- Then, use the program `CleanUpFiles.R` to clean the Raw files. See the README.md files inside the `InputFiles` folder for more information about this cleaning.

- Run the files `SupplementaryMaterials.qmd` to analyze all data.