#!/bin/bash
cd  /mnt/d/WorkDocs/Desktop/Jehangir_Surgery_Path_Reports
for f in $( ls ); do
	if [[ "$f" =~ .pdf ]]; then
	pdftotext -f 1 -nopgbrk $f "test/${f%.pdf}.txt"; 
	echo $f; 
	echo "test/${f%.pdf}.txt";
	else echo 'file not pdf';
	fi
done
