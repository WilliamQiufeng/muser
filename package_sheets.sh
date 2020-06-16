cd ../../
echo the zip will be generated under `pwd`
zip muser_sheets muser_sheets/*/*
split -b 64m muser_sheets.zip muser_sheets_split_