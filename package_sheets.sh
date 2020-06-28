cd ../../
rm muser_sheets.zip
rm muser_sheets_split_*
cd muser_sheets
rm *.sheet
echo the zip will be generated under `pwd`
zip ../muser_sheets ./*
cd ..
split -b 64m muser_sheets.zip muser_sheets_split_