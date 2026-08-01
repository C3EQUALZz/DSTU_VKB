#!/bin/bash

if [ "$(id -u)" != "0" ]; then
	echo -e "\e[33mFailed to start. Permission denied :)\e[0m"
	exit 1
fi

show_help() {
	echo "First argument:"
	echo "  1                  Collecting primary diagnostics (without configuration files)"
	echo "  2                  Collecting secondary diagnostics (with configuration files)"
	echo "  3                  Collecting diagnostics for troubleshooting with firewall problem"
	echo "  -h, --help         This help"
	echo "Usage:"
	echo "  ./$(basename "$0")"
	echo "  ./$(basename "$0") 1"
	echo "  ./$(basename "$0") 2"
	echo "  ./$(basename "$0") 3"
}

if [[ $1 == "-h" || $1 == "--help" ]]; then
    show_help
    exit 0
fi

os_name=$(cat /etc/os-release | grep '^ID=' | cut -d'=' -f2 | tr -d '"' || lsb_release -si 2>/dev/null)
current_date=$(date +"%d-%m-%Y_%H-%M-%S")

if [ -z "$os_name" ]; then
	os_name="unknown"
fi

current_dir=$(pwd)
os_folder=$(mktemp -d "${os_name}_lspdiag.XXXXXX")
if [ ! -d "$os_folder" ]; then
	echo -e "\e[31mFailed to create a temporary directory.\e[0m"
	exit 1
fi

echo "Temporary directory has been created $os_folder"

cleanup() {
	rm -rf "$current_dir/$os_folder" && echo -e "\e[33m\nEmergency stop. The temporary directory $os_folder has been removed.\e[0m"
	exit
}

trap cleanup SIGINT SIGTERM

cd "$os_folder" || exit

log_file="script_output.log"
touch "$log_file" 

if command -v dpkg &> /dev/null; then
    package_manager="dpkg -l"
elif command -v rpm &> /dev/null; then
    package_manager="rpm -qa"
fi

