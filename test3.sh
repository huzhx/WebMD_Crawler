#!/bin/bash
basepath="/home/huzhx/WebMD_code/WebMD_code/"

for i in {A..Z};
do
#	tarfile=$basepath"topics_"$i".html"
	#echo $tarfile
#	outfile1=$basepath"topics_"$i".txt"
#	if [ ! -f "$outfile" ]
#		then
#			scrapy crawl seeds -a filename="file:"$tarfile > $outfile1
#	fi

#	outfile2=$basepath"topicsDTR_"$i".txt"
#	if [ ! -f "$outfile2" ]
#		then
#			scrapy crawl expseeds -a filename=$outfile1 > $outfile2
#	fi

	outfile3=$basepath"topicsDTR_Questions_Comments_URLs_"$i
#	if [ ! -f "outfile3" ]
#		then
#			scrapy crawl questionsCommentsURL -a filename=$outfile2 > $outfile3
			#scrapy crawl getqs -a filename=$outfile2 -o $outfile3 -t json
#	fi
	outfile4=$basepath"topicsDTR_Questions_Comments_Contents_"$i
	if [ ! -f "$outfile4" ]
		then
			scrapy crawl questionsCommentsContent -a filename=$outfile3 > $outfile4 
	fi
done