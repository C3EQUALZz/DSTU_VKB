#Выводит информацию по всем установленным драйверам

pnputil.exe /enum-drivers

#Экспортирует все установленные драйвера в C:\drivers

pnputil.exe /export-driver * c:\drivers

#Установка экспортированных драйверов (не рекомендую прописывать, так это может занять некоторое время, сбои и тому подобное)

pnputil.exe /add-driver C:\drivers\*.inf /subdirs /install