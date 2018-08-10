#!/usr/bin/env bash

sh "./configs/2018-05-01_small/Replay/Monolithic-15Mins/Runner.sh"

# All category
sh "./configs/2018-05-01_small/Replay/RAll-LAll-S-M15/Runner.sh"
sh "./configs/2018-05-01_small/Replay/RMostFreq-LAll-S-M15/Runner.sh"
sh "./configs/2018-05-01_small/Replay/RGraph-LAll-S-M15/Runner.sh"
sh "./configs/2018-05-01_small/Replay/RRandom-LAll-S-M15/Runner.sh"

# only group category
sh "./configs/2018-05-01_small/Replay/ROneMostFreqSet-LExclude-S-M15/Runner.sh"
sh "./configs/2018-05-01_small/Replay/RThreeMostFreqSet-LExclude-S-M15/Runner.sh"
sh "./configs/2018-05-01_small/Replay/RTenMostFreqSet-LExclude-S-M15/Runner.sh"
sh "./configs/2018-05-01_small/Replay/RScore-LExclude-S-M15/Runner.sh"
