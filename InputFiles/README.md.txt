## EXPLANATION FILES

After each group passation, we use the file `CleanUpFiles.R` to clean the raw files by performing the following steps:

 - **Data.** merge the dataset obtained from the 4 participants into 1 single file using the R file

 - **Prosociality.** For each participant, we compute the total prosociality score by additioning the results on each question

 - **Inverse efficiency.** For each participant, we compute the inverse efficiency, where inverse efficiency is defined as $mean(time)/mean(accuracy)$

 - **Cognitive Flexibility.** We measure each participant's cognitive flexibility by examining their performance in a task that involves both numbers and letters. To do this, we calculate two average times: one for when the participant does not switch tasks (moving between letters or numbers) and another for when they do switch tasks (moving from numbers to letters or vice versa). The difference between these two averages represents their cognitive flexibility. We further normalize this difference by dividing it by the mean time required for task switching.

The files in the `Data` folder are named after the group number and type, and it is saved as a .csv file. For instance, Group1HT.csv represents the data file for Group 1 Heterogenous.

The files in the `Data_processed` folder are the same files as the ones in the data folder, except that we added the manually filled "distance" column for heterogenous groups. For more information about how this column was computed, please refer to the html file. 

The files in the `Other` folder are different measures (prosociality, inverse efficiency, cognitive flexibility) are summarized in a separate data file starting with Other_Group…, which includes the group number and type. This file also contains information about age, gender, and results in the dictator game.

The files in the `PreTest` folder concerns (as you may have guessed) the files from a pre-test. In this pre-test, the experimenter did a mistake when asking participants to switch seats. This results in a big mess. Sometimes participants were all standing up at the same time and they may have seen each other computers, which is bad. 
The results of this group goes in the same direction as what we had found (adaptation to the biased participant) but we decided not include it in the analysis, given the error. 
Also, in the raw files, there were in the mistake for the age. Right after the experiment, I corrected the value, which you see in the `Other` folder inside the `PreTest` folder.

