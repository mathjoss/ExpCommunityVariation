


# --- LOAD LIBRARIES --- #

library(dplyr)


# --- FILL THIS INFORMATION --- #

# Please note that you have to put your files all in the same folder. Then, you have to run the code for each group.
# Fill the information

typee = "HT" # It should be HM or HT depending on the group type
groupnum = 7 # Group number
path_in = "ExpCommunityVariation/InputFiles/Raw/" # The path of the folder with your files
path_out = "ExpCommunityVariation/InputFiles/" # The path of the folder where you want your new files to be stored



# --- READ FILES --- #

# enter path file

pathfiles = paste(path_in, "Group", as.character(groupnum), typee, "/", sep="")
pathfiles_out = path_out

# list all files in the folder
lfiles = list.files(path=pathfiles, pattern=NULL, all.files=FALSE,full.names=FALSE)

# read these files, add a short/long column and an ID column, and bind
df = data.frame(matrix(ncol=24, nrow=0))
df_PS = data.frame(matrix(ncol=5, nrow=0))
df_TS = data.frame(matrix(ncol=8, nrow=0))

counter=1


for (fil in lfiles){
  
  # for prosociality files
  if (startsWith(fil, "PS_file")) {
    # read file
    d_PS <- read.csv(paste(pathfiles, fil, sep=""), header=T)
    
    # add participant ID information
    part_id = substr( as.character(fil), 27, 28)
    part_id = as.numeric(gsub("[^0-9.-]", "", part_id))
    d_PS$PartID = part_id
    
    # add group num infomation
    group_num = substr( as.character(fil), 14, 15)
    group_num = as.numeric(gsub("[^0-9.-]", "", group_num))
    d_PS$GroupNum = group_num
    
    # bind to other dataframe
    df_PS <- rbind(df_PS, d_PS)
    
    # for data files
    } else if (startsWith(fil, "TS_file")) {
      # read file
      d_TS <- read.csv(paste(pathfiles,  fil, sep=""), header=T)
      
      # add participant ID information
      part_id = substr( as.character(fil), 27, 28)
      part_id = as.numeric(gsub("[^0-9.-]", "", part_id))
      d_TS$PartID = part_id
      
      # add group num infomation
      group_num = substr( as.character(fil), 14, 15)
      group_num = as.numeric(gsub("[^0-9.-]", "", group_num))
      d_TS$GroupNum = group_num
      
      # bind to other dataframe
      df_TS <- rbind(df_TS, d_TS)
      
      # for data files
  } else {
    # read file
    d <- read.csv(paste(pathfiles,  fil, sep=""), header=T, sep=",")
    
    d$index=c(1:nrow(d))
    # bind to other dataframe
    df <- rbind(df, d)
  }
  
}


# --- CLEAN DATA FILES --- #

# remove not beautiful data
df[df == 999] <- NA
df[df == "none"] <- NA

# remove useless column
df <- df[,!names(df) %in% c("GoodItem", "GoodAngle")]

# create a pair column
df$pair <- paste(df$PartID, df$Partner, sep="_")
df$pair[df$pair == "2_1"] <- "1_2"
df$pair[df$pair == "3_1"] <- "1_3"
df$pair[df$pair == "4_1"] <- "1_4"
df$pair[df$pair == "3_2"] <- "2_3"
df$pair[df$pair == "4_2"] <- "2_4"
df$pair[df$pair == "4_3"] <- "3_4"
df$pair[df$TypeTest!="ComGame_Producer" & df$TypeTest!="ComGame_Guesser"] <- NA

# create a special ID column for each interaction
df$ID_test <- paste(df$Round, df$ID_CG, df$pair, sep="__")

# build a new dataframe df_final (include at first not CG data)
df_final <- df[!(df$TypeTest == "ComGame_Producer" | df$TypeTest == "ComGame_Guesser"),]

