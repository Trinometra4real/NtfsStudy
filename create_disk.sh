VHD="$(pwd)/storage_disk.img"
MOUNTP="$(pwd)/VHD"
SIZE="175M"
rm -f $VHD
touch $VHD
sudo dd if=/dev/zero of=$VHD bs=$SIZE count=1  # bs = block size, count = number of blocks
LOOP=$(sudo losetup -f --show $VHD)
echo "$LOOP">loop
echo "Attached to : $LOOP"
sudo mkfs -t ntfs $LOOP  # sudo mkfs -t <file_system_type> <device mapped>
mkdir -p $MOUNTP         # create Folder destination if does not exists
sudo mount $LOOP $MOUNTP # mount virtual disk to target Destination
