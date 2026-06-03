MOUNTP="$(pwd)/VHD"
VHD="$(pwd)/storage_disk.img"
LOOP=$(sudo losetup -f $VHD --show)
echo "Attaching loop: $LOOP"
sudo mount $LOOP $MOUNTP
echo "Disk mounted : $MOUNTP"
