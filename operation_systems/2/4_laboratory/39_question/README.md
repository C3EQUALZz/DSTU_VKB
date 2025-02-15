## Зарегистрируйтесь в системе в консольном режиме с правами `root`. Используя команду `cat` с правами `root`, просмотрите содержимое файлов `/etc/passwd` и `/etc/shadow`. Вам необходимо создать учетные записи и определить права доступа для десяти (10) сотрудников: `w_gromov`, `n_kalinina`, `e_ivanova`, `r_klinova`, `b_rebrov`, `k_beglov`, `i_frolov`, `d_lavrov`, `m_kruglov`, `t_uporov`, работающих в одном подразделении и занятых созданием и редактированием текстовых документов различного уровня конфиденциальности. Разграничение доступа к информации должно быть произведено на основании следующих требований: - допуск к секретным сведениям имеют четыре пользователя: `w_gromov`, `n_kalinina`, `b_rebrov`, `k_beglov`; - три пользователя: `n_kalinina`, `b_rebrov`, `k_beglov` работают над созданием секретных документов, каждый по своему профилю. Их домашние каталоги и файлы должны быть полностью недоступными как друг для друга, так и для всех остальных, исключая `w_gromov`; - три пользователя: `i_frolov`, `d_lavrov`, `e_ivanova` имеют допуск к конфиденциальной информации и работают над документами с соответствующим грифом. Они имеют право читать файлы с конфиденциальной информацией, созданные своими коллегами, без права их модификации; - все секретоносители имеют право знакомиться с конфиденциальными файлами; - три пользователя: `r_klinova`, `m_kruglov`, `t_uporov` могут работать только с открытой информацией. Их файлы должны быть доступны для чтения каждому сотруднику подразделения (без права модификации); - `w_gromov` является редактором подразделения и имеет право читать и модифицировать файлы всех сотрудников и всех уровней конфиденциальности. Завершенные документы копируются пользователем `w_gromov` в его домашний каталог, который должен быть недоступен для всех остальных сотрудников подразделения. Укажите в отчете, какие коллизии вы усматриваете в сформулированных требованиях? Как реализовать указанные требования таким образом, чтобы пользователи не могли по своему усмотрению изменять установленный порядок?

Шаг 1: Создание учетных записей пользователей
sudo useradd -u 510  -d /home/w_gromov -m -p gromov510 w_gromov
sudo useradd -u 508 -d /home/n_kalinina -m -p kalinina508 -e 2024-12-31 n_kalinina
sudo useradd -u 505 -d /home/e_ivanova -m -p parolparol -e 2024-09-31 e_ivanova
sudo useradd -u 509 -d /home/r_klinova -m -p parolparol -e 2024-06-31 r_klinova
sudo useradd -u 503 -d /home/b_rebrov -m -p rebrov503 -e 2024-07-31 b_rebrov
sudo useradd -u 507 -d /home/k_beglov -m -p beglov507 -e 2024-08-20 k_beglov
sudo useradd -u 501 -d /home/i_frolov -m -p frolov501 -e 2024-12-10 i_frolov
sudo useradd -u 504 -d /home/d_lavrov -m -p lavrov504 -e 2024-12-31 d_lavrov
sudo useradd -u 502 -d /home/m_kruglov -m -p kruglov502 -e 2024-12-31 m_kruglov
sudo useradd -u 506 -d /home/t_uporov -m -p uporov506 -e 2024-12-31 t_uporov

Создаём группы секретности:
groupadd secret         # Для пользователей с допуском к секретным сведениям
groupadd confidential   # Для пользователей с допуском к конфиденциальным сведениям
groupadd open          # Для пользователей, работающих только с открытой информацией

Добавляем пользователей
usermod -aG secret w_gromov
usermod -aG secret n_kalinina
usermod -aG secret b_rebrov
usermod -aG secret k_beglov

usermod -aG confidential i_frolov
usermod -aG confidential d_lavrov
usermod -aG confidential e_ivanova

usermod -aG open r_klinova
usermod -aG open m_kruglov
usermod -aG open t_uporov

Настройка прав 
n_kalinina, b_rebrov, k_beglov:
chmod 700 /home/n_kalinina
chmod 700 /home/b_rebrov
chmod 700 /home/k_beglov

i_frolov, d_lavrov, e_ivanova:
mkdir /home/confidential
chown root:confidential /home/confidential
chmod 770 /home/confidential

r_klinova, m_kruglov, t_uporov:
mkdir /home/open
chown root:open /home/open
chmod 755 /home/open
chmod g+s /home/open

w\_gromov:** Его домашний каталог должен быть недоступен для всех остальных:
chmod 700 /home/w_gromov

Настройка прав доступа к файлам:

**Секретные файлы:**
Файлы, создаваемые n\_kalinina, b\_rebrov и k\_beglov, должны быть доступны только им самим и w\_gromov. 
Права на файлы, создаваемые в их домашних каталогах, будут определяться `umask`. Чтобы обеспечить максимальную защиту, 
можно изменить `umask` для этих пользователей в их `.bashrc` файлах:

echo "umask 077" >> /home/n_kalinina/.bashrc
echo "umask 077" >> /home/b_rebrov/.bashrc
echo "umask 077" >> /home/k_beglov/.bashrc

**Конфиденциальные файлы:**
Пользователи i\_frolov, d\_lavrov и e\_ivanova должны создавать свои файлы в `/home/confidential`. 
Пользователь владелец файла будет задавать права доступа.

**Открытые файлы:**
Пользователи r\_klinova, m\_kruglov и t\_uporov должны создавать свои файлы в `/home/open`. 
Пользователь владелец файла будет задавать права доступа.

Настройка прав доступа для w_gromov:

w\_gromov должен иметь возможность читать и модифицировать файлы всех сотрудников и всех уровней конфиденциальности. 
Самый простой способ реализовать это - добавить пользователя `w_gromov` в группу `sudo`.

