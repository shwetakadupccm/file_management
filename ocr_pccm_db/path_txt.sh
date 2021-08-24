#!/bin/bash
cd /mnt/d/WorkDocs/OneDrive/Prashanti_Data_from_Documents/surgery_reports/Golwilkar_lab_reports/Jehangir_Surgery_Reports
for f in $( ls ); do
	if [[ "$f" =~ .pdf ]]; then
	pdftotext -f 1 -nopgbrk $f "test/${f%.pdf}.txt"; 
	echo $f; 
	echo "test/${f%.pdf}.txt";
	else echo 'file not pdf';
	fi
done
