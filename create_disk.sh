VHD="$(pwd)/storage_disk.img"
MOUNTP="$(pwd)/VHD"
SIZE="2M"

sudo dd if=/dev/zero of=$VHD/storage_disk.iso bs=$SIZE count=1  # bs = block size, count = number of blocks
sudo mkfs -t ext4 $VHD/storage_disk.iso # sudo mkfs -t <file_system_type> <virtual hard disk>
mkdir $MOUNTP
sudo mount -o loop $VHD/storage_disk.iso $MOUNTP # mount virtual disk to target Destination
