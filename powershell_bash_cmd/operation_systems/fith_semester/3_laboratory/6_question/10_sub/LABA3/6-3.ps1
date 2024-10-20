# Set the drive letter to monitor
$driveLetter = "C"

# Set the free space threshold in percentage
$threshold = 70

# Load the System.Windows.Forms assembly
Add-Type -AssemblyName System.Windows.Forms

# Check free space and display a message box if threshold is exceeded
$freeSpacePercentage = (Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='${driveLetter}:'").FreeSpace / (Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='${driveLetter}:'").Size * 100

if ($freeSpacePercentage -lt $threshold) {
    # Display a message box
    [System.Windows.Forms.MessageBox]::Show("Low free space on drive $driveLetter. Please free up some space.", "Disk Space Warning", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
}