# iterate through each special ID
for (el in unique(df$ID_test)){
  # merge guesser and producer columns
  subdf <- df[df$ID_test==el,]
  subdf$Word[subdf$TypeTest=="ComGame_Guesser"] <- subdf$Word[subdf$TypeTest=="ComGame_Producer"]
  subdf$Shape[subdf$TypeTest=="ComGame_Guesser"] <- subdf$Shape[subdf$TypeTest=="ComGame_Producer"]
  final_row <-  subdf[subdf$TypeTest=="ComGame_Guesser",]
  
  # add rows to final dataframe
  df_final <- rbind(df_final, final_row)
}

# remove useless column
df_final <- df_final[,!names(df_final) %in%  c("ID_test")]




# --- PROSOCIALITY & TASK SWITCHING --- #

# compute average prosociality scale for each participant
df_PS %>%
  filter(ItemNum < 20) %>%
  group_by(PartID, GroupNum) %>%
  summarize(prosoc = mean(Answer)) -> score_prosocio

df_PS %>%
  filter(ItemNum==888) %>%
  select(PartID, Answer) %>%
  rename(Game = Answer) -> game

df_PS %>%
  filter(ItemNum==9889 & Answer > 5) %>%
  select(PartID, Answer) %>%
  rename(Age = Answer) -> age

df_PS %>%
  filter(ItemNum==9889 & Answer < 6) %>%
  select(PartID, Answer) %>%
  rename(Gender = Answer) %>%
  mutate(Gender = case_when(Gender == 1 ~ "F",
                            Gender == 2 ~ "M",
                            Gender == 3 ~ "NB")) -> gender

df_PS_ok <- merge(score_prosocio, game, by="PartID")
df_PS_ok <- merge(df_PS_ok, age, by="PartID")
df_PS_ok <- merge(df_PS_ok, gender, by="PartID")

df_TS %>%
  filter(BlockName == "lettersnumbers" & switch == 1 & acc == 1) %>%
  group_by(PartID) %>%
  summarize(mean_time_switch = mean(time)) -> h
  

df_TS %>%
  filter(BlockName == "lettersnumbers" & switch == 0 & acc == 1) %>%
  group_by(PartID) %>%
  summarize(mean_time_noswitch = mean(time)) -> g

i <- merge(h, g, by="PartID")

i$difference <- i$mean_time_switch - i$mean_time_noswitch
i$diff_nom <- i$difference / i$mean_time_switch

# now find the average inverse efficiency:
df_TS %>%
  group_by(PartID) %>%
  summarize(mean_acc = mean(acc)) -> acc

df_TS %>%
  filter(acc==1) %>%
  group_by(PartID) %>%
  summarize(mean_time = mean(time)) -> time

invefi = merge(acc, time, by="PartID")
invefi$invefi <- invefi$mean_time / invefi$mean_acc

# now find the average inverse efficiency:
df_TS %>%
  filter(BlockName == "lettersnumbers") %>%
  group_by(PartID) %>%
  summarize(mean_acc = mean(acc)) -> acc2

df_TS %>%
  filter(BlockName == "lettersnumbers" & acc==1) %>%
  group_by(PartID) %>%
  summarize(mean_time = mean(time)) -> time2

invefi2 = merge(acc2, time2, by="PartID")
invefi2$invefi <- invefi2$mean_time / invefi2$mean_acc

all_TS <- merge(invefi2, i, by="PartID")

all_TS %>%
  select(PartID, invefi, difference, diff_nom) %>%
  rename(diff_norm = diff_nom) -> all_TS

data_other <- merge(df_PS_ok, all_TS, by="PartID")


# --- WRITE FINAL FILES --- #

# write file
write.csv(df_final, paste(pathfiles_out, "Data/Group", as.character(groupnum),typee, ".csv", sep=""), row.names=FALSE)

# write file
write.csv(data_other, paste(pathfiles_out, "Other/OtherInfo_Group", as.character(groupnum), typee, ".csv", sep=""), row.names=FALSE)
