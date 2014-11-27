#!/bin/bash
basepath="/home/huzhx/WebMD_code/WebMD_code/"

for i in {P..P};
do
	tarfile=$basepath"topics_"$i".html"
	#echo $tarfile
	outfile1=$basepath"topics_"$i".txt"
	if [ ! -f "$outfile" ]
		then
			scrapy crawl seeds -a filename="file:"$tarfile > $outfile1
	fi

	outfile2=$basepath"topicsDTR_"$i".txt"
	if [ ! -f "$outfile2" ]
		then
			scrapy crawl expseeds -a filename=$outfile1 > $outfile2
	fi

	outfile3=$basepath"topicsDTR_Questions#_Comments#_"$i".txt"
	if [ ! -f "outfile3" ]
		then
			scrapy crawl questionsCommentsAmount -a filename=$outfile2 > $outfile3
	fi
done