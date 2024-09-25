# Вывести текущего владельца папки (файла) и список назначенных NTFS разрешений:
Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" | Select-Object Owner
Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" | Select-Object Access
# Скопировать NTFS разрешения с одной папки и применить их на другую:
$Acl1 = Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub"
Set-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\test" -AclObject $Acl1
# Предоставить конкретному пользователю и группе полные права на папку:
$Acl2 = Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub"
$Rule = New-Object System.Security.AccessControl.FileSystemAccessRule("srmvo", "FullControl", "Allow")
$Acl2.SetAccessRule($Rule)
Set-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" -AclObject $Acl2
# Предоставить права только на верхнем уровне и не изменять разрешения на вложенные объекты (только на папку):
$Acl3 = Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub"
$Rule = New-Object System.Security.AccessControl.FileSystemAccessRule("srmvo", "FullControl", "Allow")
$Acl3.SetAccessRule($Rule)
Set-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" -AclObject $Acl3
# Исключить NTFS доступ к папке для пользователя или группы:
$Acl4 = Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub"
$Acl4.GetAccessRules($true, $false, [System.Security.Principal.NTAccount]) | where { $_.IdentityReference -eq "danko" } | foreach { $Acl4.RemoveAccessRule($_) }
Set-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" -AclObject $Acl4
# Лишить указанную учетную запись прав на все вложенные объекты в указанной папке:
icacls "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" /deny "Tester":(OI)(CI)N /T
# Назначить учетную запись Administrator владельцем всех вложенных объектов в каталоге:
$Acl5 = Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub"
$Acl5.SetOwner([System.Security.Principal.NTAccount]"BUILTIN\Administrators")
Set-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" -AclObject $Acl5
# Включить NTFS наследование для всех объектов в каталоге:
$Acl6 = Get-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub"
$Acl6.SetAccessRuleProtection($false, $true)
Set-Acl -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub" -AclObject $Acl6
# Проверить эффективные NTFS разрешения на конкретный файл:
Get-Acl -Audit -Path "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\testing.txt"