collect_primary_diagnostics() {
    {
        echo "Collecting primary diagnostics..."
        uname -a > uname.txt
        cat /etc/*release > release.txt
        $package_manager > "$package_manager.txt"
		systemctl list-unit-files > systemctl.txt
        /opt/secretnet/bin/snpolctl -l > snpolctl.txt
        /opt/secretnet/sbin/snfc -t > snfc.txt

        echo "Collecting /var/log..."
		# Исключаем файлы lastlog и tallylog, поскольку они могут занимать значительное место на ВМ (например, до 500 ГБ, встречалось на RedOS), хотя на самом деле могут содержать лишь несколько килобайтов данных. Избегаем ненужного увеличения размера архива.
        tar --exclude='log/lastlog' --exclude='log/tallylog' -czf os_log.tar.gz -C /var log --absolute-names

        if [[ ! -f /var/log/messages && ! -f /var/log/syslog ]]; then
            echo "The /var/log/messages and /var/log/syslog files are missing. Gathering additional information through journalctl..."
            journalctl --since "1 month ago" > journalctl_logs.txt
        fi

        echo "Collecting /opt/secretnet/var/log..."
        tar -czf lsp_log.tar.gz -C /opt/secretnet/var log --absolute-names
    } > "$log_file" 2>&1 # Альтернативный вариант, если нужно помимо лог файла вывести на экран выполнение: | tee -a "$log_file" 2>&1
}

collect_secondary_diagnostics() {
    {
        echo "Collecting secondary diagnostics..."
        uname -a > uname.txt
        cat /etc/*release > release.txt
        $package_manager > "$package_manager.txt"
		systemctl list-unit-files > systemctl.txt
        /opt/secretnet/bin/snpolctl -l > snpolctl.txt
        /opt/secretnet/sbin/snfc -t > snfc.txt

        cat /etc/hostname > hostname
        cat /etc/hosts > hosts
        cat /etc/resolv.conf > resolv.conf
        cat /etc/krb5.conf > krb5.conf
        cat /etc/nsswitch.conf > nsswitch.conf
        cat /etc/samba/smb.conf > smb.conf
        cat /etc/security/pam_winbind.conf > pam_winbind.conf
        cat /etc/sssd/sssd.conf > sssd.conf

        echo "Collecting /var/log..."
        tar --exclude='log/lastlog' --exclude='log/tallylog' -czf os_log.tar.gz -C /var log --absolute-names

        if [[ ! -f /var/log/messages && ! -f /var/log/syslog ]]; then
            echo "The /var/log/messages and /var/log/syslog files are missing. Gathering additional information through journalctl..."
            journalctl --since "1 month ago" > journalctl_logs.txt
        fi

        echo "Collecting /opt/secretnet/var/log..."
        tar -czf lsp_log.tar.gz -C /opt/secretnet/var log --absolute-names
    } > "$log_file" 2>&1
}

collect_fw_diagnostics() {
    {
        echo "Collecting firewall diagnostics..."
        uname -a > uname.txt
        cat /etc/*release > release.txt
        $package_manager > "$package_manager.txt"
		systemctl list-unit-files > systemctl.txt
        /opt/secretnet/bin/snpolctl -l > snpolctl.txt
        /opt/secretnet/sbin/snfc -t > snfc.txt
        
        echo "Collecting /var/log..."
        tar -czf os_log.tar.gz -C /var log --absolute-names
        
        if [[ ! -f /var/log/messages && ! -f /var/log/syslog ]]; then
            echo "The /var/log/messages and /var/log/syslog files are missing. Gathering additional information through journalctl..."
            journalctl --since "1 month ago" > journalctl_logs.txt
        fi

        echo "Collecting /opt/secretnet/var/log..."
        tar --exclude='log/lastlog' --exclude='log/tallylog' -czf os_log.tar.gz -C /var log --absolute-names
        
        echo "Collecting /opt/snlsp-firewall/var/log/suricata..."
        tar -czf lspfw_log.tar.gz -C /opt/snlsp-firewall/var/log suricata --absolute-names
        
        fw-localcfg --show --all > fw_rules.txt 2>&1
        systemctl status snlsp-firewall > fw_status.txt
    } > "$log_file" 2>&1
}

if [ $# -eq 1 ]; then
    case $1 in
        1)
            choice="1"
			collect_primary_diagnostics
            ;;
        2)
            choice="2"
			collect_secondary_diagnostics
            ;;
        3)
            choice="3"
			collect_fw_diagnostics
            ;;
        *)
            echo -e "\e[31mInvalid value. Valid value: 1, 2, 3. The temporary directory $os_folder has been removed.\e[0m"
            rm -rf "$current_dir/$os_folder"
            exit 1
            ;;
    esac
else
    echo "Select the type of diagnosis:"
    echo "1. Collecting primary diagnostics (without configuration files)"
    echo "2. Collecting secondary diagnostics (with configuration files)"
    echo "3. Collecting FW diagnostics"

    read -p "Enter the number: " choice

    case $choice in
        1)
            collect_primary_diagnostics
            ;;
        2)
            collect_secondary_diagnostics
            ;;
        3)
            collect_fw_diagnostics
            ;;
        *)
            echo -e "\e[31mInvalid value. The temporary directory $os_folder has been removed.\e[0m"
            cd "$current_dir" && rm -rf "$current_dir/$os_folder"
            exit 1
            ;;
    esac
fi

archive_name="lspdiag_$(hostname)_type_${choice}_${current_date}.tar.gz"

echo "Archiving the data..."
cd "$current_dir"
saved_folder_name="lspdiag_$(hostname)_type_${choice}_${current_date}"
mv "$os_folder" "$saved_folder_name"
os_folder="$saved_folder_name"
tar -czf "$archive_name" "$os_folder" && rm -rf "$os_folder"

echo -e "\e[32mThe diagnostic information is stored in an archive $archive_name located in the current directory.\e[0m"
