## 1) Управление разрешениями на объекты файловой системы NTFS из PowerShell:

- вывести текущего владельца папки (файла) и список назначенных NTFS
разрешений

```
$path = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\test"
Get-Acl $path | Format-List
```

- предоставить конкретному пользователю и группе полные права на папку

```
$path = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\test"
$acl = Get-Acl $path
$permission = "DOMAIN\User","FullControl","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
Set-Acl $path $acl
```

- предоставить права только на верхнем уровне и не изменять разрешения на
вложенные объекты (только на папку)

```
$path = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\test"
$acl = Get-Acl $path
$permission = "DOMAIN\User","FullControl","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission, "None", "ContainerInherit, ObjectInherit", "None"
$acl.SetAccessRule($accessRule)
Set-Acl $path $acl
```

- убрать NTFS доступ к папке для пользователя или группы

```
$path = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\test"
$acl = Get-Acl $path
$permission = "DOMAIN\User","FullControl","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission, "Remove"
$acl.SetAccessRule($accessRule)
Set-Acl $path $acl
```

- лишить указанную учетную запись прав на все вложенные объекты в указанной папке

```
$acl = Get-Acl $path
$permission = "DOMAIN\User","FullControl","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission, "Remove"
$acl.SetAccessRule($accessRule)
Set-Acl $path $acl
```

- назначить учетную запись Administrator владельцем всех вложенных объектов в каталоге

```
$path = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\test"

$acl = Get-Acl $path
$owner = New-Object System.Security.Principal.NTAccount("Administrator")
$acl.SetOwner($owner)
Set-Acl $path $acl

# Для вложенных объектов
Get-ChildItem $path -Recurse | ForEach-Object {
    $childAcl = Get-Acl $_.FullName
    $childAcl.SetOwner($owner)
    Set-Acl $_.FullName $childAcl
}

```
- проверить эффективные NTFS разрешения на конкретный файл.

```
$path = "D:\PycharmProjects\DSTU_VKB\powershell_bash_cmd\operation_systems\fith_semester\3_laboratory\6_question\11_sub\testing.txt"
$identity = "DOMAIN\User"
$acl = Get-Acl $path
$effectiveRights = $acl.Access | Where-Object { $_.IdentityReference -eq $identity }
$effectiveRights
```

> [!NOTE]
> Примечание. Для управления доступом к файлам и папкам в Windows на каждый объект файловой системы NTFS (каталог или файл) назначается специальный
ACL (Access Control List, список контроля доступа).
> В ACL объекта задаются доступные операции (разрешения), которые может совершать с этим объектом пользователь и/или группы.