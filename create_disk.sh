PATH="$(pwd)/storage_disk.img"
DEST="$(pwd)/VHD"
SIZE="2M"

sudo dd if=/dev/zero of=$PATH/storage_disk.iso bs=$SIZE count=1  # bs = block size, count = number of blocks
sudo mkfs -t ext4 $PATH/storage_disk.iso # sudo mkfs -t <file_system_type> <virtual hard disk>
mkdir $DEST
sudo mount -o loop $PATH/storage_disk.iso $DEST # mount virtual disk to target destination
